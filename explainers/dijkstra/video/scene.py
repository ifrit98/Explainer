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
         "three. That is shorter than four, so B becomes three. <bookmark mark='r1'/> D becomes two plus eight: ten. "
         "<bookmark mark='r2'/> E becomes two plus ten: twelve.",
    "B": "Now relax B's edges. <bookmark mark='r0'/> Through B, D is three plus five: eight. "
         "Eight is shorter than ten: the bound of ten held only for paths that leave A and C at D.",
    "D": "D, at eight, is now the smallest estimate. Settle D. <bookmark mark='r0'/> E becomes eight plus two: ten. "
         "<bookmark mark='r1'/> F becomes eight plus six: fourteen.",
    "E": "E, at ten. It is the smallest unsettled estimate. <bookmark mark='r0'/> Through E, F becomes ten plus "
         "three: thirteen. That is shorter than fourteen.",
    "F": "Settle F, at thirteen. Every node is settled.",
}


class Dijkstra(ExplainerScene):
    voice = "af_heart"

    def why_smallest(self, edge_lines):
        """Right after C improves B from 4 to 3: settling in the order nodes are reached would have been wrong."""
        a, b, c = M["bfs_counterexample"]["B_first"], M["bfs_counterexample"]["B_true"], M["bfs_counterexample"]["via_C"]
        with self.voiceover(text="This is why the algorithm settles the smallest estimate, and not the first node "
                                 "it reached. <bookmark mark='w'/> Had it settled B at four, as soon as A reached it, "
                                 "the answer would be wrong: <bookmark mark='via'/> the path through C is three."):
            self.wait_until_bookmark("w")
            self.claim("why-smallest")
            self.play(ShowPassingFlash(edge_lines[frozenset("AB")].copy().set_stroke(Role.BAD, 10), time_width=0.8),
                      run_time=1.2)
            self.wait_until_bookmark("via")
            self.play(LaggedStart(ShowPassingFlash(edge_lines[frozenset("AC")].copy().set_stroke(Role.GOOD, 10), time_width=0.8),
                                  ShowPassingFlash(edge_lines[frozenset("BC")].copy().set_stroke(Role.GOOD, 10), time_width=0.8),
                                  lag_ratio=0.6), run_time=1.6)
        self.wait(1.2)

    def finality(self, nodes, tags, edge_lines, settle):
        """B is the smallest unsettled estimate (3): why no later path can beat it, before B settles.
        The settled region is A and C only; B is the candidate outside it."""
        region = DashedVMobject(SurroundingRectangle(VGroup(nodes["A"], nodes["C"], tags["A"], tags["C"]),
                                                     color=Role.GOOD, buff=0.25, corner_radius=0.2), num_dashes=40)
        region_label = label("settled", size=22, color=Role.GOOD).next_to(region, DOWN, buff=0.1).align_to(region, LEFT)
        with self.voiceover(text="B has the smallest estimate, three. Can a path found later still beat three?"):
            self.play(Create(region), FadeIn(region_label))
        self.wait(0.6)
        exit_edges = [frozenset("AB"), frozenset("BC"), frozenset("CD"), frozenset("CE")]
        with self.voiceover(text="Any path to B starts in the settled nodes, A and C. <bookmark mark='leave'/> "
                                 "Follow it to the first node outside them. If that node is B, B's estimate already "
                                 "counts the path: three. <bookmark mark='de'/> If it is D or E, the path so far "
                                 "costs at least D's estimate, ten, or E's, twelve, because A and C have relaxed "
                                 "their edges. <bookmark mark='grow'/> No length is negative, so the rest of the "
                                 "path can only add."):
            self.wait_until_bookmark("leave")
            self.play(LaggedStart(*[ShowPassingFlash(edge_lines[k].copy().set_stroke(Role.FOCUS, 10), time_width=0.8)
                                    for k in exit_edges], lag_ratio=0.3), run_time=1.8)
            self.wait_until_bookmark("de")
            self.play(Indicate(tags["D"], color=Role.FOCUS, scale_factor=1.4),
                      Indicate(tags["E"], color=Role.FOCUS, scale_factor=1.4), run_time=1.0)
            self.wait_until_bookmark("grow")
            at_least = label("first step out at D or E: ≥ 10 > 3", size=26, color=Role.FOCUS).to_edge(UP, buff=0.35)
            self.play(FadeIn(at_least, shift=UP * 0.1))
        with self.voiceover(text="So no other path can cost less than three. <bookmark mark='final'/> Settle B. "
                                 "Its estimate never changes again."):
            self.wait_until_bookmark("final")
            self.claim("guarantee-final")
            self.play(*settle, run_time=0.7)
            self.play(Indicate(tags["B"], color=Role.GOOD, scale_factor=1.5), run_time=1.0)
        self.wait(1.5)
        self.play(FadeOut(region), FadeOut(region_label), FadeOut(at_least), run_time=0.5)

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
                                 "other node. Here the start node is A. The numbers on the edges are lengths, and "
                                 "each edge works in both directions. <bookmark mark='rule'/> "
                                 "Every length must be zero or more."):
            self.play(LaggedStart(*[GrowFromCenter(v) for v in nodes.values()], lag_ratio=0.1),
                      LaggedStart(*[Create(l) for l in edge_lines.values()], lag_ratio=0.05), run_time=2)
            self.play(FadeIn(VGroup(*weights)))
            self.wait_until_bookmark("rule")
            self.play(FadeIn(label("every length ≥ 0", size=22, color=Role.MUTED).to_corner(UR, buff=0.4)))
        with self.voiceover(text="Each node has an estimate: the shortest length found so far. At the start, A has "
                                 "estimate zero. Every other node has estimate infinity: no path found yet. "
                                 "<bookmark mark='loop'/> "
                                 "Then repeat two steps. First, settle the unsettled node with the smallest "
                                 "estimate. A settled estimate is final: it is the node's distance. We check why below. Second, relax its edges. "
                                 "<bookmark mark='relax'/> To relax an edge, check whether the path through the "
                                 "settled node is shorter. <bookmark mark='keep'/> If it is, keep the shorter "
                                 "estimate, and remember where it came from."):
            self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.1) for t in tags.values()], lag_ratio=0.1))
            self.wait_until_bookmark("loop")
            rule = VGroup(label("1  settle the smallest estimate", size=24),
                          label("2  relax its edges", size=24)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            rule.to_corner(DR, buff=0.5)
            self.play(FadeIn(rule))
            self.wait_until_bookmark("relax")
            self.claim("definition-relax")
            self.play(Indicate(rule[1], color=Role.FOCUS))
            test = label("estimate(u) + length < estimate(v) ?", size=22, color=Role.QUANTITY)
            keep = label("yes: keep it, remember u", size=22, color=Role.GOOD)
            VGroup(test, keep).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(rule, UP, buff=0.3, aligned_edge=LEFT)
            self.play(FadeIn(test, shift=UP * 0.1))
            self.wait_until_bookmark("keep")
            self.play(FadeIn(keep, shift=UP * 0.1))
        self.wait(1.2)
        self.play(FadeOut(test), FadeOut(keep), run_time=0.4)

        # replay the run
        parent: dict[str, str] = {}
        settled: set[str] = set()
        for step in M["run"]:
            u = step["settle"]
            if u == "E":
                self.predict("D is settled. Which node is settled next, and at what distance?")
            ring = Circle(radius=R + 0.08, color=Role.FOCUS, stroke_width=5).move_to(POS[u])
            settle = [Create(ring), nodes[u][0].animate.set_fill(Role.GOOD, 0.35).set_stroke(Role.GOOD)]
            if u == "B":  # show finality at the moment of settling, before B relaxes its edges
                self.play(Create(ring), run_time=0.5)
                self.finality(nodes, tags, edge_lines, settle[1:])
            with self.voiceover(text=STEPS[u]):
                if u != "B":
                    self.play(*settle, run_time=0.7)
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
            if u == "C":
                self.why_smallest(edge_lines)

        # read the path back through the predecessors, then the tree
        tree = [frozenset((v, p)) for v, p in parent.items()]
        path = M["path_to_F"]
        path_edges = [frozenset(pair) for pair in zip(path, path[1:])]
        with self.voiceover(text="Each node remembers the neighbor that gave its final distance. "
                                 "<bookmark mark='back'/> Follow them back from F: E, D, B, C, and then A. "
                                 "<bookmark mark='path'/> So the shortest path to F is A, C, B, D, E, F. "
                                 "Its length is thirteen."):
            self.play(*[l.animate.set_stroke(Role.MUTED, 2) for k, l in edge_lines.items() if k not in tree],
                      *[edge_lines[k].animate.set_stroke(Role.GOOD, 5) for k in tree])
            self.wait_until_bookmark("back")
            self.claim("mechanism-path")
            self.play(LaggedStart(*[Indicate(nodes[n], color=Role.FOCUS) for n in reversed(path)], lag_ratio=0.35),
                      run_time=2.5)
            self.wait_until_bookmark("path")
            self.play(LaggedStart(*[ShowPassingFlash(edge_lines[k].copy().set_stroke(Role.FOCUS, 10), time_width=0.8)
                                    for k in path_edges], lag_ratio=0.5), run_time=2.5)
        self.wait(1.5)


class NegativeEdge(ExplainerScene):
    """Chapter 2: one negative edge breaks the guarantee (directed graph from model.yaml)."""

    voice = "af_heart"

    def construct(self):
        N = M["negative_example"]
        pos = {"A": np.array([-3.2, 0, 0]), "B": np.array([1.6, 1.7, 0]), "C": np.array([1.6, -1.7, 0])}
        nodes = {n: VGroup(Circle(radius=R, color=Role.ENTITY, stroke_width=3).set_fill(BACKGROUND, 1),
                           label(n, size=30)).move_to(p) for n, p in pos.items()}
        arrows, weights = [], []
        for a, b, w in N["edges"]:
            arrow = Arrow(pos[a], pos[b], buff=R + 0.05, color=Role.BAD if w < 0 else Role.RELATION,
                          stroke_width=3, max_tip_length_to_length_ratio=0.12)
            normal = np.array([-(pos[b] - pos[a])[1], (pos[b] - pos[a])[0], 0])
            normal = normal / np.linalg.norm(normal)
            weights.append(label(f"{w:g}", size=26, color=Role.BAD if w < 0 else Role.RELATION)
                           .move_to(arrow.get_center() + normal * 0.35))
            arrows.append(arrow)
        tags = {"A": label("0", size=26, color=Role.QUANTITY).next_to(nodes["A"], LEFT, buff=0.15),
                "B": label("∞", size=26, color=Role.QUANTITY).next_to(nodes["B"], RIGHT, buff=0.15),
                "C": label("∞", size=26, color=Role.QUANTITY).next_to(nodes["C"], RIGHT, buff=0.15)}
        title = label("one negative edge", size=28, color=Role.BAD).to_edge(UP, buff=0.5)

        with self.voiceover(text="Why must every length be zero or more? <bookmark mark='g'/> Here is a small graph "
                                 "with one negative edge, from C to B, of length minus two. Here each edge works in one direction only."):
            self.wait_until_bookmark("g")
            self.play(FadeIn(title), *[GrowFromCenter(v) for v in nodes.values()], *[GrowArrow(a) for a in arrows])
            self.play(FadeIn(VGroup(*weights)), FadeIn(VGroup(*tags.values())))
        with self.voiceover(text="Settle A. From A, B is two away, <bookmark mark='c'/> and C is three away."):
            self.play(nodes["A"][0].animate.set_fill(Role.GOOD, 0.35).set_stroke(Role.GOOD), run_time=0.6)
            self.play(Transform(tags["B"], label(str(N["edges"][0][2]), size=26, color=Role.QUANTITY).move_to(tags["B"])))
            self.wait_until_bookmark("c")
            self.play(Transform(tags["C"], label(str(N["edges"][1][2]), size=26, color=Role.QUANTITY).move_to(tags["C"])))
        with self.voiceover(text="B has the smallest estimate, so the algorithm settles B at two. It is now final."):
            self.play(nodes["B"][0].animate.set_fill(Role.GOOD, 0.35).set_stroke(Role.GOOD))
        with self.voiceover(text="Then it settles C, at three. <bookmark mark='late'/> Through C, B costs three "
                                 "minus two: one. That is shorter, but B is already final. <bookmark mark='wrong'/> "
                                 "The algorithm answers two. The true distance is one."):
            self.play(nodes["C"][0].animate.set_fill(Role.GOOD, 0.35).set_stroke(Role.GOOD))
            self.wait_until_bookmark("late")
            self.play(ShowPassingFlash(arrows[2].copy().set_stroke(Role.FOCUS, 8), time_width=0.7), run_time=1.2)
            self.wait_until_bookmark("wrong")
            self.claim("guarantee-final")
            truth = label(f"true: {N['via_C']}", size=26, color=Role.BAD).next_to(tags["B"], RIGHT, buff=0.3)
            self.play(tags["B"].animate.set_color(Role.BAD), FadeIn(truth, shift=UP * 0.1))
        self.wait(1.5)
        with self.voiceover(text="With negative lengths, use the Bellman-Ford algorithm instead."):
            self.wait(0.5)
        self.wait(1)
