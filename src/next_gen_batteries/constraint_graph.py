from __future__ import annotations

from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
import networkx as nx


def build_constraint_graph() -> nx.DiGraph:
    """Build the starter constraint graph for the battery engineering roadmap."""
    graph = nx.DiGraph()

    collaboration = [
        ("Materials", "stabilize"),
        ("Interfaces", "control"),
        ("Electrolytes", "transport"),
        ("Manufacturing", "repeat"),
        ("Diagnostics", "measure"),
        ("Physics + AI", "predict"),
    ]

    spine = [
        "Energy-storage reactions",
        "Reaction selectivity",
        "Competing reactions",
        "Engineering constraints",
        "Battery limits",
        "Measured performance",
    ]

    for name, verb in collaboration:
        graph.add_node(name, kind="collaboration", verb=verb)
        graph.add_edge(name, "Reaction selectivity", relation=verb)

    for a, b in zip(spine, spine[1:]):
        graph.add_node(a, kind="spine")
        graph.add_node(b, kind="spine")
        graph.add_edge(a, b, relation="specifies")

    outcomes = ["capacity", "power", "safety", "lifetime", "cost"]
    for outcome in outcomes:
        graph.add_node(outcome.title(), kind="outcome")
        graph.add_edge("Measured performance", outcome.title(), relation="generalizes")

    return graph


def draw_constraint_graph(path: str | Path | None = None) -> None:
    """Draw a simple starter graph for use in notebooks and README drafts."""
    graph = build_constraint_graph()

    pos = {
        "Energy-storage reactions": (0, 5),
        "Reaction selectivity": (0, 4),
        "Competing reactions": (0, 3),
        "Engineering constraints": (0, 2),
        "Battery limits": (0, 1),
        "Measured performance": (0, 0),
        "Materials": (-3, 4.8),
        "Interfaces": (-3, 4.1),
        "Electrolytes": (-3, 3.4),
        "Manufacturing": (3, 4.8),
        "Diagnostics": (3, 4.1),
        "Physics + AI": (3, 3.4),
        "Capacity": (-2.4, -0.9),
        "Power": (-1.2, -1.2),
        "Safety": (0, -1.35),
        "Lifetime": (1.2, -1.2),
        "Cost": (2.4, -0.9),
    }

    plt.figure(figsize=(10, 8))
    nx.draw_networkx_edges(graph, pos, arrows=True, arrowstyle="-|>", arrowsize=14, width=1.2)
    nx.draw_networkx_labels(graph, pos, font_size=9)
    nx.draw_networkx_nodes(graph, pos, node_size=1800)
    plt.axis("off")
    plt.tight_layout()
    if path:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(path, dpi=200, bbox_inches="tight")
    plt.show()
