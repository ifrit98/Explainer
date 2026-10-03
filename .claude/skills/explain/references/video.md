# Animated explainer mode

Create an animated explainer when the subject depends on dynamic change: movement, time, transformation, emergence, an algorithm executing, geometry changing, a signal propagating, data flowing, or repeated iteration.

Do not make a narrated slide deck.

## 1. Visual language

Use the visual language of high-quality mathematical and scientific explanation:

- Persistent visual objects.
- Spatial reasoning.
- Transformations, not slide changes.
- Narration synchronized with visuals.
- Minimal on-screen text.
- Visual emphasis on the object being discussed.
- Deliberate pacing.
- Progressive construction of complexity.

Every scene must answer one specific conceptual question.

## 2. Pre-production (write these before any rendering code)

Save to `explainers/<slug>/video/storyboard.md`:

1. Learning objective.
2. Conceptual sequence (from `model.md` dependencies and causal chain).
3. Storyboard: one entry per scene, with the question the scene answers.
4. Narration script (STE-80; also save as `narration.txt`).
5. Visual-object inventory: each object, the scene where it first appears, and the scenes where it persists.
6. Animation plan: the transformation in each scene.
7. Timing plan.
8. Rendering plan: tool per scene.

Rules:

- Introduce no object before the viewer needs it.
- Keep important objects visible across scenes.
- Transform existing objects. Do not replace the entire frame.
- Synchronize each narration statement with the visual evidence for that statement.

## 3. Production pipeline

```text
model.md → storyboard
              ├→ narration.txt → TTS → audio/ → timestamps
              └→ scene model  → Manim / HTML / SVG → scenes/
                                   │
                       timeline (visual cues timed to audio)
                                   ↓
                         render → captions (.srt) → out.mp4 (FFmpeg)
```

## 4. Tools

Prefer deterministic animation systems for technical content.

| Tool | Use for | How to run here |
|---|---|---|
| Manim (Community) | Mathematics, geometry, scientific diagrams | Not installed. Try `uvx --from manim manim -qm scene.py SceneName`. Manim needs Cairo and Pango (`brew install cairo pango`); ask before you install system packages. |
| SVG / Canvas / WebGL | Data-driven or browser-native animation | Render frames with Playwright, or record the page. |
| matplotlib (`FuncAnimation`) | Animated plots | `uv run --with matplotlib` |
| FFmpeg | Composition, audio mux, captions, final encode | Installed. |

## 5. Narration

Choose the first option that works:

1. A configured high-quality TTS provider (check for an API key in the environment; ask the user before you use a paid service).
2. Local TTS: macOS `say -v <voice> -o line.aiff "text"` (installed). List voices with `say -v '?'`.
3. No audio: render the video with captions and deliver the narration script.

Narration is optional. Do not block the visual artifact on narration.

## 6. Timing

- Generate one audio clip per narration statement. Measure each clip with `ffprobe` to get timestamps.
- Time visual transitions to the narration. Do not force narration into arbitrary scene lengths.
- Build the `.srt` captions from the same timestamps.

## 7. Verify and deliver

1. Extract key frames with `ffmpeg -ss <t> -frames:v 1` and look at them.
2. Check that each narration statement plays while its visual evidence is on screen.
3. Run the seven understanding questions from `CLAUDE.md` §7.
4. Deliver `out.mp4`, `captions.srt`, and `narration.txt`.
