import itertools
from copy import deepcopy
from enum import IntEnum
from typing import Any, SupportsFloat

import matplotlib.pyplot as plt
import networkx as nx
from gymnasium import spaces
from gymnasium.core import ActType, ObsType
from minigrid.core.constants import OBJECT_TO_IDX, TILE_PIXELS
from minigrid.core.grid import Grid
from minigrid.core.mission import MissionSpace
from minigrid.core.world_object import Goal, Wall
from minigrid.minigrid_env import MiniGridEnv
from numpy.typing import NDArray

__all__ = ["GridWorldEnv", "plot_grid_graph", "plot_grid_all_paths_graph"]


class SimplifiedActions(IntEnum):
    right = 0
    down = 1
    left = 2
    up = 3


class SimplifiedGridEnv(MiniGridEnv):
    def __init__(
        self,
        mission_space: MissionSpace,
        grid_size: int | None = None,
        width: int | None = None,
        height: int | None = None,
        max_steps: int = 100,
        see_through_walls: bool = False,
        agent_view_size: int = 7,
        render_mode: str | None = None,
        screen_size: int | None = 640,
        highlight: bool = True,
        tile_size: int = TILE_PIXELS,
        agent_pov: bool = False,
    ):
        # Initialize mission
        self.mission = mission_space.sample()

        # Can't set both grid_size and width/height
        if grid_size:
            assert width is None and height is None
            width = grid_size
            height = grid_size
        assert width is not None and height is not None

        # Action enumeration for this environment
        self.actions = SimplifiedActions
        # Actions are discrete integer values
        self.action_space = spaces.Discrete(len(self.actions))

        # Number of cells (width and height) in the agent view
        assert agent_view_size % 2 == 1
        assert agent_view_size >= 3
        self.agent_view_size = agent_view_size

        # Observations are dictionaries containing an
        # encoding of the grid and a textual 'mission' string
        image_observation_space = spaces.Box(
            low=0,
            high=255,
            shape=(self.agent_view_size, self.agent_view_size, 3),
            dtype="uint8",
        )
        self.observation_space = spaces.Dict(
            {
                "image": image_observation_space,
                "mission": mission_space,
            }
        )

        # Movement vectors
        self.left_vector = (-1, 0)
        self.right_vector = (1, 0)
        self.up_vector = (0, -1)
        self.down_vector = (0, 1)

        # Range of possible rewards
        self.reward_range = (0, 1)

        self.screen_size = screen_size
        self.render_size = None
        self.window = None
        self.clock = None

        # Environment configuration
        self.width = width
        self.height = height

        assert isinstance(
            max_steps, int
        ), f"The argument max_steps must be an integer, got: {type(max_steps)}"
        self.max_steps = max_steps

        self.see_through_walls = see_through_walls

        # Current position and direction of the agent
        self.agent_pos: NDArray | tuple[int, int] = None
        self.agent_dir: int = None

        # Current grid and mission and carrying
        self.grid = Grid(width, height)
        self.carrying = None

        # Rendering attributes
        self.render_mode = render_mode
        self.highlight = highlight
        self.tile_size = tile_size
        self.agent_pov = agent_pov

    def step(
        self, action: ActType
    ) -> tuple[ObsType, SupportsFloat, bool, bool, dict[str, Any]]:
        self.step_count += 1

        reward = 0
        terminated = False
        truncated = False

        if action == self.actions.left:
            self.agent_dir = 2
            delta_vec = self.left_vector
        elif action == self.actions.right:
            self.agent_dir = 0
            delta_vec = self.right_vector
        elif action == self.actions.up:
            self.agent_dir = 3
            delta_vec = self.up_vector
        elif action == self.actions.down:
            self.agent_dir = 1
            delta_vec = self.down_vector
        else:
            raise ValueError(f"Unknown action: {action}")

        next_pos = (self.agent_pos[0] + delta_vec[0], self.agent_pos[1] + delta_vec[1])
        next_cell = self.grid.get(*next_pos)
        if next_cell is None or next_cell.can_overlap():
            self.agent_pos = tuple(next_pos)
        if next_cell is not None and next_cell.type == "goal":
            terminated = True
            reward = self._reward()
        if next_cell is not None and next_cell.type == "lava":
            terminated = True

        if self.step_count >= self.max_steps:
            truncated = True

        if self.render_mode == "human":
            self.render()

        obs = self.gen_obs()
        del obs["direction"]

        return obs, reward, terminated, truncated, {}


