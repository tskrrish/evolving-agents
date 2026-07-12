import random
import networkx as nx


def build_agent(n_nodes=50, n_clusters=5, escape_density=0.0, seed=None):
    """Procedurally generate a belief graph.
    Nodes are grouped into clusters wired as sealed rings; escape_density adds
    weak cross-cluster edges (0 = fully sealed/trapped, higher = more escape routes)."""
    rng = random.Random(seed)      # local RNG so results are reproducible per seed
    G = nx.DiGraph()

    # 1. create nodes with values (~15% negative, like 'danger'; rest positive)
    for i in range(n_nodes):
        if rng.random() < 0.15:
            val = -rng.uniform(1.0, 3.0)
        else:
            val = rng.uniform(0.5, 5.0)
        G.add_node(i, value=round(val, 2))

    # 2. partition nodes into clusters, wire each as a ring (a sealed loop)
    nodes = list(range(n_nodes))
    rng.shuffle(nodes)
    clusters = [nodes[i::n_clusters] for i in range(n_clusters)]
    for cluster in clusters:
        for a, b in zip(cluster, cluster[1:] + cluster[:1]):   # ring: last wraps to first
            G.add_edge(a, b, weight=round(rng.uniform(1.0, 4.0), 2))

    # 3. add weak escape edges between clusters, controlled by escape_density
    n_escape = int(escape_density * n_nodes)
    added, attempts = 0, 0
    while added < n_escape and attempts < n_escape * 20:
        attempts += 1
        a, b = rng.randrange(n_nodes), rng.randrange(n_nodes)
        if a != b and not G.has_edge(a, b):
            G.add_edge(a, b, weight=round(rng.uniform(0.5, 1.5), 2))
            added += 1

    return G