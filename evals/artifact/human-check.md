# Human check for the rederivation eval

The rederivation eval asks a model reader to work out a result that an explanation never states, and a model grader marks each step. This page is for a person who does the same thing, so we can see whether the grader's marks agree with a person's working.

**Who.** A technical reader who is new to the subject: comfortable with school mathematics and science and with basic programming. Someone who already knows the subject well is not the right tester for it.

**What to do.**

1. Pick one subject below that you do not already know well.
2. The owner sends you one explanation of it: one condition's `explanation.md` or page from the saved builds in `evals/artifact/results/2026-10-04-dev/work/<subject>/<condition>/`. Read it once.
3. Without looking anything up, work out that subject's question below, on paper or in a text file. Write it as steps. For each step, note which part of the explanation it rests on (a heading, a paragraph, a figure, a control on the page), or "background" when it is something you already knew, such as arithmetic. If the explanation leaves out something you need, say what, and stop there: that gap is useful.
4. Write down your result.

Do not read `questions.yaml` before you finish: it holds the expected steps and result.

**Send it back** as `evals/artifact/human/<subject>-<condition>.md`, with no name or personal details:

```markdown
---
subject: bloom-filter
condition: principles
---

1. ... (rests on: the section "Adding an item")
2. ...

Result: ...
```

**How it is graded.** With the same rubric and the same grader as the model readers:

```bash
uv run explainer eval human --builds evals/artifact/results/2026-10-04-dev --chain evals/artifact/human/<subject>-<condition>.md
```

The marks are saved next to the file. [docs/evals.md](../../docs/evals.md#rederivation) records whether the person's marks agree with the model readers' marks on the same explanation.

## The questions (dev subjects)

- **gps-relativity.** A receiver's own clock is right, but one of the four satellites it uses has a clock 10 nanoseconds fast that nothing corrects. Roughly how wrong is the distance to that satellite, and why can the receiver's fourth unknown not absorb this error the way it absorbs its own clock error?
- **vaccine-memory.** In a simple model, the immune cells that match an antigen double every 12 hours until there are enough to clear the infection. Vaccination leaves 1,000 times more matching cells than a first infection starts with. About how much sooner does the response reach full strength, and why does the answer not depend on how many cells count as 'enough'?
- **key-exchange.** Three people, Alice, Bob, and Carol, want one shared secret key, using the same public p and g and sending only messages anyone can read. How can they do it, and why does an eavesdropper still not get the key?
- **two-tides.** At first and third quarter Moon, the Sun and Moon are at right angles as seen from Earth. How large are the tides then, compared with spring tides?
- **bloom-filter.** Two Bloom filters have the same size and the same hash functions; one was built from a set A and the other from a set B. How can you get a filter for A ∪ B without the items, and is it exact? What does a bitwise AND of the two give?
- **heat-pump.** The same machine run in reverse is an air conditioner: it takes heat from the cold inside and gives it to the warm outside. What is its ideal limit on heat removed per unit of electricity, and why is it exactly one less than the heating limit for the same two temperatures?
- **quorum.** A five-server store uses a write group of W servers and a read group of R servers, not necessarily majorities. What must W and R satisfy for every read to see the latest committed write, and with W = 4 and R = 2, how many failures can writes and reads each survive?
- **antibiotic-resistance.** In an infection of 10^10 bacteria, one in 10^8 resists drug A and one in 10^9 resists drug B, by unrelated mutations. Why is giving both drugs together much less likely to end with a resistant infection than giving either alone?
- **float-sum.** Which of these can a double store exactly: 0.375, 0.2, 0.0625, 0.3? And why does adding 0.125 eight times give exactly 1.0, while adding 0.1 ten times does not?
- **greenhouse.** Suppose the atmosphere had the same temperature at every height. What would adding CO2 then do to the surface temperature, and why?
