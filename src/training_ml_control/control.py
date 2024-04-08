from typing import Protocol

import numpy as np
from gymnasium import Env
from numpy.typing import NDArray

__all__ = [
    "FeedbackController",
    "Observer",
    "ConstantController",
    "RandomController",
]


class FeedbackController(Protocol):
    def control(self, observation: NDArray) -> NDArray:
        ...


class Observer(Protocol):
    def observe(self, measrument: NDArray) -> NDArray:
        ...


class ConstantController:
    def __init__(self, u: NDArray = np.zeros(1)) -> None:
        self.u = u

    def act(self, observation: NDArray) -> NDArray:
        return self.u


class RandomController:
    def __init__(self, env: Env) -> None:
        self.action_space = env.action_space

    def act(self, observation: NDArray) -> NDArray:
        return self.action_space.sample()
