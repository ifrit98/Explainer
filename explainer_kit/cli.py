"""explainer — CLI for the explanation compiler.

  explainer setup                       download the Kokoro voice, check the toolchain
  explainer new <slug> [--stage 1 2 3 4] scaffold explainers/<slug>/: model + chosen renderings (default: 4)
  explainer check [slug ...]            renderings vs model.yaml: numbers, claims, terms, stale pages
  explainer check --diagrams            also render every Mermaid block once (Node or mmdc)
  explainer sync <slug>                 write model values and the web toolkit into the slug's HTML pages
  explainer render <slug> [--draft]     render the video: voice, captions, chapters, timeline, contact sheet
  explainer review <slug>               review sheet: a frame at each line, bookmark, and predict pause
  explainer probe <slug>                prompt for a fresh agent that reads model.md and lists what it omits
  explainer quiz <slug> --rendering R   blind-test prompt for one rendering (R: prose, diagram, html, video)
  explainer quiz <slug> --rubric        expected answers, for scoring the blind test
  explainer coldread <slug> --rendering R  first-viewing read: every reference a reader meets before it is
                                        introduced, in order (R: narrative, prose, diagram, html, video)
  explainer voices / say "<text>"       list voices / audition a line
  explainer frames <slug>               rebuild the contact sheet

Run from any folder inside a project; explainers live in <project>/explainers/<slug>/.
In the Explainer repo, prefix commands with `uv run`.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

from explainer_kit.paths import TEMPLATES, display, explainer_dir, explainers_dir, latex_bin, model_dir, project_root

MODEL_URL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/"
STAGE_FILES = {
    1: [("explanation.md", "explanation.md")],
    2: [("diagram.md", "diagram.md")],
    3: [("index.html", "index.html")],
    4: [("video/storyboard.md", "storyboard.md"), ("video/scene.py", "scene.py")],
}


def cmd_setup(args) -> None:
    dest_dir = model_dir()
    dest_dir.mkdir(parents=True, exist_ok=True)
    for name in ("kokoro-v1.0.onnx", "voices-v1.0.bin"):
        dest = dest_dir / name
        if dest.exists():
            print(f"ok       {dest}")
            continue
        print(f"download {name} → {dest_dir} …", flush=True)
        urllib.request.urlretrieve(MODEL_URL + name, dest)
    tex = latex_bin()
    for tool, why in [("ffmpeg", "required: encode and mux"), ("ffprobe", "required: timing"),
                      ("sox", "optional: global_speed changes")]:
        print(f"{'ok' if shutil.which(tool) else 'missing':8} {tool:8} {why}")
    print(f"{'ok' if tex else 'missing':8} {'latex':8} optional: MathTex / Tex{f'  ({tex})' if tex else ''}")
    if not tex:
        print("\nMathTex needs LaTeX. A user-level install (no password):\n"
              "  curl -sL https://yihui.org/tinytex/install-bin-unix.sh -o tinytex.sh && sh tinytex.sh \"\" --no-path\n"
              "  ~/Library/TinyTeX/bin/*/tlmgr install standalone preview dvisvgm babel-english   # Linux: ~/.TinyTeX/...")
    print(f"\nproject   {project_root()}")


def cmd_new(args) -> None:
    slug = args.slug
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug):
        sys.exit("slug must be kebab-case, for example: attention-heads")
    root = explainer_dir(slug)
    class_name = "".join(part.capitalize() for part in slug.split("-"))
    files = [("model.md", "model.md"), ("model.yaml", "model.yaml"), ("narrative.md", "narrative.md")]
    for stage in sorted(set(args.stage)):
        files += STAGE_FILES[stage]
    for rel, template in files:
        dest = root / rel
        if dest.exists():
            print(f"keep     {display(dest)}")
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        text = (TEMPLATES / template).read_text().replace("{{ClassName}}", class_name).replace("{{slug}}", slug)
        dest.write_text(text)
        print(f"create   {display(dest)}")
    if 3 in args.stage:
        from explainer_kit.model import sync
        sync(root)


def cmd_check(args) -> None:
    from explainer_kit.model import check

    folders = [explainer_dir(s) for s in args.slugs] or sorted(
        d for d in explainers_dir().iterdir() if d.is_dir() and (d / "model.md").exists())
    failed = 0
    for folder in folders:
        rep = check(folder)
        print(f"{'ok  ' if rep.ok else 'FAIL'}  {rep.slug}")
        for p in rep.problems:
            print(f"      ✗ {p}")
        if args.verbose:
            for n in rep.notes:
                print(f"      · {n}")
        failed += not rep.ok
    if args.diagrams:
        failed += check_diagrams(folders)
    if failed:
        sys.exit(f"\n{failed} explainer(s) failed the check")


def check_diagrams(folders) -> int:
    from explainer_kit.diagrams import mermaid_blocks, validate

    failed = 0
    for folder in folders:
        blocks = mermaid_blocks(folder)
        if not blocks:
            continue
        try:
            failures = validate(blocks)
        except FileNotFoundError as e:
            sys.exit(f"--diagrams: {e}")
        print(f"{'ok  ' if not failures else 'FAIL'}  {folder.name}: {len(blocks)} Mermaid block(s)")
        for block, error in failures:
            print(f"      ✗ {display(block.path)}:{block.line}: {error}")
        failed += bool(failures)
    return failed


def cmd_sync(args) -> None:
    from explainer_kit.model import sync

    changed = sync(explainer_dir(args.slug))
    print("\n".join(f"updated  {display(p)}" for p in changed) or "up to date")


def cmd_render(args) -> None:
    from explainer_kit.render import render

    render(args.slug, scene=args.scene, quality=args.quality, draft=args.draft, every=args.every)
    if args.review:
        from explainer_kit.review import review_sheet
        review_sheet(args.slug, draft=args.draft)


def cmd_review(args) -> None:
    from explainer_kit.review import review_sheet

    review_sheet(args.slug, draft=args.draft)


def cmd_quiz(args) -> None:
    from explainer_kit.review import quiz_prompt, quiz_rubric

    if args.rubric:
        print(quiz_rubric(args.slug))
    elif args.rendering:
        print(quiz_prompt(args.slug, args.rendering))
    else:
        sys.exit("give --rendering {prose,diagram,html,video} or --rubric")


def cmd_coldread(args) -> None:
    from explainer_kit.review import COLDREAD_PASS, coldread_prompt

    print(COLDREAD_PASS if args.rubric else coldread_prompt(args.slug, args.rendering))


def cmd_probe(args) -> None:
    from explainer_kit.review import probe_prompt

    print(probe_prompt(args.slug))


def cmd_frames(args) -> None:
    from explainer_kit.render import contact_sheet

    video = explainer_dir(args.slug) / "video"
    src = video / ("draft.mp4" if args.draft else "out.mp4")
    print(display(contact_sheet(src, video / ("draft-contact.png" if args.draft else "contact.png"), args.every)))


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


def main() -> None:
    parser = argparse.ArgumentParser(prog="explainer", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", help="project root (default: nearest folder with explainers/ or .git)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("setup", help="download the voice model, check tools").set_defaults(fn=cmd_setup)

    p = sub.add_parser("new", help="scaffold an explainer")
    p.add_argument("slug")
    p.add_argument("--stage", type=int, nargs="+", choices=[1, 2, 3, 4], default=[4],
                   help="renderings to scaffold: 1 prose, 2 diagram, 3 interactive, 4 video (default: 4)")
    p.set_defaults(fn=cmd_new)

    p = sub.add_parser("check", help="check renderings against model.yaml")
    p.add_argument("slugs", nargs="*")
    p.add_argument("-v", "--verbose", action="store_true")
    p.add_argument("--diagrams", action="store_true", help="also render every Mermaid block (needs Node or mmdc)")
    p.set_defaults(fn=cmd_check)

    p = sub.add_parser("sync", help="write model values and toolkit into HTML pages")
    p.add_argument("slug")
    p.set_defaults(fn=cmd_sync)

    p = sub.add_parser("render", help="render the video")
    p.add_argument("slug")
    p.add_argument("--scene", help="render one scene class only")
    p.add_argument("-q", "--quality", choices=["l", "m", "h", "k"], help="l=480p15 m=720p30 h=1080p60 (default) k=4K")
    p.add_argument("--draft", action="store_true", help="silent estimated narration, low quality")
    p.add_argument("--every", type=float, default=4.0, help="contact sheet: seconds between frames")
    p.add_argument("--review", action="store_true", help="also build the review sheet")
    p.set_defaults(fn=cmd_render)

    p = sub.add_parser("review", help="frame-by-event review sheet")
    p.add_argument("slug")
    p.add_argument("--draft", action="store_true")
    p.set_defaults(fn=cmd_review)

    p = sub.add_parser("quiz", help="blind understanding test")
    p.add_argument("slug")
    p.add_argument("--rendering", choices=["prose", "diagram", "html", "video"])
    p.add_argument("--rubric", action="store_true")
    p.set_defaults(fn=cmd_quiz)

    p = sub.add_parser("coldread", help="first-viewing read: unintroduced references, in order")
    p.add_argument("slug")
    p.add_argument("--rendering", choices=["narrative", "prose", "diagram", "html", "video"], default="narrative")
    p.add_argument("--rubric", action="store_true", help="print the pass rule")
    p.set_defaults(fn=cmd_coldread)

    p = sub.add_parser("probe", help="gap-finding prompt for the model, before rendering")
    p.add_argument("slug")
    p.set_defaults(fn=cmd_probe)

    p = sub.add_parser("frames", help="rebuild the contact sheet")
    p.add_argument("slug")
    p.add_argument("--draft", action="store_true")
    p.add_argument("--every", type=float, default=4.0)
    p.set_defaults(fn=cmd_frames)

    p = sub.add_parser("voices", help="list Kokoro voices")
    p.add_argument("--all", action="store_true", help="include non-English voices")
    p.set_defaults(fn=cmd_voices)

    p = sub.add_parser("say", help="audition a line")
    p.add_argument("text")
    p.add_argument("--voice", default=os.environ.get("EXPLAINER_VOICE", "af_heart"))
    p.add_argument("--speed", type=float, default=1.0)
    p.add_argument("--out", default=str(Path(tempfile.gettempdir()) / "explainer-say.wav"))
    p.add_argument("--no-play", action="store_true")
    p.set_defaults(fn=cmd_say)

    args = parser.parse_args()
    if args.root:
        os.environ["EXPLAINER_ROOT"] = args.root
    args.fn(args)


if __name__ == "__main__":
    main()
