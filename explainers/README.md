# Examples

Each folder holds one `model.md` (the source of truth) and the renderings compiled from it. Every model ends with a **representation decision** that explains the chosen stage.

| Example | Stage | Why this stage | Files |
|---|---|---|---|
| [git-bisect](git-bisect/) | 1 · prose | A linear procedure with one loop. Numbered steps carry all of it. | [explanation](git-bisect/explanation.md) |
| [git-objects](git-objects/) | 2 · diagram | Five object types and four pointer relations, held at once. Nothing moves. | [diagram](git-objects/diagram.md) |
| [cdn-request](cdn-request/) | 3 · interactive | Two distances and a cache state set the result; the reader compares three paths. Built from the Stage 3 template. | [page (live)](https://ifrit98.github.io/Explainer/explainers/cdn-request/) |
| [softmax-temperature](softmax-temperature/) | 1 → 4 · all | **Compiler demo.** One model rendered at every stage. Normal routing picks Stage 3. | [prose](softmax-temperature/explanation.md) · [diagrams](softmax-temperature/diagram.md) · [page (live)](https://ifrit98.github.io/Explainer/explainers/softmax-temperature/) · [video](softmax-temperature/video/out.mp4) · [blind test](softmax-temperature/review/understanding.md) |
| [odd-squares](odd-squares/) | 4 · video (proof) | The proof is a transformation: each odd number is an L that wraps the square. | [video](odd-squares/video/out.mp4) · [scene](odd-squares/video/scene.py) |
| [dijkstra](dijkstra/) | 4 · video (algorithm) | An algorithm that runs: estimates change and nodes settle in order on a fixed graph. | [video](dijkstra/video/out.mp4) · [scene](dijkstra/video/scene.py) · [blind test](dijkstra/review/understanding.md) |
| [ste-80](ste-80/) | 4 · video | The meaning is in the transformation: which words survive each rewrite. | [video](ste-80/video/out.mp4) · [scene](ste-80/video/scene.py) |

Every example passes `explainer check` (CI runs it). Videos with a predict pause: softmax-temperature, odd-squares, dijkstra.

The interactive pages and the videos are live at [ifrit98.github.io/Explainer](https://ifrit98.github.io/Explainer/). Locally, serve the repo with `python3 -m http.server` and open the folder.

## Layout of one example

```text
<slug>/
  model.md          semantic model: entities, causal chain, quantities, epistemic status, decision
  model.yaml        values the renderings must agree with, plus quiz items for the blind test
  explanation.md    Stage 1: STE-80 prose
  diagram.md        Stage 2: Mermaid diagrams (GitHub renders them)
  index.html        Stage 3: self-contained interactive page
  video/
    storyboard.md   Stage 4: objective, scenes, bookmarks, object inventory
    scene.py        Manim + explainer_kit
    out.mp4         rendered video (captions as a soft track, chapters at predict pauses)
    timeline.json   narration lines, bookmarks, predict pauses
    review.png      one frame per line and bookmark
    captions.srt
```

## Add an example

1. `explainer new <slug> --stage …`, or ask Claude Code: `/explainer:explain <topic>`.
2. Fill `model.md` and `model.yaml` first. Every rendering must use their terms and numbers.
3. Render only the stages that the representation decision justifies.
4. Run `explainer check`, and the [understanding test](../docs/concepts.md#the-understanding-test) (the `verify` skill).
