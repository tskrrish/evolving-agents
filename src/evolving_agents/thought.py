import random


#def thought_step(G, current_node):
#   """From current_node, pick the next belief by a weighted random choice."""
#  neighbors = list(G.successors(current_node))   
# if not neighbors:                               
#    return None
#weights = [G[current_node][n]["weight"] for n in neighbors]
#return random.choices(neighbors, weights=weights, k=1)[0]


def thought_step(G, current_node, bias_targets=None, bias_strength=0.0):
    """Pick the next belief by weighted random choice among outgoing edges.
    If bias_targets is given, edges leading to those beliefs are amplified
    by (1 + bias_strength) — used by the soft nudge to steer toward unvisited beliefs."""
    neighbors = list(G.successors(current_node))
    if not neighbors:
        return None
    weights = []
    for n in neighbors:
        w = G[current_node][n]["weight"]
        if bias_targets and n in bias_targets:   # this neighbor is a nudge target
            w *= (1.0 + bias_strength)            # make its edge more attractive
        weights.append(w)
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


def thought_loop_hard_jump(G, start_node, max_steps=12, patience=3):
    """Thought loop with a meta-cognitive monitor. If payoff stays flat for
    `patience` steps (a stall), teleport to the best unvisited belief.
    Returns (trace, curve, interventions)."""
    trace = [start_node]
    current = start_node
    seen = {start_node}
    cumulative = G.nodes[start_node]["value"]
    curve = [round(cumulative, 2)]
    interventions = []          # record where the monitor stepped in
    flat_for = 0                # how many steps payoff hasn't risen

    for step in range(max_steps):
        nxt = thought_step(G, current)
        if nxt is None:
            break
        if nxt not in seen:
            seen.add(nxt)
            cumulative += G.nodes[nxt]["value"]
            flat_for = 0        # payoff rose → reset the stall counter
        else:
            flat_for += 1       # payoff flat → stall grows
        trace.append(nxt)
        curve.append(round(cumulative, 2))
        current = nxt

        # --- META-COGNITION: detect stall, intervene with a hard jump ---
        if flat_for >= patience:
            unvisited = [n for n in G.nodes if n not in seen]
            if unvisited:
                # jump to the highest-value belief not yet reached
                target = max(unvisited, key=lambda n: G.nodes[n]["value"])
                interventions.append((step, current, target))
                seen.add(target)
                cumulative += G.nodes[target]["value"]
                trace.append(target)
                curve.append(round(cumulative, 2))
                current = target
                flat_for = 0    # give it a fresh start from the new belief
        # ----------------------------------------------------------------

    return trace, curve, interventions


def thought_loop_soft(G, start_node, max_steps=12, patience=3, bias_strength=2.0):
    """Thought loop with soft-nudge meta-cognition. On a stall, bias the walk
    toward unvisited positive-value beliefs instead of teleporting.
    Returns (trace, curve, interventions)."""
    trace = [start_node]
    current = start_node
    seen = {start_node}
    cumulative = G.nodes[start_node]["value"]
    curve = [round(cumulative, 2)]
    interventions = []
    flat_for = 0

    for step in range(max_steps):
        # if stalled, turn on a bias toward unvisited valuable beliefs
        if flat_for >= patience:
            bias = {n for n in G.nodes if n not in seen and G.nodes[n]["value"] > 0}
            if bias:
                interventions.append((step, current))
        else:
            bias = None

        nxt = thought_step(G, current, bias_targets=bias, bias_strength=bias_strength)
        if nxt is None:
            break
        if nxt not in seen:
            seen.add(nxt)
            cumulative += G.nodes[nxt]["value"]
            flat_for = 0
        else:
            flat_for += 1
        trace.append(nxt)
        curve.append(round(cumulative, 2))
        current = nxt

    return trace, curve, interventions