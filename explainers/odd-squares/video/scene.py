"""odd-squares — each odd number is an L that grows the square by one. See ../model.md.

Render:  uv run explainer render odd-squares --draft
         uv run explainer render odd-squares
"""

from manim import *

from explainer_kit import ExplainerScene, Role, label, load_model

M = load_model(__file__)
ODDS = M["odd_numbers"]
SUMS = M["sums"]
COLORS = [BLUE_C, TEAL_C, GOLD_C, MAROON_C, PURPLE_B]  # one color per odd number (L shape)
CELL = 0.6
ORIGIN_CORNER = np.array([-5.6, -2.4, 0])  # bottom-left corner of the growing square


def cell(i: int, j: int, size: float, color) -> Square:
    sq = Square(side_length=size * 0.92, stroke_width=0, fill_color=color, fill_opacity=0.9)
    return sq.move_to(ORIGIN_CORNER + (i + 0.5) * size * RIGHT + (j + 0.5) * size * UP)


def gnomon(k: int, size: float, color) -> VGroup:
    """The k-th L shape: the cells with max(i, j) = k − 1. Corner first, then the row, then the column."""
    n = k - 1
    corner = [cell(n, n, size, color)]
    row = [cell(i, n, size, color) for i in range(n)]
    col = [cell(n, j, size, color) for j in range(n)]
    return VGroup(VGroup(*corner), VGroup(*row), VGroup(*col))


def sum_row(n: int) -> MathTex:
    parts = []
    for k in range(n):
        parts += [str(ODDS[k])] + ([r"+"] if k < n - 1 else [])
    tex = MathTex(*parts, "=", str(SUMS[n - 1]))
    for k in range(n):
        tex[2 * k].set_color(COLORS[k])
    return tex.scale(0.85)


class OddSquares(ExplainerScene):
    voice = "af_heart"

    def construct(self):
        # 1 — the pattern
        rows = VGroup(*[sum_row(n) for n in range(1, 6)]).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        rows.to_edge(RIGHT, buff=1.0).shift(UP * 0.3)
        with self.voiceover(text="Add the odd numbers in order. <bookmark mark='r1'/> One. "
                                 "<bookmark mark='r2'/> One plus three is four. <bookmark mark='r3'/> "
                                 "Add five, and you get nine. <bookmark mark='r4'/> Then sixteen, "
                                 "<bookmark mark='r5'/> then twenty-five."):
            for n in range(1, 6):
                self.wait_until_bookmark(f"r{n}")
                self.play(FadeIn(rows[n - 1], shift=RIGHT * 0.2), run_time=0.6)
        with self.voiceover(text="Every sum is a square number. Five examples show a pattern. "
                                 "They do not prove a rule. A picture can."):
            self.play(*[Indicate(r[-1], color=Role.FOCUS) for r in rows])

        # 2 — the picture: each odd number is an L that wraps the previous square
        grid = VGroup()
        with self.voiceover(text="Start with one square. <bookmark mark='g2'/> Three squares wrap it "
                                 "into a two by two square. <bookmark mark='g3'/> Five more make three by three. "
                                 "<bookmark mark='g4'/> Seven make four by four. <bookmark mark='g5'/> "
                                 "Nine make five by five."):
            for k in range(1, 6):
                if k > 1:
                    self.wait_until_bookmark(f"g{k}")
                piece = gnomon(k, CELL, COLORS[k - 1])
                grid.add(piece)
                self.play(LaggedStart(*[FadeIn(c, scale=0.6) for c in piece.family_members_with_points()],
                                      lag_ratio=0.08, run_time=0.9),
                          Indicate(rows[k - 1][2 * (k - 1)], color=Role.FOCUS))

        # 3 — why: an L is one row, one column, and one corner
        last = grid[-1]
        corner, row, col = last
        brace_row = Brace(row, UP, color=Role.RELATION)
        brace_col = Brace(col, RIGHT, color=Role.RELATION)
        tag_row = label("n − 1", size=26).next_to(brace_row, UP, buff=0.1)
        tag_col = label("n − 1", size=26).next_to(brace_col, RIGHT, buff=0.1)
        tag_corner = label("1", size=26, color=Role.FOCUS).next_to(corner, UR, buff=0.12)
        law = VGroup(MathTex(r"(n-1) + (n-1) + 1 = 2n - 1"),
                     MathTex(r"n^2 - (n-1)^2 = 2n - 1")).arrange(DOWN, buff=0.3).scale(0.85)
        law.next_to(rows, DOWN, buff=0.6).align_to(rows, RIGHT)  # right-aligned: the law is wider than the rows
        with self.voiceover(text="Why does this always work? <bookmark mark='parts'/> Each L has one new row, "
                                 "one new column, and one corner. For the fifth square, that is four, plus four, "
                                 "plus one: nine. <bookmark mark='law'/> In general, the n-th L has two n minus "
                                 "one squares. That is exactly the n-th odd number."):
            self.wait_until_bookmark("parts")
            self.play(row.animate.set_color(Role.ENTITY), col.animate.set_color(Role.SECONDARY),
                      corner.animate.set_color(Role.FOCUS))
            self.play(GrowFromCenter(brace_row), GrowFromCenter(brace_col), FadeIn(tag_row), FadeIn(tag_col),
                      FadeIn(tag_corner))
            self.wait_until_bookmark("law")
            self.play(Write(law[0]))
            self.play(Write(law[1]))
        self.play(FadeOut(VGroup(brace_row, brace_col, tag_row, tag_col, tag_corner)),
                  row.animate.set_color(COLORS[4]), col.animate.set_color(COLORS[4]),
                  corner.animate.set_color(COLORS[4]))

        # 4 — predict first: the first ten odd numbers
        self.predict("What is the sum of the first ten odd numbers?")
        with self.voiceover(text="Ten L shapes make a ten by ten square. <bookmark mark='ten'/> "
                                 "So the sum is one hundred."):
            self.play(grid.animate.scale(0.5, about_point=ORIGIN_CORNER), FadeOut(law), run_time=1)
            for k in range(6, M["predict"]["n"] + 1):
                piece = gnomon(k, CELL / 2, Role.ENTITY)  # one color: these Ls have no row on the right
                grid.add(piece)
                self.play(FadeIn(piece, scale=0.8), run_time=0.35)
            self.wait_until_bookmark("ten")
            answer = MathTex(r"1 + 3 + \cdots + 19 = 100").scale(0.95).next_to(rows, DOWN, buff=0.6).align_to(rows, RIGHT)
            self.play(Write(answer))

        # 5 — the rule
        rule = MathTex(r"1 + 3 + 5 + \cdots + (2n-1) = n^2", color=Role.ENTITY).scale(1.1).to_edge(UP, buff=0.5)
        with self.voiceover(text="The rule holds for every n, because each step adds the same kind of L."):
            self.play(Write(rule))
        self.wait(1.5)
