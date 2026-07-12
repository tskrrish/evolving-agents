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

def thought_loop_tracked(G, start_node, max_steps=12):
    """Like thought_loop, but also returns the payoff curve:
    the cumulative payoff after each step. A flat stretch in the curve = a stall."""
    trace = [start_node]
    current = start_node
    seen = {start_node}
    cumulative = G.nodes[start_node]["value"]   # collect the start node's value
    curve = [round(cumulative, 2)]              # curve[0] = payoff after step 0

    for _ in range(max_steps):
        nxt = thought_step(G, current)
        if nxt is None:
            break
        if nxt not in seen:                     # first visit → collect value
            seen.add(nxt)
            cumulative += G.nodes[nxt]["value"]
        trace.append(nxt)
        curve.append(round(cumulative, 2))      # record running total every step
        current = nxt

    return trace, curve