"""Render pipeline: manim scenes → joined video with mastered audio, captions, chapters, timeline."""

from __future__ import annotations

import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path

from explainer_kit.paths import display, explainer_dir, tool_env

QUALITY = {"l": "-ql", "m": "-qm", "h": "-qh", "k": "-qk"}


def run(cmd: list, **kwargs) -> subprocess.CompletedProcess:
    print("$", " ".join(str(c) for c in cmd), flush=True)
    return subprocess.run([str(c) for c in cmd], check=True, **kwargs)


def ffprobe_duration(path: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         check=True, capture_output=True, text=True).stdout
    return float(out.strip())


# ---------------------------------------------------------------- captions

def parse_srt(text: str) -> list[tuple[float, float, str]]:
    def t(s: str) -> float:
        h, m, rest = s.split(":")
        sec, ms = rest.replace(".", ",").split(",")
        return int(h) * 3600 + int(m) * 60 + int(sec) + int(ms) / 1000

    cues = []
    for block in re.split(r"\n\s*\n", text.strip()):
        lines = block.strip().splitlines()
        if len(lines) >= 3 and "-->" in lines[1]:
            a, b = (x.strip() for x in lines[1].split("-->"))
            cues.append((t(a), t(b), "\n".join(lines[2:])))
    return cues


def format_srt(cues: list[tuple[float, float, str]]) -> str:
    def t(x: float) -> str:
        ms = round(x * 1000)
        return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}"

    return "\n".join(f"{i}\n{t(a)} --> {t(b)}\n{txt}\n" for i, (a, b, txt) in enumerate(cues, 1))


def format_vtt(cues: list[tuple[float, float, str]]) -> str:
    """WebVTT for <video><track>: same cues, '.' before milliseconds."""
    body = re.sub(r"(\d\d:\d\d:\d\d),(\d\d\d)", r"\1.\2", format_srt(cues))
    return "WEBVTT\n\n" + body


def ffmetadata_chapters(chapters: list[tuple[float, str]], duration: float) -> str:
    lines = [";FFMETADATA1"]
    for i, (start, title) in enumerate(chapters):
        end = chapters[i + 1][0] if i + 1 < len(chapters) else duration
        title = title.replace("=", r"\=").replace(";", r"\;").replace("#", r"\#").replace("\n", " ")
        lines += ["[CHAPTER]", "TIMEBASE=1/1000", f"START={round(start * 1000)}", f"END={round(end * 1000)}",
                  f"title={title}"]
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------- render

def scene_classes(scene_file: Path) -> list[str]:
    return re.findall(r"^class\s+(\w+)\s*\(\s*ExplainerScene\s*\)", scene_file.read_text(), re.M)


def find_output(media: Path, scene: str, ext: str) -> Path | None:
    matches = sorted(media.glob(f"videos/**/{scene}{ext}"), key=lambda p: p.stat().st_mtime)
    return matches[-1] if matches else None


