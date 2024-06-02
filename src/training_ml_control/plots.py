import matplotlib.pyplot as plt
import numpy as np
from do_mpc.data import Data, MPCData
from do_mpc.graphics import Graphics
from IPython.display import HTML
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle
from numpy.typing import NDArray

__all__ = [
    "plot_cart_results",
    "plot_inverted_pendulum_results",
    "animate_cart_simulation",
    "animate_inverted_pendulum_simulation",
    "animate_full_inverted_pendulum_simulation",
    "animate_pendulum_simulation",
]


def plot_cart_results(
    T: NDArray,
    reference: float,
    observations: NDArray,
    actions: NDArray,
) -> None:
    """As its name suggests, this function plots the results
    of a run of the cart environment.
    """
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, sharex=True)
    ax1.plot(T, observations[:, 0])
    ax1.hlines(reference, T[0], T[-1], "r")
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Position")
    if observations.shape[1] == 2:
        ax2.plot(T, observations[:, 1])
    ax2.set_xlabel("Time")
    ax2.set_ylabel("Velocity")
    ax3.plot(T[1:], actions)
    ax3.set_xlabel("Time")
    ax3.set_ylabel("Force")
    fig.tight_layout()


def plot_inverted_pendulum_results(
    T: NDArray,
    reference: float,
    observations: NDArray,
    actions: NDArray,
) -> None:
    """As its name suggests, this function plots the results
    of a run of the inverted pendulum environment.
    """
    fig, axes = plt.subplots(3, 2, sharex=True)
    axes = axes.ravel()

    axes[0].plot(T, observations[:, 0])
    axes[0].set_xlabel("Time")
    axes[0].set_ylabel("Position")

    axes[1].plot(T, observations[:, 1])
    axes[1].set_xlabel("Time")
    axes[1].set_ylabel("Velocity")

    axes[2].plot(T, observations[:, 2])
    axes[2].hlines(reference, T[0], T[-1], "r")
    axes[2].set_xlabel("Time")
    axes[2].set_ylabel("Angle")

    axes[3].plot(T, observations[:, 3])
    axes[3].set_xlabel("Time")
    axes[3].set_ylabel("Angular Velocity")

    axes[4].plot(T[1:], actions)
    axes[4].set_xlabel("Time")
    axes[4].set_ylabel("Force")
    fig.tight_layout()


def animate_cart_simulation(
    data: Data | MPCData,
    *,
    reference: float | None = None,
) -> HTML:
    """Animated plots of cart simulation."""
    plt.close()
    plt.ioff()
    fig = plt.figure()
    graphics = Graphics(data)

    ax1 = plt.subplot2grid((3, 2), (0, 0), rowspan=3)
    ax2 = plt.subplot2grid((3, 2), (0, 1))
    ax3 = plt.subplot2grid((3, 2), (1, 1))
    ax4 = plt.subplot2grid((3, 2), (2, 1))

    ax2.set_ylabel("Position $x$")
    ax3.set_ylabel("Velocity $\\dot{x}$")
    ax4.set_ylabel("Force $u$")

    # Axis on the right.
    for ax in [ax2, ax3, ax4]:
        ax.yaxis.set_label_position("right")
        ax.yaxis.tick_right()
        if ax != ax4:
            ax.xaxis.set_ticklabels([])

    ax4.set_xlabel("Time")

    graphics.add_line(var_type="_x", var_name="position", axis=ax2)
    graphics.add_line(var_type="_x", var_name="velocity", axis=ax3)
    graphics.add_line(var_type="_u", var_name="force", axis=ax4)

    # reference
    if reference is not None:
        ax2.axhline(reference, color="red")

    # Inverted Pendulum
    ax1.axhline(0, color="black")
    cart_rectangle = Rectangle((0, 0), 1, 0.1)
    ax1.add_patch(cart_rectangle)

    ax1.set_xlim(-10, 10)
    ax1.set_ylim(-1, 1)
    ax1.set_axis_off()

    fig.align_ylabels()
    fig.tight_layout()

    plt.ion()
    x_arr = data["_x"]
    u_arr = data["_u"]
    x_max = np.max(x_arr, axis=0)
    x_min = np.min(x_arr, axis=0)
    u_max = np.max(u_arr, axis=0)
    u_min = np.min(u_arr, axis=0)
    x_range = x_max - x_min
    u_range = u_max - u_min

    # Axis limits
    ax2.set_ylim(x_min[0] - 0.1 * x_range[0], x_max[0] + 0.1 * x_range[0])
    ax3.set_ylim(x_min[1] - 0.1 * x_range[1], x_max[1] + 0.1 * x_range[1])
    ax4.set_ylim(u_min[0] - 0.1 * u_range[0], u_max[0] + u_range[0])

    def update(t_ind):
        # Get the x,y coordinates of the cart for the given state x.
        x = x_arr[t_ind]
        cart_rectangle.set_x(x[0])
        graphics.plot_results(t_ind)
        if isinstance(data, MPCData):
            graphics.plot_predictions(t_ind)

    anim = FuncAnimation(
        fig, update, frames=len(data["_time"]), repeat=False, interval=100
    )
    return HTML(anim.to_html5_video())


