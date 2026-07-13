# Evolving Agents

A prototype for studying **evolving, interacting agents** modeled as *belief
graphs* traversed by probabilistic *thought loops*. Built and analyzed
incrementally — each layer tested and understood before adding the next.

> Note on framing: this began as a "consciousness" experiment, but what it
> actually models is evolutionary and cultural dynamics on graphs — not
> subjective experience. It's best understood as a study of how structure,
> selection, and transmission produce collective behavior.

## What's here

An agent's "mind" is a directed graph of **beliefs** (nodes, each with a value)
connected by weighted **associations** (edges). A *thought* is a probabilistic
walk over that graph; its *payoff* is the value of the distinct beliefs it
reaches. From that single idea, the project builds up:

- **Thought mechanics** — probabilistic traversal, payoff, payoff curves, stalls
- **Meta-cognition** — a monitor that detects a stalled thought and intervenes
  (hard jump vs. soft nudge)
- **Scaling** — a procedural generator making 50-node agents with sealed
  clusters and tunable escape routes
- **Evolution** — crossover, mutation, and fitness-proportional selection, under
  which a population improves on its own
- **Culture** — living agents exchanging beliefs with neighbors on a 2D grid

## Install

```bash
git clone https://github.com/tskrrish/evolving-agents.git
cd evolving-agents
pip install -e .
```

Requires Python 3.9+, `networkx`, and `matplotlib` (installed automatically).

## Quick start

```python
from evolving_agents.generators import build_agent
from evolving_agents.fitness import mean_fitness

# an agent with escape routes thinks far more productively than a sealed one
open_agent   = build_agent(n_nodes=50, escape_density=0.6, seed=1)
sealed_agent = build_agent(n_nodes=50, escape_density=0.0, seed=1)

print("open:  ", round(mean_fitness(open_agent), 1))
print("sealed:", round(mean_fitness(sealed_agent), 1))
```

The `notebooks/01_explore_graph.ipynb` notebook walks through the whole project
interactively with visualizations.

## Key findings

Honest results, including the ones that contradicted expectations:

1. **Payoff beats coverage.** Measuring how many beliefs a thought *touches*
   (coverage) wrongly rewards useless looping. Measuring the *value* of distinct
   beliefs reached (payoff, first-visit only) correctly makes looping stop
   scoring.

2. **Optimizing payoff destroys individuality.** A meta-cognitive "hard jump"
   drives every thought to the maximum payoff (mean 15.0) but collapses variety
   to zero (stdev 0.00) — every thought becomes identical. The gentler "soft
   nudge" scores slightly lower (mean 14.3) but preserves diversity (stdev 1.6).
   Diversity matters, because evolution needs it.

3. **"Stuck wiring loses" — but only at scale.** On the 6-node toy graph, escape
   routes barely matter. On a 50-node graph they nearly *double* fitness
   (~20 → ~37). Some effects are invisible until the system is large enough.

4. **A population evolves on its own.** Under fitness-proportional selection,
   mean fitness climbs (~27 → ~46) with no design input — good wiring spreads,
   bad wiring dies out. (It tends to *converge* toward its best member rather
   than *innovate* beyond it.)

5. **Copy-from-fitter yields a monoculture, and homophily didn't fix it.** On a
   grid, imitating fitter neighbors converges the whole population into one
   culture. Adding a homophily barrier ("only copy from similar-enough
   neighbors") changed nothing — because the barrier gates *imitation* after
   neighbors already interact, whereas distinct cultures require gating
   *interaction itself* (as in Axelrod's 1997 model). Where a constraint sits
   matters more than its strength.

See [`docs/Culture-Documentation.pdf`](docs/Culture-Documentation.pdf) for the
full walkthrough with plots and code explanations.

## Project structure

```
src/evolving_agents/
  graph.py         the hand-built 6-belief toy graph
  thought.py       thought_step, thought_loop, payoff tracking, meta-cognition
  metrics.py       coverage and payoff
  generators.py    procedural agent generator (clusters + escape routes)
  fitness.py       average payoff over many thoughts
  evolution.py     crossover, mutation, selection, the generational loop
  culture.py       grid-based belief transmission
  visualize.py     graph drawing, payoff curves, distributions, culture grid
notebooks/
  01_explore_graph.ipynb   interactive walkthrough
docs/
  Culture-Documentation.pdf
```

## Limitations & next steps

- Results are single stochastic runs; reliable claims would need many runs
  averaged.
- Evolution converges rather than innovating — NEAT-style speciation could push
  the fitness ceiling higher.
- Culture needs interaction-gating (not just imitation-gating) to produce
  distinct subcultures — the natural next experiment.
- This work independently re-derives ideas from established models
  (Axelrod 1997 on cultural dissemination; NEAT on evolving graph topology). It
  is a learning project and a demonstration of method, not a novel research
  contribution.

## License

MIT — see [`LICENSE`](LICENSE).