def render(slug: str, scene: str | None = None, quality: str | None = None, draft: bool = False,
           every: float = 4.0) -> Path:
    video = explainer_dir(slug) / "video"
    scene_file = video / "scene.py"
    if not scene_file.exists():
        sys.exit(f"missing {display(scene_file)} — run: explainer new {slug} --stage 4")
    scenes = [scene] if scene else scene_classes(scene_file)
    if not scenes:
        sys.exit("no class(ExplainerScene) found in scene.py")

    media = video / "media"
    env = tool_env()
    env.setdefault("PYTHONWARNINGS", "ignore::SyntaxWarning")  # pydub regex warnings
    env["EXPLAINER_SLUG_DIR"] = str(explainer_dir(slug))
    quality = "l" if draft and not quality else (quality or "h")
    if draft:
        env["EXPLAINER_TTS"] = "silent"
    shutil.rmtree(media / "timeline", ignore_errors=True)
    for name in scenes:
        # sys.executable: the interpreter that has explainer_kit, also under uvx or a plugin install
        run([sys.executable, "-m", "manim", "render", QUALITY[quality], "--media_dir", media, scene_file, name],
            cwd=video, env=env)

    parts = [find_output(media, s, ".mp4") for s in scenes]
    if None in parts:
        sys.exit("manim finished but an output video is missing")

    # Join scenes in file order; shift captions and timeline events by each scene's start.
    cues: list[tuple[float, float, str]] = []
    events: list[dict] = []
    offset = 0.0
    for name, part in zip(scenes, parts):
        srt = part.with_suffix(".srt")
        if srt.exists():
            cues += [(a + offset, b + offset, txt) for a, b, txt in parse_srt(srt.read_text())]
        tl = media / "timeline" / f"{name}.json"
        if tl.exists():
            for e in json.loads(tl.read_text())["events"]:
                e = dict(e, scene=name, t=round(e["t"] + offset, 3))
                if "bookmarks" in e:
                    e["bookmarks"] = {k: round(v + offset, 3) for k, v in e["bookmarks"].items()}
                events.append(e)
        offset += ffprobe_duration(part)

    prefix = "draft-" if draft else ""
    captions = video / f"{prefix}captions.srt"
    captions.write_text(format_srt(cues))
    captions.with_suffix(".vtt").write_text(format_vtt(cues))

    joined = video / "joined.mp4"
    if len(parts) == 1:
        shutil.copy(parts[0], joined)
    else:
        listing = video / "concat.txt"
        listing.write_text("".join(f"file '{p.resolve()}'\n" for p in parts))
        run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", listing, "-c", "copy", joined])
        listing.unlink()

    duration = ffprobe_duration(joined)
    chapters = [(0.0, "Start")] + [(e["t"], f"Predict: {e['question']}") for e in events if e["kind"] == "predict"]
    meta = video / "chapters.txt"
    meta.write_text(ffmetadata_chapters(chapters, duration))

    # Master narration to -16 LUFS (skip for silent drafts); mux soft captions and chapters.
    out = video / ("draft.mp4" if draft else "out.mp4")
    audio = ["-c:a", "aac", "-b:a", "192k"] + ([] if draft else ["-af", "loudnorm=I=-16:TP=-1.5:LRA=11"])
    run(["ffmpeg", "-y", "-v", "error", "-i", joined, "-i", captions, "-i", meta,
         "-map", "0:v", "-map", "0:a?", "-map", "1", "-map_metadata", "2", "-map_chapters", "2",
         "-c:v", "copy", *audio, "-c:s", "mov_text", "-metadata:s:s:0", "language=eng", out])
    joined.unlink()
    meta.unlink()

    timeline = video / f"{prefix}timeline.json"
    timeline.write_text(json.dumps({"duration": round(duration, 3), "events": events}, indent=1))

    sheet = contact_sheet(out, video / f"{prefix}contact.png", every)
    issues = sorted({i for e in events for i in e.get("issues", [])})
    lines = [e["text"] for e in events if e["kind"] == "voiceover"]
    issues += sorted({f"repeated narration: {t[:50]!r}" for t in lines if lines.count(t) > 1})
    print(f"\nvideo     {display(out)}  ({ffprobe_duration(out):.1f}s)")
    print(f"captions  {display(captions)}  ({len(cues)} cues, .srt + .vtt)")
    print(f"timeline  {display(timeline)}  ({len(events)} events, {len(chapters) - 1} predict pauses)")
    print(f"contact   {display(sheet)}  (one frame every {every}s — read it to review)")
    if issues:
        print(f"\nlayout issues ({len(issues)}) — run `explainer review {slug}` to see where:")
        for i in issues:
            print(f"  · {i}")
    return out


def contact_sheet(video_file: Path, dest: Path, every: float) -> Path:
    frames = max(1, math.ceil(ffprobe_duration(video_file) / every))
    cols = 4
    rows = math.ceil(frames / cols)
    run(["ffmpeg", "-y", "-v", "error", "-i", video_file, "-vf",
         f"fps=1/{every},scale=480:-1,drawtext=text='%{{pts\\:hms}}':x=w-tw-8:y=h-th-8:fontsize=18:fontcolor=white:"
         f"box=1:boxcolor=black@0.6,tile={cols}x{rows}:padding=4", "-frames:v", "1", dest])
    return dest
