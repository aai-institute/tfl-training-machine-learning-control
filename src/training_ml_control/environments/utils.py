from collections import defaultdict
from dataclasses import dataclass

import networkx as nx
import numpy as np
from gymnasium import Env
from gymnasium.envs.classic_control.pendulum import PendulumEnv
from gymnasium.wrappers import OrderEnforcing, PassiveEnvChecker, TimeLimit
from gymnasium.wrappers.render_collection import RenderCollection
from numpy.typing import NDArray

from training_ml_control.control import FeedbackController, Observer, RandomController
from training_ml_control.environments.cart import CartEnv
from training_ml_control.environments.grid_world import GridWorldEnv
from training_ml_control.environments.inverted_pendulum import InvertedPendulumEnv

__all__ = [
    "create_inverted_pendulum_environment",
    "create_grid_world_environment",
    "create_cart_environment",
    "create_pendulum_environment",
    "simulate_environment",
    "value_iteration",
    "compute_best_path_and_actions_from_values",
]


def create_cart_environment(
    render_mode: str | None = "rgb_array",
    *,
    max_steps: int = 200,
    goal_velocity: float = 0,
    max_position: float = 10,
    max_speed: float = 10,
    max_force: float = 10,
    goal_position: float = 9.0,
) -> Env:
    """Creates instance of CartEnv with some wrappers
    to ensure correctness, limit the number of steps and store rendered frames.
    """
    env = CartEnv(
        render_mode=render_mode,
        goal_velocity=goal_velocity,
        max_position=max_position,
        max_speed=max_speed,
        max_force=max_force,
        goal_position=goal_position,
    )
    env = TimeLimit(env, max_steps)
    # env = PassiveEnvChecker(env)
    env = OrderEnforcing(env)
    if render_mode is not None:
        env = RenderCollection(env)
    return env


def create_pendulum_environment(
    render_mode: str | None = "rgb_array",
    *,
    max_steps: int = 200,
) -> Env:
    """Creates instance of PendulumEnv with some wrappers
    to ensure correctness, limit the number of steps and store rendered frames.
    """
    env = PendulumEnv(render_mode=render_mode)
    env = TimeLimit(env, max_steps)
    # env = PassiveEnvChecker(env)
    env = OrderEnforcing(env)
    if render_mode is not None:
        env = RenderCollection(env)
    return env


def create_grid_world_environment(
    render_mode: str | None = "rgb_array",
    *,
    max_steps: int = 20,
) -> Env:
    """Creates instance of GridWorldEnv with some wrappers
    to ensure correctness, limit the number of steps and store rendered frames.
    """
    env = GridWorldEnv(render_mode=render_mode, max_steps=max_steps)
    # env = PassiveEnvChecker(env)
    env = OrderEnforcing(env)
    if render_mode is not None:
        env = RenderCollection(env)
    return env


def create_inverted_pendulum_environment(
    render_mode: str | None = "rgb_array",
    *,
    max_steps: int = 500,
    masspole: float | None = None,
    masscart: float | None = None,
    length: float | None = None,
    x_threshold: float = 3,
    theta_initial: float = 0.0,
    theta_threshold: float = 24,
    force_max: float = 10.0,
) -> Env:
    """Creates instance of InvertedPendulumEnv with some wrappers
    to ensure correctness, limit the number of steps and store rendered frames.

    Args:
        render_mode: Render mode for environment.
        max_steps: Maximum number of steps in the environment before termination.
        masspole: mass of the pole.
        masscart: mass of the cart.
        length: length of the pole.
        force_max: maximum absolute value for force applied to Cart.
        x_threshold: Threshold value for cart position.
        theta_threshold: Threshold value for pole angle.

    Returns:
        Instantiated and wrapped environment.
    """
    env = InvertedPendulumEnv(
        masspole=masspole,
        masscart=masscart,
        length=length,
        x_threshold=x_threshold,
        theta_threshold=theta_threshold,
        theta_initial=theta_initial,
        force_max=force_max,
        render_mode=render_mode,
    )
    env = PassiveEnvChecker(env)
    env = OrderEnforcing(env)
    env = TimeLimit(env, max_steps)
    if render_mode is not None:
        env = RenderCollection(env)
    return env


@dataclass
class SimulationResults:
    frames: list[NDArray]
    observations: NDArray
    estimated_observations: NDArray
    actions: NDArray


def simulate_environment(
    env: Env,
    *,
    max_steps: int = 500,
    controller: FeedbackController | None = None,
    observer: Observer | None = None,
    seed: int = 16,
) -> SimulationResults:
    if controller is None:
        controller = RandomController(env)

    observation, _ = env.reset(seed=seed)
    actions = []
    observations = [observation]
    estimated_observations = []
    frames = []

    if observer is not None:
        estimated_observation = observer.observe(observation)
        estimated_observations.append(estimated_observation)

    for _ in range(max_steps):
        action = controller.act(observation)
        observation, _, terminated, truncated, _ = env.step(action)

        observations.append(observation)
        actions.append(action)

        if observer is not None:
            estimated_observation = observer.observe(observation)
            estimated_observations.append(estimated_observation)

        # Check if we need to stop the simulation
        if terminated or truncated:
            break

    if env.render_mode is not None:
        frames = env.render()
    env.reset()
    env.close()

    actions = np.stack(actions)
    observations = np.stack(observations)
    if estimated_observations:
        estimated_observations = np.stack(estimated_observations)

    return SimulationResults(
        frames=frames,
        observations=observations,
        estimated_observations=estimated_observations,
        actions=actions,
    )


def value_iteration(G: nx.DiGraph) -> dict[tuple[int, int], float]:
    values = defaultdict(lambda: 0.0)

    delta = np.inf

    while delta > 0.0:
        delta = 0.0
        Q = defaultdict(lambda: defaultdict(lambda: 0.0))
        visited_nodes = []
        for node in G.nodes:
            if node in visited_nodes:
                continue
            visited_nodes.append(node)
            next_nodes = list(G.successors(node))
            if not next_nodes:
                continue
            for next_node in G.successors(node):
                new_value = 1.0 + values[next_node]
                Q[node][next_node] = new_value
            min_q = min(Q[node].values())
            delta = max(delta, abs(values[node] - min_q))
            values[node] = min_q
    return values


def compute_best_path_and_actions_from_values(
    G: nx.DiGraph,
    start_node: tuple[int, int],
    target_node: tuple[int, int],
    values: dict[tuple[int, int], float],
) -> tuple[list[tuple[int, int]], list[int]]:
    best_path = [start_node]
    actions = []

    current_node = start_node
    while current_node != target_node:
        next_nodes = list(G.successors(current_node))
        if not next_nodes:
            break
        current_values = defaultdict(lambda: 0.0)
        for next_node in G.successors(current_node):
            value = 1.0 + values[next_node]
            current_values[next_node] = value
        best_next_node = min(current_values, key=current_values.get)
        best_path.append(current_node)
        action = G.edges[(current_node, best_next_node)].get("action")
        actions.append(action)
        current_node = best_next_node
    return best_path, actions
