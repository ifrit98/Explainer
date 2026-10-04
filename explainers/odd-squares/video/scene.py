"""odd-squares — each odd number is an L of tiles that grows a square by one, and each L is two bigger than the last.

Follows ../narrative.md beat by beat (the beat number is in each comment). Values from ../model.yaml.

Render:  uv run explainer render odd-squares --draft
         uv run explainer render odd-squares
"""

from manim import *

from explainer_kit import ExplainerScene, Role, label, load_model

M = load_model(__file__)
ODDS = M["odd_numbers"]
SUMS = M["sums"]
# one color per odd number; an L has the color of its odd number in the sums (ledger: "L colors")
COLORS = [BLUE_C, TEAL_C, GOLD_C, MAROON_C, PURPLE_B, GREEN_C, RED_C, YELLOW_D, PINK, GREY_B]
CELL = 0.6
ANCHOR = np.array([-2.3, 0.6, 0])  # top-right corner of the square; it grows left and down, so each L is an L


def tile(i: int, j: int, size: float, color) -> Square:
    sq = Square(side_length=size * 0.92, stroke_width=0, fill_color=color, fill_opacity=0.9)
    return sq.move_to(ANCHOR + (i + 0.5) * size * LEFT + (j + 0.5) * size * DOWN)


def ell(k: int, size: float, color) -> VGroup:
    """The k-th L: the tiles that grow a square of side k − 1 to side k.
    Parts: corner (bottom left), row (along the bottom), column (on the left)."""
    n = k - 1
    corner = VGroup(tile(n, n, size, color))
    row = VGroup(*[tile(i, n, size, color) for i in range(n)])
    col = VGroup(*[tile(n, j, size, color) for j in range(n)])
    return VGroup(corner, row, col)


def braces(piece: VGroup, row_text: str, col_text: str):
    corner, row, col = piece
    b_row, b_col = Brace(row, DOWN, color=Role.RELATION), Brace(col, LEFT, color=Role.RELATION)
    t_row = label(row_text, size=26).next_to(b_row, DOWN, buff=0.1)
    t_col = label(col_text, size=26).next_to(b_col, LEFT, buff=0.1)
    t_corner = label("1", size=26, color=Role.FOCUS).next_to(corner, DL, buff=0.1)
    return VGroup(b_row, b_col), VGroup(t_row, t_col, t_corner)


def sum_row(n: int, odds=ODDS, total=None, scale=0.8) -> MathTex:
    parts = []
    for k in range(n):
        parts += [str(odds[k])] + (["+"] if k < n - 1 else [])
    tex = MathTex(*parts, "=", str(total if total is not None else SUMS[n - 1]))
    for k in range(n):
        tex[2 * k].set_color(COLORS[k])
    return tex.scale(scale)


