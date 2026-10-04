"""dijkstra — replay the run in model.yaml: settle the smallest estimate, then relax its edges.

Render:  uv run explainer render dijkstra --draft
         uv run explainer render dijkstra
"""

from manim import *

from explainer_kit import BACKGROUND, ExplainerScene, Role, label, load_model

M = load_model(__file__)
POS = {n: np.array([x, y, 0]) for n, (x, y) in M["nodes"].items()}
EDGES = {frozenset((a, b)): w for a, b, w in M["edges"]}
R = 0.38  # node radius

# Narration per settle step. Each <bookmark mark='rK'/> starts the K-th relaxation of that step.
STEPS = {
    "A": "Settle A. <bookmark mark='r0'/> From A, B is four away, <bookmark mark='r1'/> and C is two away.",
    "C": "The smallest estimate is now C, at two. Settle C. <bookmark mark='r0'/> Through C, B is two plus one: "
         "three. That is shorter than four, so B becomes three. <bookmark mark='r1'/> D becomes ten, "
         "<bookmark mark='r2'/> and E becomes twelve.",
    "B": "Settle B, at three. <bookmark mark='r0'/> Through B, D is three plus five: eight. "
         "Eight is shorter than ten.",
    "D": "Settle D, at eight. <bookmark mark='r0'/> E becomes ten, <bookmark mark='r1'/> and F becomes fourteen.",
    "E": "E, at ten. It is the smallest unsettled estimate. <bookmark mark='r0'/> Through E, F becomes thirteen.",
    "F": "Settle F, at thirteen. Every node is settled.",
}


class Dijkstra(ExplainerScene):
    voice = "af_heart"

    def construct(self):
        # graph
        nodes = {n: VGroup(Circle(radius=R, color=Role.ENTITY, stroke_width=3).set_fill(BACKGROUND, 1),
                           label(n, size=30)).move_to(p) for n, p in POS.items()}
        edge_lines, weights = {}, []
        for key, w in EDGES.items():
            a, b = sorted(key)
            direction = (POS[b] - POS[a]) / np.linalg.norm(POS[b] - POS[a])
            line = Line(POS[a] + direction * R, POS[b] - direction * R, color=Role.RELATION, stroke_width=3)
            normal = np.array([-direction[1], direction[0], 0])
            weights.append(label(str(w), size=24, color=Role.RELATION).move_to(line.get_center() + normal * 0.28))
            edge_lines[key] = line
        # tags sit on the outside of the graph, so edges into a node never run through its tag
        tags = {n: label("0" if n == M["start"] else "∞", size=26, color=Role.QUANTITY)
                .next_to(nodes[n], UP if POS[n][1] >= 0 else DOWN, buff=0.12) for n in POS}

        with self.voiceover(text="Dijkstra's algorithm finds the shortest distance from one start node to every "
                                 "other node. The numbers on the edges are lengths. <bookmark mark='rule'/> "
                                 "Every length must be zero or more."):
            self.play(LaggedStart(*[GrowFromCenter(v) for v in nodes.values()], lag_ratio=0.1),
                      LaggedStart(*[Create(l) for l in edge_lines.values()], lag_ratio=0.05), run_time=2)
            self.play(FadeIn(VGroup(*weights)))
            self.wait_until_bookmark("rule")
        with self.voiceover(text="At the start, A has distance zero. Every other node has distance infinity. "
                                 "<bookmark mark='loop'/> Then repeat two steps. First, settle the unsettled node "
                                 "with the smallest distance. Second, update its neighbors: if a path through it "
                                 "is shorter, keep the shorter distance."):
            self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.1) for t in tags.values()], lag_ratio=0.1))
            self.wait_until_bookmark("loop")
            rule = VGroup(label("1  settle the smallest estimate", size=24),
                          label("2  relax its edges", size=24)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            rule.to_corner(DR, buff=0.5)
            self.play(FadeIn(rule))

        # replay the run
        parent: dict[str, str] = {}
        settled: set[str] = set()
        for step in M["run"]:
            u = step["settle"]
            if u == "E":
                self.predict("D is settled. Which node is settled next, and at what distance?")
            with self.voiceover(text=STEPS[u]):
                ring = Circle(radius=R + 0.08, color=Role.FOCUS, stroke_width=5).move_to(POS[u])
                self.play(Create(ring), nodes[u][0].animate.set_fill(Role.GOOD, 0.35).set_stroke(Role.GOOD),
                          run_time=0.7)
                settled.add(u)
                for k, (v, d) in enumerate(step["relax"]):
                    self.wait_until_bookmark(f"r{k}")
                    edge = edge_lines[frozenset((u, v))]
                    new_tag = label(str(d), size=26, color=Role.QUANTITY).move_to(tags[v])
                    improves_from = parent.get(v)
                    anims = [ShowPassingFlash(edge.copy().set_stroke(Role.FOCUS, 8), time_width=0.6),
                             Transform(tags[v], new_tag)]
                    if improves_from:  # the old best edge is no longer part of the tree
                        anims.append(edge_lines[frozenset((improves_from, v))].animate.set_stroke(Role.RELATION, 3))
                    anims.append(edge.animate.set_stroke(Role.FOCUS, 5))
                    self.play(*anims, run_time=0.9)
                    parent[v] = u
                self.play(FadeOut(ring), run_time=0.4)

        # why it works, then the tree
        with self.voiceover(text="Why is a settled distance final? Any other path must leave the settled nodes "
                                 "through an unsettled node, which is already at least as far. With no negative "
                                 "lengths, the rest of that path cannot make it shorter."):
            self.play(Indicate(rule, color=Role.FOCUS))
        tree = [frozenset((v, p)) for v, p in parent.items()]
        path = M["path_to_F"]
        path_edges = [frozenset(pair) for pair in zip(path, path[1:])]
        with self.voiceover(text="The edges that gave each final distance form the shortest-path tree. "
                                 "<bookmark mark='path'/> The shortest path to F is A, C, B, D, E, F. "
                                 "Its length is thirteen."):
            self.play(*[l.animate.set_stroke(Role.MUTED, 2) for k, l in edge_lines.items() if k not in tree],
                      *[edge_lines[k].animate.set_stroke(Role.GOOD, 5) for k in tree])
            self.wait_until_bookmark("path")
            self.play(LaggedStart(*[ShowPassingFlash(edge_lines[k].copy().set_stroke(Role.FOCUS, 10), time_width=0.8)
                                    for k in path_edges], lag_ratio=0.5), run_time=2.5)
        self.wait(1.5)