def animate_inverted_pendulum_simulation(
    data: Data | MPCData,
) -> HTML:
    """Animated plots of inverted pendulum simulation."""
    plt.close()
    plt.ioff()
    fig = plt.figure()
    graphics = Graphics(data)

    ax1 = plt.subplot2grid((3, 2), (0, 0), rowspan=3)
    ax2 = plt.subplot2grid((3, 2), (0, 1))
    ax3 = plt.subplot2grid((3, 2), (1, 1))
    ax4 = plt.subplot2grid((3, 2), (2, 1))

    ax2.set_ylabel("$\\theta$")
    ax3.set_ylabel("$\\dot{\\theta}$")
    ax4.set_ylabel("Force")

    # Axis on the right.
    for ax in [ax2, ax3, ax4]:
        ax.yaxis.set_label_position("right")
        ax.yaxis.tick_right()
        if ax != ax4:
            ax.xaxis.set_ticklabels([])

    ax4.set_xlabel("Time")

    graphics.add_line(var_type="_x", var_name="theta", axis=ax2)
    graphics.add_line(var_type="_x", var_name="dtheta", axis=ax3)
    graphics.add_line(var_type="_u", var_name="force", axis=ax4)

    # reference
    ax2.axhline(0.0, color="red")

    # Inverted Pendulum
    ax1.axhline(0, color="black")
    bar = ax1.plot([], [], "-o", linewidth=5, markersize=10)

    ax1.set_xlim(-3, 3)
    ax1.set_ylim(-2, 2)
    ax1.set_axis_off()

    fig.align_ylabels()
    fig.tight_layout()

    plt.ion()
    x_arr = data["_x"]
    u_arr = data["_u"]
    x_max = np.max(x_arr, axis=0)
    x_min = np.min(x_arr, axis=0)
    u_max = np.max(u_arr, axis=0)
    u_min = np.min(u_arr, axis=0)
    x_range = x_max - x_min
    u_range = u_max - u_min

    # Axis limits
    ax2.set_ylim(x_min[0] - 0.1 * x_range[0], x_max[0] + 0.1 * x_range[0])
    ax3.set_ylim(x_min[1] - 0.1 * x_range[1], x_max[1] + 0.1 * x_range[1])
    ax4.set_ylim(u_min[0] - 0.1 * u_range[0], u_max[0] + u_range[0])

    def update(t_ind):
        # Get the x,y coordinates of the bar for the given state x.
        x = x_arr[t_ind]
        line_x = np.array(
            [
                0,
                0.7 * np.sin(x[0]),
            ],
        )
        line_y = np.array(
            [
                0,
                0.7 * np.cos(x[0]),
            ],
        )
        line = np.stack([line_x, line_y])
        bar[0].set_data(line)
        graphics.plot_results(t_ind)
        if isinstance(data, MPCData):
            graphics.plot_predictions(t_ind)

    anim = FuncAnimation(
        fig, update, frames=len(data["_time"]), repeat=False, interval=100
    )
    return HTML(anim.to_html5_video())


