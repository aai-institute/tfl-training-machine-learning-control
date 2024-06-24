"""
Original code taken from:
https://github.com/Farama-Foundation/Gymnasium/blob/f26cbe13e9ac20d43486032b7e9dd4b8f2c563dc/gymnasium/envs/classic_control/cartpole.py

MIT License:
https://github.com/Farama-Foundation/Gymnasium/blob/f26cbe13e9ac20d43486032b7e9dd4b8f2c563dc/LICENSE
"""
import logging
import math

import gymnasium as gym
import numpy as np
from gymnasium import spaces
from gymnasium.envs.classic_control.continuous_mountain_car import (
    Continuous_MountainCarEnv,
)
from gymnasium.error import DependencyNotInstalled
from numpy.typing import NDArray

__all__ = ["CartEnv"]

logger = logging.getLogger(__name__)


class CartEnv(Continuous_MountainCarEnv):
    r"""The cart, or double-integarator, problem is based on the classic problem
    in control theory. It is a simple cart that can move without friction
    to the left or to the right.

    $$
    \begin{array}{ll}
    \ddot {q} &= u(t)\\
    y &= q(t)
    \end{array}
    $$

    where $\displaystyle q(t),u(t)\in \mathbb {R}$.

    This class is a modified version of the `Continuous_MountainCarEnv`
    environment from gymnasium that modifies that environment to be flat.
    """

    def __init__(
        self,
        render_mode: str | None = None,
        *,
        goal_velocity: float = 5,
        max_position: float = 200,
        max_speed: float = 10,
        max_force: float = 10,
        goal_position: float = 9.0,
    ):
        self.min_position = -max_position
        self.max_position = max_position
        self.min_speed = -max_speed
        self.max_speed = max_speed
        self.min_action = -max_force
        self.max_action = max_force
        if abs(goal_position) >= max_position:
            raise ValueError(
                "Goal position should be smaller in magnitude than max position."
            )
        self.goal_position = goal_position
        self.goal_velocity = goal_velocity
        self.dt = 1 / self.metadata["render_fps"]

        self.low_state = np.array([self.min_position, self.min_speed], dtype=np.float32)
        self.high_state = np.array(
            [self.max_position, self.max_speed], dtype=np.float32
        )

        self.render_mode = render_mode

        self.screen_width = 600
        self.screen_height = 400
        self.screen = None
        self.clock = None
        self.isopen = True

        self.action_space = spaces.Box(
            low=self.min_action, high=self.max_action, shape=(1,), dtype=np.float32
        )
        self.observation_space = spaces.Box(
            low=self.low_state, high=self.high_state, dtype=np.float32
        )

    def _height(self, xs: NDArray) -> NDArray:
        # Constant height
        return np.ones_like(xs) * 0.55

    def step(self, action: NDArray) -> tuple[NDArray, float, bool, bool, dict]:
        position = self.state[0]
        velocity = self.state[1]
        force = min(max(action[0], self.min_action), self.max_action)

        velocity += force * self.dt
        if velocity > self.max_speed:
            velocity = self.max_speed
        if velocity < self.min_speed:
            velocity = self.min_speed
        position += velocity * self.dt
        if position > self.max_position:
            position = self.max_position
            velocity = 0
        if position < self.min_position:
            position = self.min_position
            velocity = 0

        # Convert a possible numpy bool to a Python bool.
        terminated = bool(
            abs(position) >= abs(self.goal_position)
            and abs(velocity) >= self.goal_velocity
        )

        reward = 0
        if terminated:
            reward = 100.0
        reward -= math.pow(action[0], 2) * 0.1

        self.state = np.array([position, velocity], dtype=np.float32)

        if self.render_mode == "human":
            self.render()
        return self.state, reward, terminated, False, {}

    def render(self):
        if self.render_mode is None:
            assert self.spec is not None
            gym.logger.warn(
                "You are calling render method without specifying any render mode. "
                "You can specify the render_mode at initialization, "
                f'e.g. gym.make("{self.spec.id}", render_mode="rgb_array")'
            )
            return

        try:
            import pygame
            from pygame import gfxdraw
        except ImportError as e:
            raise DependencyNotInstalled(
                "pygame is not installed, run `pip install gymnasium[classic-control]`"
            ) from e

        if self.screen is None:
            pygame.init()
            if self.render_mode == "human":
                pygame.display.init()
                self.screen = pygame.display.set_mode(
                    (self.screen_width, self.screen_height)
                )
            else:  # mode == "rgb_array":
                self.screen = pygame.Surface((self.screen_width, self.screen_height))
        if self.clock is None:
            self.clock = pygame.time.Clock()

        world_width = self.max_position - self.min_position
        scale = self.screen_width / world_width
        carwidth = 40
        carheight = 20

        self.surf = pygame.Surface((self.screen_width, self.screen_height))
        self.surf.fill((255, 255, 255))

        pos = self.state[0]

        xs = np.linspace(self.min_position, self.max_position, 100)
        ys = self._height(xs)
        xys = list(zip((xs - self.min_position) * scale, ys * scale))

        pygame.draw.aalines(self.surf, points=xys, closed=False, color=(0, 0, 0))

        clearance = 10

        l, r, t, b = -carwidth / 2, carwidth / 2, carheight, 0
        coords = []
        for c in [(l, b), (l, t), (r, t), (r, b)]:
            c = pygame.math.Vector2(c)
            coords.append(
                (
                    c[0] + (pos - self.min_position) * scale,
                    c[1] + clearance + self._height(pos) * scale,
                )
            )

        gfxdraw.aapolygon(self.surf, coords, (0, 0, 0))
        gfxdraw.filled_polygon(self.surf, coords, (0, 0, 0))

        for c in [(carwidth / 4, 0), (-carwidth / 4, 0)]:
            c = pygame.math.Vector2(c)
            wheel = (
                int(c[0] + (pos - self.min_position) * scale),
                int(c[1] + clearance + self._height(pos) * scale),
            )

            gfxdraw.aacircle(
                self.surf, wheel[0], wheel[1], int(carheight / 2.5), (128, 128, 128)
            )
            gfxdraw.filled_circle(
                self.surf, wheel[0], wheel[1], int(carheight / 2.5), (128, 128, 128)
            )

        flagx = int((self.goal_position - self.min_position) * scale)
        flagy1 = int(self._height(self.goal_position) * scale)
        flagy2 = flagy1 + 50
        gfxdraw.vline(self.surf, flagx, flagy1, flagy2, (0, 0, 0))

        gfxdraw.aapolygon(
            self.surf,
            [(flagx, flagy2), (flagx, flagy2 - 10), (flagx + 25, flagy2 - 5)],
            (204, 204, 0),
        )
        gfxdraw.filled_polygon(
            self.surf,
            [(flagx, flagy2), (flagx, flagy2 - 10), (flagx + 25, flagy2 - 5)],
            (204, 204, 0),
        )

        self.surf = pygame.transform.flip(self.surf, False, True)
        self.screen.blit(self.surf, (0, 0))
        if self.render_mode == "human":
            pygame.event.pump()
            self.clock.tick(self.metadata["render_fps"])
            pygame.display.flip()

        elif self.render_mode == "rgb_array":
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(self.screen)), axes=(1, 0, 2)
            )