class OddSquares(ExplainerScene):
    voice = "af_heart"

    def light(self, k: int, rows):
        """Ledger 'a term lights up': the k-th odd number in the last visible sum row is the L being added."""
        return Indicate(rows[min(k, 4)][2 * k], color=COLORS[k], scale_factor=1.5)

    def construct(self):
        rows = VGroup(*[sum_row(n) for n in range(1, 6)]).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        rows.move_to(RIGHT * 1.6 + UP * 0.75)
        squares = VGroup(*[MathTex(rf"= {n} \times {n}", color=Role.FOCUS).scale(0.8).next_to(rows[n - 1], RIGHT, buff=0.25)
                           for n in range(1, 6)])

        # 1 — hook: the sums, each odd number in its own color
        with self.voiceover(text="Add the odd numbers in order, each in its own color, and watch what the sums make. "
                                 "<bookmark mark='r1'/> One. "
                                 "<bookmark mark='r2'/> One plus three is four. <bookmark mark='r3'/> One plus three "
                                 "plus five is nine. <bookmark mark='r4'/> Add seven: sixteen. <bookmark mark='r5'/> "
                                 "Add nine: twenty-five."):
            for n in range(1, 6):
                self.wait_until_bookmark(f"r{n}")
                self.play(FadeIn(rows[n - 1], shift=RIGHT * 0.2), run_time=0.6)

        # 2 — notice and name: every sum is a square; n is the count of odd numbers
        rule = label("the first n odd numbers add up to n × n", size=30, color=Role.ENTITY).to_edge(UP, buff=0.45)
        with self.voiceover(text="Look at the answers. <bookmark mark='s1'/> One is one times one. <bookmark mark='s2'/> "
                                 "Four is two times two. <bookmark mark='s3'/> Nine is three times three. "
                                 "<bookmark mark='s4'/> Sixteen is four times four. <bookmark mark='s5'/> Twenty-five is "
                                 "five times five. Every sum is a square number. Yellow marks what to look at."):
            for n in range(1, 6):
                self.wait_until_bookmark(f"s{n}")
                self.play(FadeIn(squares[n - 1], shift=LEFT * 0.1), run_time=0.5)
        with self.voiceover(text="Now count the odd numbers in each sum. <bookmark mark='count'/> Three of them give "
                                 "three times three. Call that count n. For one plus three plus five, n is three. "
                                 "<bookmark mark='rule'/> So it seems that the first n odd numbers add up to n times n."):
            self.wait_until_bookmark("count")
            self.play(Indicate(VGroup(*[rows[2][2 * k] for k in range(3)]), color=Role.FOCUS),
                      Indicate(squares[2], color=Role.FOCUS), run_time=1.2)
            self.wait_until_bookmark("rule")
            self.play(FadeIn(rule, shift=DOWN * 0.1))

        # 3 — objection and motive; the question mark means "not proved yet"
        doubt = label("?", size=34, color=Role.BAD).next_to(rule, RIGHT, buff=0.15)
        with self.voiceover(text="But why should odd numbers make squares at all? <bookmark mark='q'/> Five examples show "
                                 "a pattern. They do not prove it for every n. <bookmark mark='qm'/> The question mark "
                                 "means: not proved yet. We need a reason."):
            self.wait_until_bookmark("q")
            self.claim("misconception-examples")
            self.wait_until_bookmark("qm")
            self.play(FadeIn(doubt, scale=1.5))
        self.wait(1.2)

        # 4 — approach: a square number is a square of tiles; ask what one more odd number adds
        E = M["example_square"]
        nine = VGroup(*[tile(i, j, CELL, Role.MUTED) for i in range(E["rows"]) for j in range(E["rows"])])
        side = label("side 3", size=24, color=Role.MUTED).next_to(nine, DOWN, buff=0.15)
        first = ell(1, CELL, COLORS[0])
        grid = VGroup(first)
        self.play(FadeOut(squares), run_time=0.5)
        with self.voiceover(text="A square number is a square of tiles. <bookmark mark='nine'/> Nine tiles make three rows "
                                 "of three: a three by three square, with side three. <bookmark mark='ask'/> Each sum "
                                 "adds one more odd number. So ask: what does one more odd number add to a square of "
                                 "tiles? <bookmark mark='t'/> Start with the first odd number, one: one tile, a square "
                                 "with side one."):
            self.play(LaggedStart(*[FadeIn(t, scale=0.6) for t in nine], lag_ratio=0.05), FadeIn(side), run_time=1.2)
            self.wait_until_bookmark("ask")
            self.play(Indicate(rows[2], color=Role.FOCUS))
            self.wait_until_bookmark("t")
            self.play(FadeOut(nine), FadeOut(side))
            self.play(FadeIn(first, scale=0.6), self.light(0, rows))

        # 5 — name the L (a column on the left, a row along the bottom); the color and highlight links
        with self.voiceover(text="Add the next odd number, three. <bookmark mark='l2'/> Three tiles go around it: to the "
                                 "left, below, and in the corner. Together they make an L shape: a column and a row "
                                 "that share a corner. The square now has side two. <bookmark mark='four'/> One plus three "
                                 "is four tiles, the same four as in the sums. <bookmark mark='color'/> Each L has the "
                                 "color of its odd number, and its number lights up in the sums."):
            self.wait_until_bookmark("l2")
            second = ell(2, CELL, COLORS[1])
            grid.add(second)
            self.play(LaggedStart(*[FadeIn(c, scale=0.6) for c in second.family_members_with_points()],
                                  lag_ratio=0.25, run_time=1.2))
            self.wait_until_bookmark("four")
            self.play(Indicate(rows[1][-1], color=Role.FOCUS, scale_factor=1.5))
            self.wait_until_bookmark("color")
            self.play(Indicate(second, color=COLORS[1]), self.light(1, rows))

        # 6 — the build continues; n Ls make side n
        with self.voiceover(text="The next L has five tiles, <bookmark mark='g3'/> and makes side three. "
                                 "<bookmark mark='g4'/> Seven tiles make side four. <bookmark mark='g5'/> Nine tiles make "
                                 "side five. Each L adds one to the side. So after n Ls, the side is n. Here n counts the "
                                 "Ls, and each L is one odd number, so it is the same n as before."):
            for k in range(3, 6):
                self.wait_until_bookmark(f"g{k}")
                piece = ell(k, CELL, COLORS[k - 1])
                grid.add(piece)
                self.play(LaggedStart(*[FadeIn(c, scale=0.6) for c in piece.family_members_with_points()],
                                      lag_ratio=0.08, run_time=0.9), self.light(k - 1, rows))
        self.wait(1.2)

        # 7 — mechanism: an L is row + column + corner, and each L is two bigger than the last
        F, G = M["fifth_l"], M["sixth_l"]
        old = SurroundingRectangle(VGroup(*grid[:4]), color=WHITE, buff=0.02, stroke_width=2)
        marks5, tags5 = braces(grid[4], str(F["row"]), str(F["column"]))
        ghost = ell(M["next_square_side"], CELL, COLORS[5])
        ghost.set_fill(opacity=0.3)
        marks6, tags6 = braces(ghost, str(G["row"]), str(G["column"]))
        sums_l = VGroup(
            label(f"around 4 by 4:  {F['row']} + {F['column']} + {F['corner']} = {F['total']}", size=26),
            label(f"around 5 by 5:  {G['row']} + {G['column']} + {G['corner']} = {G['total']}", size=26),
            label("each L is two bigger: 1, 3, 5, 7, 9, 11, …", size=26, color=Role.FOCUS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(rows, DOWN, buff=0.5).align_to(rows, LEFT)
        with self.voiceover(text="Why is each L the next odd number? <bookmark mark='old'/> Look at the L around the four "
                                 "by four square. <bookmark mark='parts'/> It has a row of four, <bookmark mark='col'/> a "
                                 "column of four, <bookmark mark='corner'/> and one corner. Four plus four plus one is "
                                 "nine."):
            self.wait_until_bookmark("old")
            self.play(Create(old))
            self.wait_until_bookmark("parts")
            self.claim("mechanism-l")
            self.play(GrowFromCenter(marks5[0]), FadeIn(tags5[0]))
            self.wait_until_bookmark("col")
            self.play(GrowFromCenter(marks5[1]), FadeIn(tags5[1]))
            self.wait_until_bookmark("corner")
            self.play(Indicate(grid[4][0], color=Role.FOCUS, scale_factor=1.3), FadeIn(tags5[2]))
            self.play(FadeIn(sums_l[0], shift=UP * 0.1))
        self.wait(1.2)
        with self.voiceover(text="The next L goes around the five by five square, <bookmark mark='next'/> and makes six by "
                                 "six. It is drawn faint, because we have not added it yet. It has five plus five plus "
                                 "one: eleven. <bookmark mark='two'/> Each L is two "
                                 "bigger than the one before: one more in its row, and one more in its column. "
                                 "<bookmark mark='odd'/> The first L is the first tile: no row, no column, only its "
                                 "corner. It is one. So the Ls are one, three, five, seven, and so on: the odd numbers, in "
                                 "order."):
            self.wait_until_bookmark("next")
            self.play(FadeOut(VGroup(old, marks5, tags5)), FadeIn(ghost), run_time=0.8)
            self.play(GrowFromCenter(marks6[0]), GrowFromCenter(marks6[1]), FadeIn(tags6), FadeIn(sums_l[1], shift=UP * 0.1))
            self.wait_until_bookmark("two")
            self.claim("mechanism-next")
            self.play(Indicate(VGroup(tags6[0], tags6[1]), color=Role.FOCUS, scale_factor=1.4))
            self.wait_until_bookmark("odd")
            self.play(Indicate(grid[0], color=Role.FOCUS, scale_factor=1.6))
            self.play(FadeIn(sums_l[2], shift=UP * 0.1))
            self.play(LaggedStart(*[self.light(k, rows) for k in range(5)], lag_ratio=0.4), run_time=2.5)
        self.wait(1.2)

        # 8 — close: the argument for every n, in words; the question mark goes
        final_rule = MathTex(r"\underbrace{1 + 3 + 5 + \cdots}_{n \text{ odd numbers}}", "=", "n^2",
                             color=Role.ENTITY).scale(0.95).to_edge(UP, buff=0.3)
        self.play(FadeOut(VGroup(ghost, marks6, tags6, sums_l)), run_time=0.5)
        with self.voiceover(text="So adding the odd numbers in order is adding the Ls in order. <bookmark mark='build'/> "
                                 "After n Ls, the square has side n. <bookmark mark='done'/> So the first n odd numbers "
                                 "add up to n times n. The question mark can go. <bookmark mark='sq'/> We write n times n "
                                 "as n squared, n with a small two. <bookmark mark='dots'/> The brace marks the n odd "
                                 "numbers, and the dots mean: and so on, in order."):
            self.wait_until_bookmark("build")
            self.play(LaggedStart(*[AnimationGroup(Indicate(grid[k], color=COLORS[k], scale_factor=1.08), self.light(k, rows))
                                    for k in range(5)], lag_ratio=0.5), run_time=3)
            self.wait_until_bookmark("done")
            self.claim("guarantee-every-n")
            self.play(FadeOut(doubt, scale=1.5))
            self.play(FadeOut(rule, shift=UP * 0.1), FadeIn(final_rule, shift=UP * 0.1))
            self.wait_until_bookmark("sq")
            self.play(Indicate(final_rule[2], color=Role.FOCUS, scale_factor=1.4))
            self.wait_until_bookmark("dots")
            self.play(Indicate(final_rule[0], color=Role.FOCUS, scale_factor=1.1))
        self.wait(1.5)

        # 9 — test
        self.predict("What is the sum of the first ten odd numbers?")

        # 10 — apply: ten Ls, each in its own color, make side 10; the full sum in the L colors
        Q, T = M["predict"], M["tenth_l"]
        full = sum_row(Q["n"], M["odd_numbers_to_10"], Q["sum"], scale=0.62).next_to(rows, DOWN, buff=0.5).align_to(rows, LEFT)
        steps = label(f"1 + {T['steps_of_two']} × 2 = {T['size']}", size=26, color=COLORS[-1]).next_to(full, DOWN, buff=0.3).align_to(full, LEFT)
        with self.voiceover(text="Ten Ls make a square with side ten: one hundred tiles. <bookmark mark='new'/> The five "
                                 "new Ls are eleven, thirteen, fifteen, seventeen, and nineteen, each in its own color. "
                                 "<bookmark mark='tenth'/> The first L is one, and each of the nine Ls after it adds two: "
                                 "one plus nine times two is nineteen. "
                                 "<bookmark mark='ten'/> So the first ten odd numbers add up to one hundred."):
            self.play(grid.animate.scale(0.5, about_point=ANCHOR), run_time=0.8)
            for k in range(6, Q["n"] + 1):
                piece = ell(k, CELL / 2, COLORS[k - 1])
                grid.add(piece)
                self.play(FadeIn(piece, scale=0.8), run_time=0.3)
            self.wait_until_bookmark("new")
            self.play(Write(full), run_time=1.5)
            self.wait_until_bookmark("tenth")
            self.play(FadeIn(steps, shift=UP * 0.1), Indicate(grid[-1], color=COLORS[-1], scale_factor=1.05))
            self.wait_until_bookmark("ten")
            self.play(Indicate(full[-1], color=Role.FOCUS, scale_factor=1.4))
        self.wait(1.2)

        # 11 — objection: the first tile matters; without it the Ls go around a hole (3 + 5 = 9 − 1)
        S = M["start_at_3"]
        bad = label(f"{S['terms'][0]} + {S['terms'][1]} = {S['sum']}: not a square", size=28, color=Role.BAD)
        bad.next_to(steps, DOWN, buff=0.35).align_to(steps, LEFT)
        mini = VGroup(ell(2, CELL, COLORS[1]), ell(3, CELL, COLORS[2]))
        hole = DashedVMobject(Square(side_length=CELL * 0.92, color=Role.BAD, stroke_width=3), num_dashes=12).move_to(tile(0, 0, CELL, BLACK))
        with self.voiceover(text="The first tile matters. <bookmark mark='s3'/> Start at three instead: three plus five is "
                                 "eight. <bookmark mark='need'/> Without the first tile, the Ls go around a hole. Nine "
                                 "minus one is eight, and eight is not a square."):
            self.wait_until_bookmark("s3")
            self.claim("guarantee-every-n")
            self.play(FadeOut(grid), FadeIn(mini), run_time=0.8)
            self.wait_until_bookmark("need")
            self.play(Create(hole), FadeIn(bad, shift=UP * 0.1))
        self.wait(1.2)

        # 12 — payoff: which odd number is in place n; concrete first (n is 5), the middle step, then checks
        self.play(FadeOut(VGroup(bad, steps, full, mini, hole)), run_time=0.6)
        small = VGroup(*[ell(k, CELL, COLORS[k - 1]) for k in range(1, 6)])
        marks, tags = braces(small[4], "4", "4")
        n_is = label("n = 5", size=28, color=Role.FOCUS).next_to(small, UP, buff=0.25).align_to(small, RIGHT)
        law = MathTex(r"(n-1) + (n-1) + 1", r"= 2n - 2 + 1", r"= 2n - 1").scale(0.68).next_to(rows, DOWN, buff=0.5).align_to(rows, LEFT)
        C = M["check_2n_minus_1"]
        checks = label("check:  " + ",  ".join(f"n = {k} → {v}" for k, v in C.items()), size=26, color=Role.GOOD)
        checks.next_to(law, DOWN, buff=0.35).align_to(law, LEFT)
        with self.voiceover(text="One more thing. A sum of the first ten odd numbers stopped at nineteen. Where does a sum "
                                 "of n odd numbers stop? The L that makes side n tells us. It goes around a square of side "
                                 "n minus one. <bookmark mark='n'/> Here n is five, and n minus one is four. "
                                 "<bookmark mark='sym'/> So it has n minus one, plus n minus one, plus one tiles. The "
                                 "brackets keep each n minus one together. <bookmark mark='l2'/> Two copies of n make two "
                                 "n, which means two times n. Take away the two ones, and add the corner: "
                                 "<bookmark mark='l3'/> two n minus one. <bookmark mark='check'/> Check: n equals five gives "
                                 "nine. N equals ten gives nineteen, where the sum stopped. N equals one gives one, the "
                                 "first tile."):
            self.play(FadeIn(small), FadeIn(marks), FadeIn(tags))
            self.wait_until_bookmark("n")
            self.play(FadeIn(n_is, shift=DOWN * 0.1))
            self.wait_until_bookmark("sym")
            self.play(FadeTransform(tags[0], label("n − 1", size=26).move_to(tags[0])),
                      FadeTransform(tags[1], label("n − 1", size=26).next_to(marks[1], LEFT, buff=0.1)))
            self.play(Write(law[0]), run_time=0.8)
            self.wait_until_bookmark("l2")
            self.play(Write(law[1]), run_time=0.8)
            self.wait_until_bookmark("l3")
            self.play(Write(law[2]), run_time=0.8)
            self.wait_until_bookmark("check")
            self.play(FadeIn(checks, shift=UP * 0.1))
        self.wait(1.2)

        # 13 — recap: end on the answer to the opening question
        with self.voiceover(text="So, the answer: <bookmark mark='ans'/> the first n odd numbers add up to n squared. "
                                 "Every odd number is an L, and the Ls build squares."):
            self.wait_until_bookmark("ans")
            self.play(Indicate(final_rule, color=Role.FOCUS))
        self.wait(2)
