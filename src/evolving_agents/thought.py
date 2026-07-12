import random


def thought_step(G, current_node):
    """From current_node, pick the next belief by a weighted random choice."""
    neighbors = list(G.successors(current_node))   
    if not neighbors:                               
        return None
    weights = [G[current_node][n]["weight"] for n in neighbors]
    return random.choices(neighbors, weights=weights, k=1)[0]
