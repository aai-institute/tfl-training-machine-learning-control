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
    "SineController",
    "SumOfSineController",
    "RandomController",
    "build_lqr_controller",
    "build_mpc_controller",
]


class FeedbackController(Protocol):
    def control(self, measurement: NDArray) -> NDArray:
        ...


class Observer(Protocol):
    def observe(self, measurement: NDArray) -> NDArray:
        ...


class ConstantController:
    def __init__(self, u: NDArray = np.zeros(1)) -> None:
        self.u = u

    def act(self, measurement: NDArray) -> NDArray:
        return self.u


class SineController:
    def __init__(
        self, env: Env, u_max: NDArray = np.asarray([10]), frequency: float = 1
    ) -> None:
        self.dt = env.unwrapped.dt
        self.u_max = u_max
        self.frequency = frequency
        self.i = 0

    def act(self, measurement: NDArray) -> NDArray:
        t = self.dt * self.i
        self.i += 1
        u = self.u_max * np.sin(2 * np.pi * self.frequency * t)
        return u


class SumOfSineController:
    def __init__(
        self,
        env: Env,
        u_max: NDArray = np.asarray([10]),
        frequencies: list[float] = [1.0],
    ) -> None:
        self.dt = env.unwrapped.dt
        self.u_max = u_max
        self.frequencies = frequencies
        self.i = 0

    def act(self, measurement: NDArray) -> NDArray:
        t = self.dt * self.i
        self.i += 1
        u = np.asarray([0.0])
        for frequency in self.frequencies:
            u += np.sin(2 * np.pi * frequency * t)
        u *= self.u_max
        return u


class SchroederSweepController:
    def __init__(
        self,
        env: Env,
        u_max: NDArray = np.asarray([10]),
        n_time_steps: int = 200,
        input_power: float = 10,
        n_harmonics: int = 3,
    ) -> None:
        self.dt = env.unwrapped.dt
        self.u_max = u_max
        self.input_power = input_power
        self.n_time_steps = n_time_steps
        self.n_harmonics = n_harmonics
        self.amplitude = np.sqrt(self.input_power / self.n_harmonics)
        self.phis = np.zeros(self.n_harmonics)
        for k in range(1, self.n_harmonics):
            self.phis[k] = self.phis[k - 1] - np.pi * k**2 / self.n_time_steps
        self.i = 0

    def act(self, measurement: NDArray) -> NDArray:
        t = self.dt * self.i
        self.i += 1
        u = np.asarray([0.0])
        for k, phi in enumerate(self.phis):
            u += np.cos(2 * np.pi * (k + 1) * t + phi)
        u *= self.amplitude
        return u


class RandomController:
    def __init__(self, env: Env) -> None:
        self.action_space = env.action_space

    def act(self, measurment: NDArray) -> NDArray:
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
