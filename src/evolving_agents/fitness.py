import random
import statistics
from evolving_agents.thought import thought_loop_tracked


def fitness(G, n_thoughts=300, max_steps=25, seed=None):
    """Average final payoff over many thoughts, each from a random start node.
    This is how we measure how 'good' an agent's belief-graph wiring is."""
    rng = random.Random(seed)
    nodes = list(G.nodes)
    payoffs = []
    for _ in range(n_thoughts):
        start = rng.choice(nodes)
        _, curve = thought_loop_tracked(G, start, max_steps=max_steps)
        payoffs.append(curve[-1])
    return payoffs


def mean_fitness(G, **kwargs):
    return statistics.mean(fitness(G, **kwargs))