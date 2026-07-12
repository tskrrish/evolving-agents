import networkx as nx
import matplotlib.pyplot as plt



def build_belief_graph():
    G = nx.DiGraph()

    beliefs = {
        "survival": 5.0,
        "food": 3.0,
        "safety": 3.0,
        "rest": 2.0,
        "explore": 4.0,
        "danger": -2.0,
    }
    for name, val in beliefs.items():
        G.add_node(name, value=val)

    edges = [
        ("survival", "food",    3.0),
        ("survival", "danger",  2.0),
        ("food",     "explore", 2.0),
        ("food",     "rest",    1.0),
        ("danger",   "safety",  4.0),
        ("safety",   "rest",    2.0),
        ("rest",     "survival", 3.0),
        ("explore",  "danger",  1.5),
        ("explore",  "food",    1.5),
    ]
    G.add_weighted_edges_from(edges)
    return G