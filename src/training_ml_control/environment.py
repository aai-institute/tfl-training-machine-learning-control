from dataclasses import dataclass

import numpy as np
from gymnasium import Env
from gymnasium.wrappers import OrderEnforcing, PassiveEnvChecker, TimeLimit
from gymnasium.wrappers.render_collection import RenderCollection
from numpy.typing import NDArray

from training_ml_control.control import FeedbackController, Observer, RandomController
from training_ml_control.inverted_pendulum import InvertedPendulumEnv

__all__ = [
    "create_inverted_pendulum_environment",
    "simulate_environment",
]


def create_inverted_pendulum_environment(
    render_mode: str | None = "rgb_array",
    *,
    max_steps: int = 500,
    masspole: float = 0.1,
    masscart: float = 1.0,
    length: float = 1.0,
    x_threshold: float = 3,
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
) -> SimulationResults:
    if controller is None:
        controller = RandomController(env)

    observation, _ = env.reset()
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
            if env.render_mode is not None:
                frames = env.render()
            env.reset()
            break
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
