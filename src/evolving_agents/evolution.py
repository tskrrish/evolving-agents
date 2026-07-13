import random
import networkx as nx
import statistics
from evolving_agents.fitness import mean_fitness


def crossover(parentA, parentB, rng):
    """Combine two parent graphs into a child.
    Nodes: union of both parents (values averaged where they share a node).
    Edges: shared edges kept (weights averaged); edges in only one parent
    kept with 50% chance — so unstable wiring can drop out."""
    child = nx.DiGraph()

    # nodes: take every node either parent has
    for n in set(parentA.nodes) | set(parentB.nodes):
        vals = []
        if n in parentA.nodes:
            vals.append(parentA.nodes[n]["value"])
        if n in parentB.nodes:
            vals.append(parentB.nodes[n]["value"])
        child.add_node(n, value=round(sum(vals) / len(vals), 2))

    # edges: consider every edge that appears in either parent
    for (a, b) in set(parentA.edges) | set(parentB.edges):
        inA = parentA.has_edge(a, b)
        inB = parentB.has_edge(a, b)
        if inA and inB:                          # both parents have it → keep, average weight
            w = (parentA[a][b]["weight"] + parentB[a][b]["weight"]) / 2
            child.add_edge(a, b, weight=round(w, 2))
        elif rng.random() < 0.5:                 # only one parent → 50% chance to inherit
            src = parentA if inA else parentB
            child.add_edge(a, b, weight=src[a][b]["weight"])

    return child


def mutate(G, rng, weight_rate=0.1, add_edge_rate=0.05, remove_edge_rate=0.02):
    """Return a mutated copy of G: jitter some weights, rarely add/remove an edge."""
    H = G.copy()

    # jitter weights: each edge has a `weight_rate` chance of a small change
    for (a, b) in list(H.edges):
        if rng.random() < weight_rate:
            new_w = max(0.1, H[a][b]["weight"] + rng.uniform(-0.5, 0.5))
            H[a][b]["weight"] = round(new_w, 2)

    # rarely add a brand-new edge (novel structure)
    nodes = list(H.nodes)
    if rng.random() < add_edge_rate and len(nodes) > 1:
        a, b = rng.choice(nodes), rng.choice(nodes)
        if a != b and not H.has_edge(a, b):
            H.add_edge(a, b, weight=round(rng.uniform(0.5, 1.5), 2))

    # rarely remove an edge — but never leave a node with no way out
    if rng.random() < remove_edge_rate and H.number_of_edges() > len(nodes):
        a, b = rng.choice(list(H.edges))
        if H.out_degree(a) > 1:                  # don't create a dead end
            H.remove_edge(a, b)

    return H




def next_generation(scored, rng, elite=2):
    """Build the next generation from a scored population.
    scored = list of (agent, fitness). Fitter agents reproduce more.
    The top `elite` agents pass through unchanged."""
    agents = [a for a, f in scored]
    fits = [max(0.01, f) for a, f in scored]     # weights for selection (must be positive)

    # elitism: carry the best few forward untouched, so the best never regresses
    ranked = sorted(scored, key=lambda x: x[1], reverse=True)
    new_pop = [a for a, f in ranked[:elite]]

    # fill the rest with children of fitness-proportionally chosen parents
    size = len(scored)
    while len(new_pop) < size:
        pa = random.choices(agents, weights=fits, k=1)[0]
        pb = random.choices(agents, weights=fits, k=1)[0]
        child = mutate(crossover(pa, pb, rng), rng)
        new_pop.append(child)

    return new_pop


def evolve(pop, generations, rng, n_thoughts=120):
    """Run evolution. Yields (generation, mean_fitness, best_fitness) each generation."""
    for gen in range(generations):
        scored = [(a, mean_fitness(a, n_thoughts=n_thoughts, seed=gen)) for a in pop]
        mean_f = statistics.mean(f for a, f in scored)
        best_f = max(f for a, f in scored)
        yield gen, mean_f, best_f
        pop = next_generation(scored, rng)