# Examples

Each folder holds one `model.md` (the source of truth) and the renderings compiled from it. Every model ends with a **representation decision** that explains the chosen stage.

| Example | Stage | Why this stage | Files |
|---|---|---|---|
| [git-bisect](git-bisect/) | 1 · prose | A linear procedure with one loop. Numbered steps carry all of it. | [explanation](git-bisect/explanation.md) |
| [git-objects](git-objects/) | 2 · diagram | Five object types and four pointer relations, held at once. Nothing moves. | [diagram](git-objects/diagram.md) |
| [softmax-temperature](softmax-temperature/) | 1 → 4 · all | **Compiler demo.** One model rendered at every stage. Normal routing picks Stage 3. | [prose](softmax-temperature/explanation.md) · [diagrams](softmax-temperature/diagram.md) · [interactive](softmax-temperature/index.html) · [video](softmax-temperature/video/out.mp4) |
| [ste-80](ste-80/) | 4 · video | The meaning is in the transformation: which words survive each rewrite. | [video](ste-80/video/out.mp4) · [scene](ste-80/video/scene.py) |

The interactive page is a single HTML file. Download it and open it in a browser, or serve the repo with `python3 -m http.server`.

## Layout of one example

```text
<slug>/
  model.md          semantic model: entities, causal chain, quantities, epistemic status, decision
  explanation.md    Stage 1: STE-80 prose
  diagram.md        Stage 2: Mermaid diagrams (GitHub renders them)
  index.html        Stage 3: self-contained interactive page
  video/
    storyboard.md   Stage 4: objective, scenes, bookmarks, object inventory
    scene.py        Manim + explainer_kit
    out.mp4         rendered video (captions as a soft track)
    captions.srt
```

## Add an example

1. `uv run explainer new <slug>`, or ask Claude Code: `/explain <topic>`.
2. Fill `model.md` first. Every rendering must use its terms and numbers.
3. Render only the stages that the representation decision justifies.
4. Check the result against the [understanding test](../docs/concepts.md#the-understanding-test).