class GridWorldEnv(SimplifiedGridEnv):
    def __init__(
        self,
        max_steps: int | None = None,
        **kwargs,
    ):
        size = 8
        self.agent_start_pos = (size - 2, size - 2)
        self.agent_start_dir = 2

        mission_space = MissionSpace(mission_func=self._gen_mission)

        if max_steps is None:
            max_steps = 4 * size**2

        super().__init__(
            mission_space=mission_space,
            grid_size=size,
            # Set this to True for maximum speed
            see_through_walls=True,
            max_steps=max_steps,
            highlight=False,
            **kwargs,
        )

    @staticmethod
    def _gen_mission():
        return "grand mission"

    def _gen_grid(self, width: int, height: int) -> None:
        # Create an empty grid
        self.grid = Grid(width, height)
        # Generate the surrounding walls
        self.grid.wall_rect(0, 0, width, height)
        # Generate obstacles
        self.grid.set(5, 1, Wall())
        self.grid.set(1, 2, Wall())
        self.grid.set(3, 2, Wall())
        self.grid.set(6, 3, Wall())
        self.grid.set(2, 4, Wall())
        self.grid.set(4, 4, Wall())
        self.grid.set(4, 6, Wall())
        # Place a goal square
        self.put_obj(Goal(), 1, int(height / 2))
        # Place the agent
        if self.agent_start_pos is not None:
            self.agent_pos = self.agent_start_pos
            self.agent_dir = self.agent_start_dir
        else:
            self.place_agent()

        self.mission = "grand mission"

    def get_graph(self) -> nx.DiGraph:
        G = nx.Graph()
        grid_representation = self.grid.encode()
        # Add nodes
        start_node = self.agent_start_pos
        target_node: tuple[int, int] | None = None
        G.add_node(start_node, start_node=True, target_node=False)
        for i in range(1, grid_representation.shape[0]):
            for j in range(1, grid_representation.shape[1]):
                if grid_representation[i, j, 0] == OBJECT_TO_IDX["wall"]:
                    continue
                # Determine if current node is goal
                current_node = (i, j)
                if grid_representation[i, j, 0] == OBJECT_TO_IDX["goal"]:
                    target_node = current_node
                    G.add_node(current_node, start_node=False, target_node=True)
                elif current_node != start_node:
                    G.add_node(current_node, start_node=False, target_node=False)
                # Add edges to next nodes
                for next_i, next_j in [(i, j + 1), (i + 1, j)]:
                    if grid_representation[next_i, next_j, 0] != OBJECT_TO_IDX["wall"]:
                        next_node = (next_i, next_j)
                        G.add_edge(current_node, next_node, weight=1)
        # Convert to a directed graph
        F = nx.DiGraph()
        F.add_nodes_from((n, deepcopy(d)) for n, d in G.nodes.items())
        F.start_node = start_node
        F.target_node = target_node

        # Connect all paths from start node to end node
        for path in nx.all_shortest_paths(G, source=start_node, target=target_node):
            for n1, n2 in itertools.pairwise(path):
                if (n1, n2) in F.edges or (n2, n1) in F.edges:
                    continue
                # Determine action
                if n1[0] > n2[0]:
                    action = SimplifiedActions.left.value
                elif n1[0] < n2[0]:
                    action = SimplifiedActions.right.value
                elif n1[1] > n2[1]:
                    action = SimplifiedActions.up.value
                else:
                    action = SimplifiedActions.down.value
                F.add_edge(n1, n2, weight=1, action=action)
        # Connect all remaining nodes
        for node in F.nodes:
            for path in nx.all_shortest_paths(G, source=node, target=target_node):
                if len(path) <= 1:
                    continue
                n1, n2 = path[0], path[1]
                if (n1, n2) in F.edges or (n2, n1) in F.edges:
                    continue
                # Determine action
                if n1[0] > n2[0]:
                    action = SimplifiedActions.left.value
                elif n1[0] < n2[0]:
                    action = SimplifiedActions.right.value
                elif n1[1] > n2[1]:
                    action = SimplifiedActions.up.value
                else:
                    action = SimplifiedActions.down.value
                F.add_edge(n1, n2, weight=1, action=action)
        return F


