import random
import statistics
from itertools import product
from evolving_agents.fitness import mean_fitness
from evolving_agents.generators import build_agent     

def graph_similarity(g1, g2):
    """How similar two agents are: fraction of edges they share 
    1.0 = identical wiring, 0.0 = no shared edges."""
    e1, e2 = set(g1.edges), set(g2.edges)
    if not e1 and not e2:
        return 1.0
    return len(e1 & e2) / len(e1 | e2)     # shared edges / total distinct edges


def transmit(fitter, weaker, rng):
    """The weaker agent copies one edge it lacks from the fitter agent.
    This is 'copy-from-fitter' — imitating whoever's doing better."""
    candidates = [e for e in fitter.edges if not weaker.has_edge(*e)]
    if not candidates:
        return
    a, b = rng.choice(candidates)
    weaker.add_edge(a, b, weight=fitter[a][b]["weight"])

def run_culture(grid=5, rounds=30, n_thoughts=60, seed=0):
    """Agents on a grid×grid lattice exchange beliefs with neighbors each round.
    Yields per-round measurements so you can watch culture form (or not)."""
    rng = random.Random(seed)
    coords = list(product(range(grid), range(grid)))    # every (x, y) cell

    # place a random agent in each cell (mix of sealed and open wiring)
    pop = {}
    for c in coords:
        dens = rng.choice([0.0, 0.2, 0.4])
        pop[c] = build_agent(30, n_clusters=4, escape_density=dens,
                             seed=rng.randint(1, 99999))

    def neighbors(x, y):
        out = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:   # up/down/left/right
            nx_, ny_ = x + dx, y + dy
            if 0 <= nx_ < grid and 0 <= ny_ < grid:
                out.append((nx_, ny_))
        return out

    for r in range(rounds):
        # score everyone this round
        scores = {c: mean_fitness(pop[c], n_thoughts=n_thoughts) for c in coords}

        # each cell interacts with one random neighbor; fitter teaches weaker
        for c in coords:
            nb = rng.choice(neighbors(*c))
            if scores[c] >= scores[nb]:
                transmit(pop[c], pop[nb], rng)      # c is fitter → teaches nb
            else:
                transmit(pop[nb], pop[c], rng)      # nb is fitter → teaches c

        # measure clustering: neighbor similarity vs random-pair similarity
        nb_sims = [graph_similarity(pop[c], pop[nb])
                   for c in coords for nb in neighbors(*c)]
        rand_sims = []
        for _ in range(200):
            a, b = rng.choice(coords), rng.choice(coords)
            if a != b:
                rand_sims.append(graph_similarity(pop[a], pop[b]))

        clustering = statistics.mean(nb_sims) - statistics.mean(rand_sims)
        yield {
            "round": r,
            "neighbor_sim": statistics.mean(nb_sims),
            "random_sim": statistics.mean(rand_sims),
            "clustering": clustering,
        }

def run_culture_with_snapshot(grid=5, rounds=30, n_thoughts=60, seed=0):
    """Same as run_culture, but returns (history, final_pop, coords) so we can
    visualize the final grid of agents."""
    rng = random.Random(seed)
    coords = list(product(range(grid), range(grid)))

    pop = {}
    for c in coords:
        dens = rng.choice([0.0, 0.2, 0.4])
        pop[c] = build_agent(30, n_clusters=4, escape_density=dens,
                             seed=rng.randint(1, 99999))

    def neighbors(x, y):
        out = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx_, ny_ = x + dx, y + dy
            if 0 <= nx_ < grid and 0 <= ny_ < grid:
                out.append((nx_, ny_))
        return out

    history = []
    for r in range(rounds):
        scores = {c: mean_fitness(pop[c], n_thoughts=n_thoughts) for c in coords}
        for c in coords:
            nb = rng.choice(neighbors(*c))
            if scores[c] >= scores[nb]:
                transmit(pop[c], pop[nb], rng)
            else:
                transmit(pop[nb], pop[c], rng)
        nb_sims = [graph_similarity(pop[c], pop[nb])
                   for c in coords for nb in neighbors(*c)]
        rand_sims = []
        for _ in range(200):
            a, b = rng.choice(coords), rng.choice(coords)
            if a != b:
                rand_sims.append(graph_similarity(pop[a], pop[b]))
        history.append({
            "round": r,
            "neighbor_sim": statistics.mean(nb_sims),
            "random_sim": statistics.mean(rand_sims),
            "clustering": statistics.mean(nb_sims) - statistics.mean(rand_sims),
        })

    return history, pop, coords