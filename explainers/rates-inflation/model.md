# Semantic model: how a higher interest rate lowers inflation

> Source of truth. The page derives from this file.

## Central question

How does a central bank lower inflation by raising its interest rate, how long does it take, and which parts are disputed?

## Audience and prior knowledge

A technical reader who knows what inflation and an interest rate are and follows news about central banks. No economics training.

## Entities

| Entity | Definition (one sentence) | Status |
|---|---|---|
| policy rate | the interest rate the central bank sets on overnight money between banks (the federal funds rate, Bank Rate) | fact |
| market rates | the rates on loans, mortgages, deposits, and bonds | fact |
| real rate | the interest rate minus the inflation people expect | definition |
| demand | the spending of households, firms, and buyers abroad | fact |
| output gap | how far output is above (+) or below (−) what the economy can produce without speeding up inflation, in % | model concept; estimated, not observed |
| inflation | the yearly rise of the price level, in % | observation |
| expected inflation | the inflation that people and firms build into wages, prices, and contracts | estimate (surveys, markets) |
| anchored expectations | expected inflation stays near the target, whatever inflation did last year | assumption about credibility |

## Causal chain (the mainstream view)

```text
policy rate ↑
  → market rates ↑ (fully for variable-rate loans, slowly for fixed-rate mortgages)
  → real rate ↑ (if expected inflation does not rise as much)
  → borrowing costs more, saving pays more, asset prices fall, the currency rises
  → demand ↓ → output gap < 0
  → firms raise prices less, wage growth slows → inflation ↓, later
  → and if the bank is credible, expected inflation ↓ too, which lowers inflation directly
```

## Lags

- Market rates move within days. Spending changes over months. Inflation changes last.
- Estimate: central banks put the largest effect on inflation one to two years after a change in the policy rate. The lag varies by country and period ("long and variable lags").

## The toy model on the page (constructed)

Quarterly, all in changes from a steady state with inflation at target. Not an estimate for any economy: it shows directions and order, not sizes. It assumes full, immediate pass-through to market rates, and expectations that look back (w is how strongly they are anchored to the target). It leaves out the forward-looking expectations channel: in the toy, expected inflation never responds to the hike itself. Its timing follows the hike: output keeps falling while the hike lasts and turns when it ends at quarter 5; inflation follows two quarters later.

```text
output gap:          y_t = 0.7 · y_(t−1) − 0.25 · (Δi_(t−1) − πe_(t−1))
expected inflation:  πe_t = (1 − w) · π_(t−1)          w = 0.9 anchored, 0.4 weakly anchored
inflation:           π_t = πe_t + 0.35 · y_(t−2) + cost · 0.15 · Δi_(t−1) + supply shock
neo-Fisherian:       πe_t = Δi_t, no effect on demand (disputed long-run view)
```

The hike is held for 4 quarters, then reversed. The supply shock adds 2 points to inflation in quarter 1, shrinking by 40% each quarter.

| Scenario (1-point hike unless stated) | Output gap, lowest | Inflation change, lowest or highest | At quarter 16 |
|---|---|---|---|
| anchored expectations | −0.63% at quarter 5 | −0.24 points at quarter 7 | −0.01 |
| weakly anchored | −0.63% at quarter 5 | −0.41 points at quarter 7 | −0.18 |
| cost channel on | −0.63% at quarter 5 | first +0.16 at quarter 3, then −0.24 | −0.01 |
| supply shock, no hike, anchored | slightly above 0 | +2.00 at quarter 1, fades | 0.00 |
| supply shock, no hike, weakly anchored | above 0 | +2.40 at quarter 2, persists | +0.44 |
| neo-Fisherian, permanent hike | 0 | +1.00, permanent | +1.00 |

## Why this form

| Operation | Simplest alternative | What the alternative breaks (with numbers) |
|---|---|---|
| demand responds to the real rate | demand responds to the policy rate itself | if expected inflation rises 1 point when the policy rate rises 1 point, the real rate is unchanged and borrowing is no more costly: no effect on demand (the neo-Fisherian toggle shows inflation 1 point higher instead) |
| inflation responds to the output gap with a lag | prices respond at once | prices and wages are set in contracts and menus for months; in the toy model inflation is lowest at quarter 7, two quarters after output |
| expected inflation in the inflation equation | inflation depends only on demand | a supply shock would then fade on its own however people react; with weakly anchored expectations it is still +0.44 points at quarter 16 |

## Concrete cases

| Claim | Holds here | Breaks here |
|---|---|---|
| a higher policy rate lowers inflation, after a lag | toy model, anchored: −0.24 points at quarter 7 | neo-Fisherian assumption: inflation ends 1 point higher |
| with anchored expectations a supply shock fades on its own | anchored: the shock is back to 0 by quarter 16 with no hike | weakly anchored: still +0.44 points at quarter 16 |
| the first effect of a hike on prices is down | without a cost channel: inflation never rises | cost channel on: +0.16 points at quarter 3 (the "price puzzle") |

## Epistemic status

- **Established (mainstream):** the policy rate moves market rates; a higher real rate lowers demand; lower demand slows price and wage rises; effects on inflation come with a lag of a year or more.
- **Definition:** real rate = nominal rate − expected inflation.
- **Estimate:** the size of the effect and the length of the lag; they differ across countries, periods, and studies.
- **Disputed:** the price puzzle (some statistical studies find prices rise for a while after a hike; a cost channel may explain it, or the studies may miss information the central bank had); the neo-Fisherian view (a permanently higher rate raises inflation in the long run; a minority view); how fast expected inflation responds to a credible central bank.
- **Constructed:** every number from the toy model.

## Confusion points

- "Higher rates raise prices, because borrowing costs more for firms." → That is the cost channel; in the mainstream view the demand effect is larger and wins after a few quarters.
- "Inflation falls as soon as rates rise." → Inflation responds last: months to years.
- "Central banks control inflation directly." → They set one short interest rate; the rest passes through markets, spending, and expectations.

## Scope

- **Out of scope:** quantitative easing and the bank's balance sheet; fiscal policy and its interaction with inflation; how the neutral real rate is estimated; exchange-rate regimes.

## Representation decision

- **Stage:** 3 (interactive).
- **Reason:** the result depends on assumptions that are disputed or vary by economy (how anchored expectations are, a cost channel, a supply shock, the neo-Fisherian view), and it unfolds over 16 quarters. A reader needs to switch assumptions and compare paths over time.
- **Levels:** L1 the chain in one line / L2 the channels / L3 why the real rate, why a lag, why expectations / L4 the toy model's equations.