def animate_full_inverted_pendulum_simulation(
    data: Data | MPCData,
) -> HTML:
    """Animated plots of full inverted pendulum simulation with angle and position."""
    plt.close()
    plt.ioff()
    fig = plt.figure()
    graphics = Graphics(data)

    ax1 = plt.subplot2grid((5, 2), (0, 0), rowspan=5)
    ax2 = plt.subplot2grid((5, 2), (0, 1))
    ax3 = plt.subplot2grid((5, 2), (1, 1))
    ax4 = plt.subplot2grid((5, 2), (2, 1))
    ax5 = plt.subplot2grid((5, 2), (3, 1))
    ax6 = plt.subplot2grid((5, 2), (4, 1))

    ax2.set_ylabel("$x$")
    ax3.set_ylabel("$\\dot{x}$")
    ax4.set_ylabel("$\\theta$")
    ax5.set_ylabel("$\\dot{\\theta}$")
    ax6.set_ylabel("Force")

    # Axis on the right.
    for ax in [ax2, ax3, ax4, ax5, ax6]:
        ax.yaxis.set_label_position("right")
        ax.yaxis.tick_right()
        if ax != ax6:
            ax.xaxis.set_ticklabels([])

    ax6.set_xlabel("Time")

    graphics.add_line(var_type="_x", var_name="position", axis=ax2)
    graphics.add_line(var_type="_x", var_name="velocity", axis=ax3)
    graphics.add_line(var_type="_x", var_name="theta", axis=ax4)
    graphics.add_line(var_type="_x", var_name="dtheta", axis=ax5)
    graphics.add_line(var_type="_u", var_name="force", axis=ax6)

    # reference
    ax2.axhline(0.0, color="red")
    ax3.axhline(0.0, color="red")

    # Inverted Pendulum
    ax1.axhline(0, color="black")
    bar = ax1.plot([], [], "-o", linewidth=5, markersize=10)

    ax1.set_xlim(-3, 3)
    ax1.set_ylim(-2, 2)
    ax1.set_axis_off()

    fig.align_ylabels()
    fig.tight_layout()

    plt.ion()
    factor = 0.2
    x_arr = data["_x"]
    x_max = np.max(x_arr, axis=0)
    x_min = np.min(x_arr, axis=0)
    x_max, x_min = x_max + factor * (x_max - x_min), x_min - factor * (x_max - x_min)

    u_arr = data["_u"]
    u_max = np.max(u_arr, axis=0)
    u_min = np.min(u_arr, axis=0)
    u_max, u_min = u_max + factor * (u_max - u_min), u_min - factor * (u_max - u_min)

    # Axis limits
    ax2.set_ylim(x_min[0], x_max[0])
    ax3.set_ylim(x_min[1], x_max[1])
    ax4.set_ylim(x_min[2], x_max[2])
    ax5.set_ylim(x_min[3], x_max[3])
    ax6.set_ylim(u_min[0], u_max[0])

    def update(t_ind):
        # Get the x,y coordinates of the bar for the given state x.
        x = x_arr[t_ind]
        line_x = np.array(
            [
                x[0],
                x[0] + 0.7 * np.sin(x[2]),
            ],
        )
        line_y = np.array(
            [
                0,
                0.7 * np.cos(x[2]),
            ],
        )
        line = np.stack([line_x, line_y])
        bar[0].set_data(line)
        graphics.plot_results(t_ind)
        if isinstance(data, MPCData):
            graphics.plot_predictions(t_ind)

    anim = FuncAnimation(
        fig, update, frames=len(data["_time"]), repeat=False, interval=100
    )
    return HTML(anim.to_html5_video())


def animate_pendulum_simulation(
    data: Data | MPCData,
) -> HTML:
    """Animated plots of pendulum simulation."""
    plt.close()
    plt.ioff()
    plt.figure()
    graphics = Graphics(data)

    fig, axes = plt.subplots(2, 2, sharex=True)
    axes = axes.ravel()

    axes[0].set_ylabel(r"$\cos(\theta)$")
    axes[1].set_ylabel(r"$\sin(\theta)$")
    axes[2].set_ylabel(r"$\dot{\theta}$")
    axes[3].set_ylabel(r"$u$")

    graphics.add_line(var_type="_x", var_name="x0", axis=axes[0])
    graphics.add_line(var_type="_x", var_name="x1", axis=axes[1])
    graphics.add_line(var_type="_x", var_name="x2", axis=axes[2])
    graphics.add_line(var_type="_u", var_name="u0", axis=axes[3])

    fig.align_ylabels()
    fig.tight_layout()

    plt.ion()
    factor = 0.2
    x_arr = data["_x"]
    x_max = np.max(x_arr, axis=0)
    x_min = np.min(x_arr, axis=0)
    x_max, x_min = x_max + factor * (x_max - x_min), x_min - factor * (x_max - x_min)

    u_arr = data["_u"]
    u_max = np.max(u_arr, axis=0)
    u_min = np.min(u_arr, axis=0)
    u_max, u_min = u_max + factor * (u_max - u_min), u_min - factor * (u_max - u_min)

    # Axis limits
    axes[0].set_ylim(x_min[0], x_max[0])
    axes[1].set_ylim(x_min[1], x_max[1])
    axes[2].set_ylim(x_min[2], x_max[2])
    axes[3].set_ylim(u_min[0], u_max[0])

    def update(t_ind):
        graphics.plot_results(t_ind)
        if isinstance(data, MPCData):
            graphics.plot_predictions(t_ind)

    anim = FuncAnimation(
        fig, update, frames=len(data["_time"]), repeat=False, interval=100
    )
    return HTML(anim.to_html5_video())
