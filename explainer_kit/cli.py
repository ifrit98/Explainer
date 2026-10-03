"""explainer — CLI for the 3b1b-style video pipeline.

  uv run explainer setup                 download Kokoro model files, check the toolchain
  uv run explainer new <slug>            scaffold explainers/<slug>/ (model, storyboard, scene)
  uv run explainer voices                list Kokoro voices
  uv run explainer say "<text>"          audition a line (--voice, --speed)
  uv run explainer render <slug>         render, master audio, mux captions, write contact sheet
  uv run explainer render <slug> --draft fast layout pass: low quality, silent estimated narration
  uv run explainer frames <slug>         rebuild the contact sheet for visual review
"""

from __future__ import annotations

import argparse
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EXPLAINERS = REPO / "explainers"
TEMPLATES = Path(__file__).resolve().parent / "templates"
MODEL_URL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/"
QUALITY = {"l": "-ql", "m": "-qm", "h": "-qh", "k": "-qk"}


def run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    print("$", " ".join(str(c) for c in cmd), flush=True)
    return subprocess.run([str(c) for c in cmd], check=True, **kwargs)


def ffprobe_duration(path: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         check=True, capture_output=True, text=True).stdout
    return float(out.strip())


# ---------------------------------------------------------------- setup

def cmd_setup(args) -> None:
    from explainer_kit.voice import MODEL_DIR

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    for name in ("kokoro-v1.0.onnx", "voices-v1.0.bin"):
        dest = MODEL_DIR / name
        if dest.exists():
            print(f"ok       {dest}")
            continue
        print(f"download {name} …", flush=True)
        urllib.request.urlretrieve(MODEL_URL + name, dest)
    for tool, why in [("ffmpeg", "required: encode and mux"), ("ffprobe", "required: timing"),
                      ("sox", "optional: global_speed changes"), ("latex", "optional: MathTex / Tex"),
                      ("dvisvgm", "optional: MathTex / Tex")]:
        print(f"{'ok' if shutil.which(tool) else 'missing':8} {tool:8} {why}")
    if not shutil.which("latex"):
        print("\nMathTex needs LaTeX. To enable it, run: brew install --cask basictex  (asks for your password)")


# ---------------------------------------------------------------- new

def cmd_new(args) -> None:
    slug = args.slug
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug):
        sys.exit("slug must be kebab-case, for example: attention-heads")
    root = EXPLAINERS / slug
    video = root / "video"
    video.mkdir(parents=True, exist_ok=True)
    class_name = "".join(part.capitalize() for part in slug.split("-"))
    files = {
        root / "model.md": REPO / ".claude/skills/explain/templates/model.md",
        video / "storyboard.md": TEMPLATES / "storyboard.md",
        video / "scene.py": TEMPLATES / "scene.py",
    }
    for dest, src in files.items():
        if dest.exists():
            print(f"keep     {dest.relative_to(REPO)}")
            continue
        dest.write_text(src.read_text().replace("{{ClassName}}", class_name).replace("{{slug}}", slug))
        print(f"create   {dest.relative_to(REPO)}")


# ---------------------------------------------------------------- voices / say

def cmd_voices(args) -> None:
    from explainer_kit.voice import KokoroService

    voices = sorted(KokoroService.engine().get_voices())
    print("\n".join(v for v in voices if args.all or v[:2] in ("af", "am", "bf", "bm")))


def cmd_say(args) -> None:
    import soundfile as sf

    from explainer_kit.voice import KokoroService

    audio, sr = KokoroService.engine().create(args.text, voice=args.voice, speed=args.speed, lang="en-us")
    out = Path(args.out)
    sf.write(out, audio, sr)
    print(f"{out}  {len(audio) / sr:.2f}s")
    if not args.no_play and shutil.which("afplay"):
        subprocess.run(["afplay", str(out)])


# ---------------------------------------------------------------- render

def scene_classes(scene_file: Path) -> list[str]:
    return re.findall(r"^class\s+(\w+)\s*\(\s*ExplainerScene\s*\)", scene_file.read_text(), re.M)


def find_output(media: Path, scene: str, ext: str) -> Path | None:
    matches = sorted(media.glob(f"videos/**/{scene}{ext}"), key=lambda p: p.stat().st_mtime)
    return matches[-1] if matches else None


def parse_srt(text: str) -> list[tuple[float, float, str]]:
    def t(s: str) -> float:
        h, m, rest = s.split(":")
        sec, ms = rest.split(",")
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
    body = format_srt(cues)
    body = re.sub(r"(\d\d:\d\d:\d\d),(\d\d\d)", r"\1.\2", body)
    return "WEBVTT\n\n" + body


