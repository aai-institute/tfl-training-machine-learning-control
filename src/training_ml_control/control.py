from typing import Protocol

import numpy as np
from do_mpc.controller import LQR, MPC
from do_mpc.model import LinearModel, Model
from gymnasium import Env
from numpy.typing import NDArray

__all__ = [
    "FeedbackController",
    "Observer",
    "ConstantController",
    "RandomController",
    "build_lqr_controller",
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


def build_lqr_controller(
    model: LinearModel,
    t_step: float,
    n_horizon: int | None,
    setpoint: NDArray,
    Q: NDArray,
    R: NDArray,
) -> LQR:
    lqr = LQR(model)
    lqr.settings.t_step = t_step
    lqr.settings.n_horizon = n_horizon
    lqr.set_objective(Q=Q, R=R)
    lqr.setup()
    lqr.set_setpoint(setpoint)
    return lqr
