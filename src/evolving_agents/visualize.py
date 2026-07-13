import networkx as nx
import matplotlib.pyplot as plt

def draw_graph(G, path=None, title="Belief graph"):
   
    pos = nx.spring_layout(G, seed=42)
 
    node_colors = []
    for n in G.nodes:
        val = G.nodes[n]["value"]
        node_colors.append("#8ecf9e" if val >= 0 else "#e69595")
 
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1600)
    nx.draw_networkx_labels(G, pos, font_size=9)
    nx.draw_networkx_edges(G, pos, edge_color="#cccccc",
                           arrows=True, arrowsize=18, node_size=1600)
 
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)
 
    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges,
                               edge_color="red", width=2.5,
                               arrows=True, arrowsize=18, node_size=1600)
        title = f"{title}: {' -> '.join(path)}"
 
    plt.title(title, fontsize=10)
    plt.axis("off")          
    plt.tight_layout()
    plt.show()              
 
def draw_payoff_curves(curves, labels=None):
    """Plot one or more payoff curves. Each curve is a list of cumulative
    payoffs over steps. A flat stretch = the thought stalled."""
    plt.figure(figsize=(8, 5))
    for i, curve in enumerate(curves):
        label = labels[i] if labels else f"thought {i+1}"
        plt.plot(range(len(curve)), curve, marker="o", label=label)
    plt.xlabel("step")
    plt.ylabel("cumulative payoff")
    plt.title("Payoff curves (flat stretch = a stall)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def draw_payoff_distributions(datasets, labels):
    """Plot histograms of final-payoff distributions for several approaches,
    side by side. Each dataset is a list of final payoffs (e.g. 500 numbers)."""
    fig, axes = plt.subplots(1, len(datasets), figsize=(5 * len(datasets), 4),
                             sharey=True)
    if len(datasets) == 1:
        axes = [axes]
    for ax, data, label in zip(axes, datasets, labels):
        ax.hist(data, bins=20, range=(7, 16), color="#6a9fd4", edgecolor="white")
        mean = sum(data) / len(data)
        ax.axvline(mean, color="red", linestyle="--", linewidth=1.5,
                   label=f"mean {mean:.2f}")
        ax.set_title(label)
        ax.set_xlabel("final payoff")
        ax.legend()
    axes[0].set_ylabel("number of thoughts (of 500)")
    plt.tight_layout()
    plt.show()

def draw_evolution(history):
    """Plot fitness over generations. history = list of (gen, mean, best)."""
    gens = [h[0] for h in history]
    means = [h[1] for h in history]
    bests = [h[2] for h in history]
    plt.figure(figsize=(8, 5))
    plt.plot(gens, means, marker="o", label="mean fitness")
    plt.plot(gens, bests, marker="s", label="best fitness")
    plt.xlabel("generation")
    plt.ylabel("fitness")
    plt.title("Evolution: fitness over generations")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


import networkx as nx   # (already at top of visualize.py)


def draw_culture_grid(pop, coords, grid, threshold=0.15):
    """Color each grid cell by its cultural group. Two agents are the 'same
    culture' if their wiring similarity exceeds `threshold`. Contiguous similar
    cells form regions — visible as same-colored patches."""
    from evolving_agents.culture import graph_similarity

    # 1. build a similarity graph: connect cells whose agents are similar enough
    sim_graph = nx.Graph()
    sim_graph.add_nodes_from(coords)
    for c in coords:
        x, y = c
        for dx, dy in [(1, 0), (0, 1)]:                  # check right & down neighbors
            nb = (x + dx, y + dy)
            if nb in pop and graph_similarity(pop[c], pop[nb]) > threshold:
                sim_graph.add_edge(c, nb)

    # 2. find connected groups (each group = one "culture")
    groups = {}
    for i, component in enumerate(nx.connected_components(sim_graph)):
        for cell in component:
            groups[cell] = i
    n_groups = len(set(groups.values()))

    # 3. build a 2D array of group-ids and draw it as a colored grid
    grid_map = [[groups[(x, y)] for x in range(grid)] for y in range(grid)]

    plt.figure(figsize=(6, 6))
    plt.imshow(grid_map, cmap="tab20", origin="upper")
    plt.title(f"Cultural regions ({n_groups} distinct groups, threshold={threshold})")
    # annotate each cell with its group number
    for y in range(grid):
        for x in range(grid):
            plt.text(x, y, str(grid_map[y][x]), ha="center", va="center",
                     color="white", fontsize=9)
    plt.xticks(range(grid))
    plt.yticks(range(grid))
    plt.tight_layout()
    plt.show()
    return n_groups