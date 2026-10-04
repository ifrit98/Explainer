# Diagram mode

Create a diagram when a visual representation reduces cognitive load.

## 1. Decide what the diagram must communicate

Name the one relationship type that the diagram shows. Then select the diagram type.

| Relationship | Diagram type |
|---|---|
| Hierarchy | Tree |
| Process | Flowchart |
| Architecture | Component diagram |
| Causality | Causal graph |
| Sequence | Timeline or sequence diagram |
| State changes | State machine |
| Quantities | Chart (load the `dataviz` skill) |
| Spatial relationships | Annotated schematic |
| Mathematical transformation | Staged mathematical diagram |
| Competing mechanisms | Side-by-side comparison |

## 2. Rules

- Keep the first-level view understandable at a glance: about 5–9 major objects.
- Group secondary detail into nested regions or later diagrams.
- Use arrows only when their meaning is clear.
- Label arrows when the diagram has more than one relationship type.
- Do not add decorative elements that encode no information.
- Use the exact terms from `model.md`. Text and diagram must use the same words.
- Use color to encode one variable, and say what it encodes.

## 3. Choose the format

| Need | Format |
|---|---|
| Quick structure in chat | ASCII or Mermaid in a code block |
| Precise topology (a wrong arrow changes the meaning) | SVG, HTML/CSS, Mermaid, or Graphviz |
| Intuitive schematic where aesthetics matter more than exact topology | Generated image, if a generator is available |
| Chart of data | SVG or a plotting library |

Prefer deterministic, programmatic formats for technical content. Example: `database → queue → inference worker → API` must be exact, so draw it in code.

For an SVG or HTML diagram page, load the `artifact-diagramming` skill first.

## 4. Progressive diagrams

When one diagram exceeds about 9 objects, split it by level:

```text
Level 1:  Tokens → Attention → MLP → Prediction

Level 2 (Attention):
          Q ─┐
          K ─┼→ similarity → softmax → weighted sum
          V ─┘

Level 3 (similarity):  QKᵀ / √d
```

Each level expands exactly one object of the level above it.
