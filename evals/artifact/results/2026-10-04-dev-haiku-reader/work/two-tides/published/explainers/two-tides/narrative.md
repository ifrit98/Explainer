# Narrative: two-tides

## 1. Reader before and after

- **Before:** A technical reader who knows Newton's inverse-square gravity, acceleration as a vector, free fall, and that the Earth turns once a day. Knows "the Moon causes tides". Has never asked why the side away from the Moon also has a high tide.
- **After:** "The Moon pulls the near side more than Earth's centre, and the centre more than the far side; because the whole Earth falls toward the Moon, only these differences act, and they stretch the ocean into two bulges that the Earth turns through each 24 h 50 min."

## 2. Question and motive

- **Question:** The Moon is on one side of the Earth. Why is the water high on both sides? Result in words: the Moon does not lift the water toward itself; it stretches the Earth's ocean along the Earth–Moon line, and a stretch has two ends.
- **Why care:** The obvious picture (the Moon pulls water toward it) predicts one high tide a day. Most coasts have two. The obvious picture is wrong in a way that teaches something about gravity.
- **Why this approach:** Ask what the pull is at three points, near side, centre, far side, with real numbers. Then ask which of those pulls can change the Earth's shape.

## 3. Introduction ledger

| Reference | Means | Grounded by | Beat |
|---|---|---|---|
| Moon's pull | acceleration from the Moon's gravity at a point | 33.19 µm/s² at Earth's centre | 2 |
| µm/s² | 10⁻⁶ m/s² | g is 9.81 m/s² = 9,810,000 µm/s² | 2 |
| near side / far side | surface points nearest / farthest from the Moon | 378,029 km / 390,771 km from the Moon | 2 |
| tidal acceleration | Moon's pull at a point minus the pull at the centre | +1.13 at the near side | 4 |
| side point | surface point 90° from the near side | 0.55 µm/s² toward the centre | 5 |
| bulge | water gathered on the Earth–Moon line | the two ends of the stretch | 6 |
| lunar day | 24 h 50 min, time for the Moon to come back to the same place in the sky | Moon moves about 12° a day | 8 |

## 4. Beats

| # | Kind | Reader's question | Bridge | Shown | Said | Reader now knows |
|---|---|---|---|---|---|---|
| 1 | hook | Why two high tides? | — | question, then the answer in bold | Most coasts get two high tides a day, one when the Moon is overhead and one when it is on the other side of the Earth. Answer: the Moon stretches the ocean along the Earth–Moon line; a stretch has two ends; the Earth turns through both. | the result |
| 2 | instance | How strong is the pull at different points? | So compute it | table: near side 378,029 km, centre 384,400 km, far side 390,771 km | near side 34.32, centre 33.19, far side 32.12 µm/s², all toward the Moon | all three point toward the Moon, unequal |
| 3 | objection | Then why is the far water not pulled toward the Moon? | But | — | The Earth and Moon orbit their shared centre of mass; an orbit is free fall, so Earth's centre accelerates toward the Moon at 33.19. A shared acceleration changes nothing inside a falling body (astronauts float in an orbiting station). | only the part that differs from the centre's pull acts |
| 4 | name | What is left? | Therefore subtract | difference column; sign: + toward the Moon | tidal acceleration = pull − 33.19: near +1.13 (ahead of the centre, toward the Moon), far −1.07 (left behind, away from the Moon). Both point away from Earth's centre. | both ends pulled outward relative to the centre |
| 5 | mechanism | What about the sides? | And | side row | A side point is 90° from the near side. Its pull points at the Moon, so it tilts 0.95° toward Earth's centre; subtracting the centre's pull leaves 0.55 inward. | stretch along the line, squeeze across |
| 6 | mechanism | 1.1 µm/s² is about 10⁻⁷ g. How does it move water? | But it is tiny | ASCII figure | Up/down: it competes with g, so it changes weight by 1 part in 10 million; no effect. Along the surface: gravity has no part along a level surface, so the tidal acceleration (up to 0.82 at 45° from the near side) is the only sideways push; water flows until the sea slopes enough to balance it. Water gathers at two bulges. | two bulges |
| 7 | test | Does the subtraction matter? | So check it | — | If something held the Earth still, nothing would subtract 33.19; the far side's 32.12 points toward the Moon, into the Earth: one bulge. Sun: pull 179× the Moon's but 389× farther; the difference across Earth is about pull × 2R/d, so 179/389 = 0.46× tide. | why subtract |
| 8 | mechanism | When do high tides come? | Therefore | timeline | Earth turns under bulges. The Moon moves about 12° a day in the same direction, so Earth takes 24 h 50 min (a lunar day) to face it again; high tides 12 h 25 min apart. | timing |
| 9 | close | — | So | — | Two high tides because the Moon pulls the near side more and the far side less than Earth's centre, and the falling Earth feels only these differences. The far bulge needs no centrifugal force (a common textbook story). Scope: real heights, once-a-day coasts, spring/neap. | the answer |

## 5. Concrete to symbol

Pull = GM/r² first with numbers; then the approximation 2GMR/d³ only to explain the Sun's cube law.

## 6. Links between representations

The table and the text use the same four point names and the same numbers.

## 7. Close the loop

- **Answer:** Two high tides because the tidal acceleration stretches the ocean along the Earth–Moon line, toward the Moon on the near side and away on the far side.
- **General argument:** Any body falling in a non-uniform gravity field stretches along the line to the source.
- **Payoff:** Predict the next high tide (12 h 25 min later), why the Sun's tide is smaller. Scope: real tide heights, once-a-day tides, spring/neap.
