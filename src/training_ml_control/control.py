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
    "build_mpc_controller",
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


def build_mpc_controller(
    model: Model,
    t_step: float,
    n_horizon: int | None,
    terminal_cost,
    stage_cost,
    x_limits: NDArray,
    u_limits: NDArray,
    force_penalty: float,
    *,
    uncertainty_values: dict[str, NDArray] | None = None,
) -> MPC:
    mpc = MPC(model)
    mpc_params = {
        "n_horizon": n_horizon,
        "t_step": t_step,
        "state_discretization": "collocation",
        "collocation_type": "radau",
        "collocation_deg": 3,
        "collocation_ni": 1,
        "store_full_solution": True,
        # Use MA27 linear solver in ipopt for faster calculations:
        "nlpsol_opts": {"ipopt.linear_solver": "mumps"},
    }
    mpc.set_param(**mpc_params)
    mpc.set_objective(mterm=terminal_cost, lterm=stage_cost)
    mpc.set_rterm(force=force_penalty)
    # lower and upper bounds of the position
    mpc.bounds["lower", "_x", "position"] = x_limits[0]
    mpc.bounds["upper", "_x", "position"] = x_limits[1]
    # lower and upper bounds of the input
    mpc.bounds["lower", "_u", "force"] = u_limits[0]
    mpc.bounds["upper", "_u", "force"] = u_limits[1]
    # Parameter uncertainty
    if uncertainty_values is not None:
        mpc.set_uncertainty_values(**uncertainty_values)
    mpc.setup()
    return mpc