def plot_grid_graph(G: nx.Graph, *, show_start_to_target_paths: bool = False) -> None:
    options = {
        "font_size": 10,
        "node_size": 1000,
        "edgecolors": "black",
        "linewidths": 3,
        "width": 2,
    }
    pos = {}
    node_color = []
    for node, attributes in dict(G.nodes).items():
        pos[node] = (node[0], -node[1])
        if attributes["start_node"] is True:
            node_color.append("xkcd:light red")
        elif attributes["target_node"] is True:
            node_color.append("lightgreen")
        else:
            node_color.append("white")
    options["node_color"] = node_color

    if show_start_to_target_paths:
        F = nx.DiGraph()
        F.add_nodes_from((n, deepcopy(d)) for n, d in G.nodes.items())
        start_node = G.start_node
        target_node = G.target_node
        for path in nx.all_simple_paths(
            G.to_undirected(), source=start_node, target=target_node, cutoff=len(G)
        ):
            for n1, n2 in itertools.pairwise(path):
                """
                if (n1, n2) in F.edges or (n2, n1) in F.edges:
                    continue
                """
                F.add_edge(n1, n2, weight=1)
        """
        F = nx.DiGraph()
        for node, next_nodes in nx.bfs_successors(G.to_undirected(), G.start_node):
            for next_node in next_nodes:
                F.add_edge(node, next_node, weight=1)
        """
    else:
        F = G.copy().to_undirected()
    plt.figure(figsize=(12, 12))
    nx.draw_networkx(F, pos, **options)
    edge_labels = {(n1, n2): data["weight"] for n1, n2, data in F.edges(data=True)}
    nx.draw_networkx_edge_labels(F, pos, edge_labels=edge_labels)
    ax = plt.gca()
    ax.margins(0.20)
    plt.axis("off")
    plt.show()


def plot_grid_all_paths_graph(G: nx.DiGraph, *, show_solution: bool = False) -> None:
    """Plot all paths from start_node to target_node in shortest-path problem graph."""
    F = nx.DiGraph()
    for path in nx.all_simple_edge_paths(G, source=G.start_node, target=G.target_node):
        node_prefix = []
        for n1, n2 in itertools.pairwise(path):
            node_prefix += [n1]
            try:
                weight = G.edges[(n1, n2)]["weight"]
            except KeyError:
                continue
            start_node = tuple(node_prefix)
            end_node = tuple(node_prefix + [n2])
            F.add_node(start_node, layer=0, label=n1)
            F.add_node(end_node, layer=0, label=n2)
            F.add_edge(start_node, end_node, weight=weight)

    edge_label_options = {
        "font_size": 6,
    }

    edge_options = {
        "width": 3,
    }

    node_color = []
    for node, attributes in F.nodes(data=True):
        if attributes["label"] == G.target_node:
            node_color.append("lightgreen")
        elif attributes["label"] == G.start_node:
            node_color.append("xkcd:light red")
        else:
            node_color.append("white")

    node_options = {
        "node_size": 600,
        "edgecolors": "black",
        "linewidths": 2,
        "node_color": node_color,
    }

    for layer, nodes in enumerate(nx.topological_generations(F)):
        # `multipartite_layout` expects the layer as a node attribute, so add the
        # numeric layer value as a node attribute
        for node in nodes:
            F.nodes[node]["layer"] = layer

    for node, attributes in F.nodes(data=True):
        if attributes["label"] == G.target_node:
            attributes["node_color"] = "red"

    # Compute the multipartite_layout using the "layer" node attribute
    pos = nx.multipartite_layout(F, subset_key="layer", scale=2, align="horizontal")
    # Flip the layout so the root node is on top
    for k in pos:
        pos[k][-1] *= -1

    node_labels = {}
    for node in F.nodes:
        node_labels[node] = node[-1]

    plt.subplots(figsize=(10, 10))

    nx.draw_networkx_nodes(F, pos, **node_options)
    nx.draw_networkx_labels(F, pos, font_size=8, labels=node_labels)

    edge_labels = {(n1, n2): data["weight"] for n1, n2, data in F.edges(data=True)}

    if show_solution:
        shortest_path = nx.shortest_path(
            G, source=G.start_node, target=G.target_node, weight="weight"
        )
        shortest_path = list(itertools.accumulate(map(lambda x: (x,), shortest_path)))
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
