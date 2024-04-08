"""
Original code taken from:
https://github.com/Farama-Foundation/Gymnasium/blob/f26cbe13e9ac20d43486032b7e9dd4b8f2c563dc/gymnasium/envs/classic_control/cartpole.py

MIT License:
https://github.com/Farama-Foundation/Gymnasium/blob/f26cbe13e9ac20d43486032b7e9dd4b8f2c563dc/LICENSE
"""
import logging
import math
from typing import Optional

import numpy as np
from gymnasium import spaces
from gymnasium.envs.classic_control import utils
from gymnasium.envs.classic_control.cartpole import CartPoleEnv
from numpy.typing import NDArray

__all__ = ["InvertedPendulumEnv"]


logger = logging.getLogger(__name__)


class InvertedPendulumEnv(CartPoleEnv):
    """
    Description
    -----------

    The inverted pendulum problem is based on the classic problem in control theory.
    The system consists of an inverted pole attached at one end to a cart, and the other end being free.
    The pole can rotate around its fixed point and the cart can move horizontally.
    The pole starts by default in a random upright position and the goal is to move the cart
    to keep it upright.

        **Note** This environment is a modified version of the CartPole environment.
        It allows configuring most relevant parameters of the system (e.g. cart mass,
        pole mass, pole length) and it uses a continuous action space instead of
        a discrete one.

    Action Space
    ============

    The action is a `ndarray` with shape `(1,)` representing the force applied to the cart.

    +-----+---------------------------+-------------+-------------+
    | Num | Action                    | Control Min | Control Max |
    +=====+===========================+=============+=============+
    | 0   | Force applied on the cart | -10         | 10          |
    +-----+---------------------------+-------------+-------------+

    Observation Space
    =================

    The observation is a `ndarray` with shape `(4,)` where the elements correspond to the following:

    +-----+-----------------------------------------------+------+-----+
    | Num | Observation                                   | Min  | Max |
    +=====+===============================================+======+=====+
    | 0   | position of the cart along the linear surface | -3   | 3   |
    | 1   | linear velocity of the cart                   | -Inf | Inf |
    | 2   | vertical angle of the pole on the cart        | -24  | 24  |
    | 3   | angular velocity of the pole on the cart      | -Inf | Inf |
    +-----+-----------------------------------------------+------+-----+

    Rewards
    =======

    The goal is to make the inverted pendulum remain upright (within a certain angle limit)
    as long as possible - as such a reward of +1 is awarded for each timestep that
    the pole is upright.

    Starting State
    ==============

    All observations start in state
    (0.0, 0.0, 0.0, 0.0) with a uniform noise in the range
    of [-0.01, 0.01] added to the values for stochasticity.

    Episode End
    -----------

    The episode ends when any of the following happens:

    1. Termination: Any of the state space values is no longer finite.
    2. Termination: The absolute value of the vertical angle between the pole
            and the cart are greater than a threshold value (which defaults to 24 degrees).


    :param masspole: mass of the pole.
    :param masscart: mass of the cart.
    :param length: length of the pole.
    :param x_threshold: threshold for cart position.
    :param theta_threshold: threshold for pole angle.
    :param force_max: maximum absolute value for force applied to Cart.

    """

    def __init__(
        self,
        render_mode: Optional[str] = None,
        *,
        masspole: float = 0.1,
        masscart: float = 1.0,
        length: float = 1.0,
        x_threshold: float = 3,
        theta_threshold: float = 24,
        force_max: float = 30.0,
    ) -> None:
        super().__init__()
        self.gravity = 9.81
        self.masscart = masscart
        self.masspole = masspole
        self.total_mass = self.masspole + self.masscart
        self.length = length
        self.half_length = self.length / 2
        self.polemass_length = self.masspole * self.half_length
        self.dt = 0.02
        self.kinematics_integrator = "euler"

        # Angle at which to fail the episode
        self.theta_threshold_radians = math.radians(theta_threshold)
        # Cart position at which to fail the episode
        self.x_threshold = x_threshold
        # Maximum absolute value of force applied on Cart
        self.force_max = force_max

        # Angle limit set to 2 * theta_threshold_radians so failing observation
        # is still within bounds.
        high = np.array(
            [
                self.x_threshold * 2,
                np.finfo(np.float32).max,
                self.theta_threshold_radians * 2,
                np.finfo(np.float32).max,
            ],
            dtype=np.float32,
        )

        self.action_space = spaces.Box(
            -self.force_max, self.force_max, dtype=np.float32
        )
        self.observation_space = spaces.Box(-high, high, dtype=np.float32)

        self.render_mode = render_mode

        self.screen_width = 600
        self.screen_height = 400
        self.screen = None
        self.clock = None
        self.isopen = True
        self.state = None

        self.steps_beyond_terminated = None

        self.init_state = np.array([0.0, 0.0, 0.0, 0.0])
        self.state = self.init_state.copy()

    def step(self, action: float) -> tuple[NDArray, float, bool, bool, dict]:
        if self.state is None:
            raise RuntimeError("Call reset before using step method.")
        x, x_dot, theta, theta_dot = self.state
        force = np.clip(action, -self.force_max, self.force_max).item()
        costheta = math.cos(theta)
        sintheta = math.sin(theta)

        # For the interested reader:
        # https://coneural.org/florian/papers/05_cart_pole.pdf
        temp = (
            force + self.polemass_length * theta_dot**2 * sintheta
        ) / self.total_mass
        thetaacc = (self.gravity * sintheta - costheta * temp) / (
            self.half_length
            * (4.0 / 3.0 - self.masspole * costheta**2 / self.total_mass)
        )
        xacc = temp - self.polemass_length * thetaacc * costheta / self.total_mass

        if self.kinematics_integrator == "euler":
            x = x + self.dt * x_dot
            x_dot = x_dot + self.dt * xacc
            theta = theta + self.dt * theta_dot
            theta_dot = theta_dot + self.dt * thetaacc
        else:  # semi-implicit euler
            x_dot = x_dot + self.dt * xacc
            x = x + self.dt * x_dot
            theta_dot = theta_dot + self.dt * thetaacc
            theta = theta + self.dt * theta_dot

        self.state = (x, x_dot, theta, theta_dot)

        terminated = bool(
            x < -self.x_threshold
            or x > self.x_threshold
            or theta < -self.theta_threshold_radians
            or theta > self.theta_threshold_radians
        )

        if not terminated:
            reward = 1.0
        elif self.steps_beyond_terminated is None:
            # Pole just fell!
            self.steps_beyond_terminated = 0
            reward = 1.0
        else:
            if self.steps_beyond_terminated == 0:
                logger.warning(
                    "You are calling 'step()' even though this "
                    "environment has already returned terminated = True. You "
                    "should always call 'reset()' once you receive 'terminated = "
                    "True' -- any further steps are undefined behavior."
                )
            self.steps_beyond_terminated += 1
            reward = 0.0

        if self.render_mode == "human":
            self.render()
        return np.asarray(self.state, dtype=np.float32), reward, terminated, False, {}

    def reset(
        self,
        *,
        seed: Optional[int] = None,
        options: Optional[dict] = None,
    ) -> tuple[NDArray, dict]:
        super().reset(seed=seed)
        # Note that if you use custom reset bounds, it may lead to out-of-bound
        # state/observations.
        low, high = utils.maybe_parse_reset_bounds(
            options, -0.01, 0.01  # default low
        )  # default high
        self.state = self.init_state + self.np_random.uniform(
            low=low, high=high, size=(4,)
        )
        self.steps_beyond_terminated = None

        if self.render_mode == "human":
            self.render()
        return np.array(self.state, dtype=np.float32), {}
