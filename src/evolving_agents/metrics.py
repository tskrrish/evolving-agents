import random

def coverage(G, trace):
    """Fraction of all beliefs the thought touched (distinct nodes / total)."""
    return round(len(set(trace)) / G.number_of_nodes(), 2)

def thought_payoff(G, trace):
    collected = 0.0
    seen = set()
    for node in trace:
        if node not in seen:        # first time reaching this belief
            seen.add(node)
            collected += G.nodes[node]["value"]
        # revisits fall through and collect nothing
    return round(collected, 2)