def cmd_render(args) -> None:
    video = EXPLAINERS / args.slug / "video"
    scene_file = video / "scene.py"
    if not scene_file.exists():
        sys.exit(f"missing {scene_file.relative_to(REPO)} — run: uv run explainer new {args.slug}")
    scenes = [args.scene] if args.scene else scene_classes(scene_file)
    if not scenes:
        sys.exit("no class(ExplainerScene) found in scene.py")

    media = video / "media"
    env = os.environ.copy()
    env.setdefault("PYTHONWARNINGS", "ignore::SyntaxWarning")  # pydub regex warnings
    quality = "l" if args.draft and not args.quality else (args.quality or "h")
    if args.draft:
        env["EXPLAINER_TTS"] = "silent"
    for scene in scenes:
        run(["manim", "render", QUALITY[quality], "--media_dir", media, scene_file, scene], cwd=REPO, env=env)

    parts = [find_output(media, s, ".mp4") for s in scenes]
    if None in parts:
        sys.exit("manim finished but an output video is missing")

    # Concatenate scenes in file order; shift captions by the running offset.
    cues: list[tuple[float, float, str]] = []
    offset = 0.0
    for scene, part in zip(scenes, parts):
        srt = part.with_suffix(".srt")
        if srt.exists():
            cues += [(a + offset, b + offset, txt) for a, b, txt in parse_srt(srt.read_text())]
        offset += ffprobe_duration(part)
    captions = video / "captions.srt"
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

    # Master narration to -16 LUFS (skip for silent drafts) and mux soft captions.
    out = video / ("draft.mp4" if args.draft else "out.mp4")
    audio = ["-c:a", "aac", "-b:a", "192k"] + ([] if args.draft else ["-af", "loudnorm=I=-16:TP=-1.5:LRA=11"])
    run(["ffmpeg", "-y", "-v", "error", "-i", joined, "-i", captions, "-map", "0:v", "-map", "0:a?", "-map", "1",
         "-c:v", "copy", *audio, "-c:s", "mov_text", "-metadata:s:s:0", "language=eng", out])
    joined.unlink()

    sheet = contact_sheet(out, video / ("draft-contact.png" if args.draft else "contact.png"), args.every)
    print(f"\nvideo     {out.relative_to(REPO)}  ({ffprobe_duration(out):.1f}s)")
    print(f"captions  {captions.relative_to(REPO)}  ({len(cues)} cues)")
    print(f"contact   {sheet.relative_to(REPO)}  (one frame every {args.every}s — read it to review)")


def contact_sheet(video_file: Path, dest: Path, every: float) -> Path:
    frames = max(1, math.ceil(ffprobe_duration(video_file) / every))
    cols = 4
    rows = math.ceil(frames / cols)
    run(["ffmpeg", "-y", "-v", "error", "-i", video_file, "-vf",
         f"fps=1/{every},scale=480:-1,drawtext=text='%{{pts\\:hms}}':x=w-tw-8:y=h-th-8:fontsize=18:fontcolor=white:"
         f"box=1:boxcolor=black@0.6,tile={cols}x{rows}:padding=4", "-frames:v", "1", dest])
    return dest


def cmd_frames(args) -> None:
    video = EXPLAINERS / args.slug / "video"
    src = video / ("draft.mp4" if args.draft else "out.mp4")
    sheet = contact_sheet(src, video / ("draft-contact.png" if args.draft else "contact.png"), args.every)
    print(sheet.relative_to(REPO))


# ---------------------------------------------------------------- main

def main() -> None:
    parser = argparse.ArgumentParser(prog="explainer", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("setup").set_defaults(fn=cmd_setup)

    p = sub.add_parser("new")
    p.add_argument("slug")
    p.set_defaults(fn=cmd_new)

    p = sub.add_parser("voices")
    p.add_argument("--all", action="store_true", help="include non-English voices")
    p.set_defaults(fn=cmd_voices)

    p = sub.add_parser("say")
    p.add_argument("text")
    p.add_argument("--voice", default=os.environ.get("EXPLAINER_VOICE", "af_heart"))
    p.add_argument("--speed", type=float, default=1.0)
    p.add_argument("--out", default=str(Path(tempfile.gettempdir()) / "explainer-say.wav"))
    p.add_argument("--no-play", action="store_true")
    p.set_defaults(fn=cmd_say)

    p = sub.add_parser("render")
    p.add_argument("slug")
    p.add_argument("--scene", help="render one scene class only")
    p.add_argument("-q", "--quality", choices=QUALITY, help="l=480p15 m=720p30 h=1080p60 (default) k=4K")
    p.add_argument("--draft", action="store_true", help="silent estimated narration, low quality")
    p.add_argument("--every", type=float, default=4.0, help="contact sheet: seconds between frames")
    p.set_defaults(fn=cmd_render)

    p = sub.add_parser("frames")
    p.add_argument("slug")
    p.add_argument("--draft", action="store_true")
    p.add_argument("--every", type=float, default=4.0)
    p.set_defaults(fn=cmd_frames)

    args = parser.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
