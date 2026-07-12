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