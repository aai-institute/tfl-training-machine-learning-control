import itertools
from copy import deepcopy

import matplotlib.pyplot as plt
import networkx as nx

__all__ = [
    "plot_optimality_principle_graph",
    "create_shortest_path_graph",
    "plot_shortest_path_graph",
    "plot_all_paths_graph",
]


def plot_optimality_principle_graph(
    n_stages: int = 5, n_nodes_per_stage: int = 3
) -> nx.DiGraph:
    """Plots optimality principle graph."""
    G = nx.DiGraph()
    G.add_node("initial_state")
    G.add_node("final_state")

    previous_stage_nodes = ["initial_state"]
    next_stage_nodes = [f"stage_0_node_{i}" for i in range(n_nodes_per_stage)]

    for stage in range(1, n_stages):
        for previous_node in previous_stage_nodes:
            for next_node in next_stage_nodes:
                G.add_edge(previous_node, next_node)
        previous_stage_nodes = next_stage_nodes
        next_stage_nodes = [f"stage_{stage}_node_{i}" for i in range(n_nodes_per_stage)]
    for previous_node in previous_stage_nodes:
        G.add_edge(previous_node, "final_state")

    for layer, nodes in enumerate(nx.topological_generations(G)):
        # `multipartite_layout` expects the layer as a node attribute, so add the
        # numeric layer value as a node attribute
        for node in nodes:
            G.nodes[node]["layer"] = layer

    shortest_path = nx.shortest_path(G, source="initial_state", target="final_state")
    shortest_path_edges = list(itertools.pairwise(shortest_path))

    options = {
        "node_size": 1000,
        "edgecolors": "black",
        "linewidths": 3,
    }

    node_color = []
    for node in G.nodes:
        if node == "initial_state":
            node_color.append("lightgreen")
        elif node == "final_state":
            node_color.append("xkcd:light red")
        elif node in shortest_path:
            node_color.append("lightblue")
        else:
            node_color.append("white")
    options["node_color"] = node_color
    # Compute the multipartite_layout using the "layer" node attribute
    pos = nx.multipartite_layout(G, subset_key="layer", scale=2, align="vertical")
    plt.figure(figsize=(14, 8))
    nx.draw_networkx_nodes(G, pos, **options)
    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=shortest_path_edges,
        edge_color="red",
        width=5,
    )
    other_edges = [edge for edge in G.edges if edge not in shortest_path_edges]
    nx.draw_networkx_edges(G, pos, edgelist=other_edges, edge_color="gray", width=1)
    ax = plt.gca()
    ax.margins(0.20)
    plt.axis("off")
    plt.show()


def create_shortest_path_graph() -> nx.DiGraph:
    """Create shortest-path problem graph."""
    G = nx.DiGraph()
    edge_list = [
        ("A", "B", 4),
        ("A", "C", 5),
        ("A", "D", 3),
        ("B", "D", 9),
        ("B", "E", 1),
        ("C", "F", 2),
        ("D", "F", 5),
        ("D", "G", 8),
        ("E", "G", 1),
        ("F", "G", 1),
    ]
    G.add_weighted_edges_from(edge_list)
    return G


def plot_shortest_path_graph(G: nx.DiGraph) -> None:
    """Plot shortest-path problem graph."""
    options = {
        "font_size": 20,
        "node_size": 1000,
        "node_color": "white",
        "edgecolors": "black",
        "linewidths": 3,
        "width": 2,
    }

    # explicitly set positions
    pos = {
        "A": (0, 0),
        "B": (1, -1),
        "C": (1, 1),
        "D": (2, 0),
        "E": (2, -1),
        "F": (3, 1),
        "G": (4, 0),
    }

    edge_labels = {(n1, n2): data["weight"] for n1, n2, data in G.edges(data=True)}

    nx.draw_networkx(G, pos, **options)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    ax = plt.gca()
    ax.margins(0.20)
    plt.axis("off")
    plt.show()


def plot_all_paths_graph(G: nx.DiGraph, *, show_solution: bool = False) -> None:
    """Plot all paths from A to G in shortest-path problem graph."""
    F = nx.DiGraph()
    for path in nx.all_simple_paths(G, source="A", target="G"):
        node_prefix = ""
        for n1, n2 in itertools.pairwise(path):
            node_prefix += n1
            weight = G.edges[(n1, n2)]["weight"]
            F.add_edge(node_prefix, node_prefix + n2, weight=weight)

    edge_label_options = {
        "font_size": 9,
    }

    edge_options = {
        "width": 2,
    }
    node_options = {
        "node_size": 1800,
        "node_color": "white",
        "edgecolors": "black",
        "linewidths": 1,
    }

    # explicitly set positions
    pos = {
        "A": (0, 0),
        "AB": (2, 8),
        "AC": (2, 0),
        "AD": (2, -8),
        "ABD": (4, 13),
        "ABE": (4, 6),
        "ACF": (4, -1),
        "ADF": (4, -8),
        "ABDF": (6, 18),
        "ABDG": (8, 11),
        "ABEG": (8, 3),
        "ACFG": (8, -4),
        "ADFG": (8, -11),
        "ABDFG": (8, 19),
        "ADG": (8, -19),
    }

    nx.draw_networkx_nodes(F, pos, **node_options)
    nx.draw_networkx_labels(F, pos)

    edge_labels = {(n1, n2): data["weight"] for n1, n2, data in F.edges(data=True)}

    if show_solution:
        shortest_path = nx.shortest_path(G, source="A", target="G", weight="weight")
        shortest_path = list(itertools.accumulate(shortest_path))
        shortest_path_edges = list(itertools.pairwise(shortest_path))
        nx.draw_networkx_edges(
            F,
            pos,
            edgelist=shortest_path_edges,
            edge_color="red",
            **edge_options,
        )
        other_edges = [edge for edge in F.edges if edge not in shortest_path_edges]
        nx.draw_networkx_edges(
            F, pos, edgelist=other_edges, edge_color="black", **edge_options
        )
        # Compute cost-to-go recursively
        # leaves = [node for node in F.nodes if not list(F.successors(node))]
    else:
        nx.draw_networkx_edges(F, pos, edge_color="black", **edge_options)

    nx.draw_networkx_edge_labels(F, pos, edge_labels=edge_labels, **edge_label_options)

    ax = plt.gca()
    ax.margins(0.05)
    plt.axis("off")
    plt.show()
