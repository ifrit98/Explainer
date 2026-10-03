# Softmax temperature — Stage 2: diagrams

> Rendered from [`model.md`](model.md). Other renderings: [prose](explanation.md) · [interactive](index.html) · [video](video/out.mp4).

## Level 1 — Where temperature acts in one decoding step

```mermaid
flowchart LR
    M[Model] -->|one logit per token| Z["Logits z<br/>cat 2.0 · dog 1.0 · fox 0.5 · owl −1.0"]
    Z -->|"divide by T"| S["Scaled logits z/T"]
    S -->|"exp, then normalize"| P["Probabilities p<br/>sum = 1"]
    P -->|"pick at random"| X[Next token]
    T((Temperature T)) -.->|controls the gaps| S
```

## Level 2 — What T does to the distribution (same logits, three temperatures)

```mermaid
---
config:
  xyChart:
    height: 260
---
xychart-beta
    title "T = 0.5 — sharp (entropy 0.78 bits)"
    x-axis [cat, dog, fox, owl]
    y-axis "probability" 0 --> 1
    bar [0.842, 0.114, 0.042, 0.002]
```

```mermaid
---
config:
  xyChart:
    height: 260
---
xychart-beta
    title "T = 1.0 — the model's own distribution (1.46 bits)"
    x-axis [cat, dog, fox, owl]
    y-axis "probability" 0 --> 1
    bar [0.609, 0.224, 0.136, 0.030]
```

```mermaid
---
config:
  xyChart:
    height: 260
---
xychart-beta
    title "T = 2.0 — flat (1.82 bits)"
    x-axis [cat, dog, fox, owl]
    y-axis "probability" 0 --> 1
    bar [0.434, 0.263, 0.205, 0.097]
```

The ranking is the same in all three charts. Only the spread changes.

## Level 3 — Why: the causal chain

```mermaid
flowchart LR
    A["T increases"] --> B["Gaps between<br/>scaled logits shrink"]
    B --> C["Ratios pᵢ / pⱼ = exp(gap / T)<br/>move toward 1"]
    C --> D["Distribution flattens<br/>(entropy rises)"]
    D --> E["Samples vary more"]
```

## Limit states

```mermaid
stateDiagram-v2
    direction LR
    Greedy: T → 0<br/>greedy — top token only
    Native: T = 1<br/>plain softmax
    Uniform: T → ∞<br/>all tokens equal
    Greedy --> Native: raise T
    Native --> Uniform: raise T
    Uniform --> Native: lower T
    Native --> Greedy: lower T
```
