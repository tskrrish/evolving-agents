import random


def thought_step(G, current_node):
    """From current_node, pick the next belief by a weighted random choice."""
    neighbors = list(G.successors(current_node))   
    if not neighbors:                               
        return None
    weights = [G[current_node][n]["weight"] for n in neighbors]
    return random.choices(neighbors, weights=weights, k=1)[0]


def thought_loop(G, start_node, max_steps=10):
    trace = [start_node]        # record of beliefs visited, in order
    current = start_node
    for _ in range(max_steps):
        nxt = thought_step(G, current)
        if nxt is None:         # hit a dead end, stop early
            break
        trace.append(nxt)
        current = nxt
    return trace

