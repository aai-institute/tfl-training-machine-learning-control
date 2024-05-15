import numpy as np
from gymnasium import spaces
from gymnasium.envs.classic_control.acrobot import AcrobotEnv, bound, rk4, wrap
from numpy import cos, pi
from numpy.typing import NDArray

__all__ = ["ContinuousAcrobotEnv"]


class ContinuousAcrobotEnv(AcrobotEnv):
    r"""The continuous acrobot environment problem is based on the classic problem.

    This class is a modified version of the `AcrobotEnv`
    environment from gymnasium that modifies that environment to taken continuous
    value for the action.

    ## Action Space

    The action is continuous, deterministic, and represents the torque applied
    on the actuated joint between the two links.

    +-----+---------------------------+-------------+-------------+
    | Num | Action                    | Control Min | Control Max |
    +=====+===========================+=============+=============+
    | 0   | Torque applied to the actuated joint | -1.0         | 1.0          |
    +-----+---------------------------+-------------+-------------+

    """

    def __init__(
        self,
        render_mode: str | None = None,
        max_torque: float = 1.0,
        *,
        torque_noise_max: float = 0.0,
        target_height: float = 1.0,
    ):
        self.render_mode = render_mode
        self.screen = None
        self.clock = None
        self.isopen = True

        self.torque_noise_max = torque_noise_max
        self.target_height = target_height
        self.max_torque = max_torque

        high = np.array(
            [1.0, 1.0, 1.0, 1.0, self.MAX_VEL_1, self.MAX_VEL_2], dtype=np.float32
        )
        low = -high
        self.observation_space = spaces.Box(low=low, high=high, dtype=np.float32)
        self.action_space = spaces.Box(
            low=-self.max_torque, high=self.max_torque, dtype=np.float32
        )
        self.state = None

    def step(self, a: NDArray) -> tuple[NDArray, float, bool, bool, dict]:
        s = self.state
        assert s is not None, "Call reset before using AcrobotEnv object."
        torque = a
        # Add noise to the force action
        if self.torque_noise_max > 0:
            torque += self.np_random.uniform(
                -self.torque_noise_max, self.torque_noise_max
            )

        # Now, augment the state with our force action so it can be passed to
        # _dsdt
        s_augmented = np.append(s, torque)

        ns = rk4(self._dsdt, s_augmented, [0, self.dt])

        ns[0] = wrap(ns[0], -pi, pi)
        ns[1] = wrap(ns[1], -pi, pi)
        ns[2] = bound(ns[2], -self.MAX_VEL_1, self.MAX_VEL_1)
        ns[3] = bound(ns[3], -self.MAX_VEL_2, self.MAX_VEL_2)
        self.state = ns
        terminated = self._terminal()
        reward = -1.0 if not terminated else 0.0

        if self.render_mode == "human":
            self.render()
        return (self._get_ob(), reward, terminated, False, {})

    def _terminal(self):
        s = self.state
        assert s is not None, "Call reset before using AcrobotEnv object."
        return bool(-cos(s[0]) - cos(s[1] + s[0]) > self.target_height)
