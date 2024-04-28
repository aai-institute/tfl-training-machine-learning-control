import do_mpc
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import HTML
from matplotlib.animation import FuncAnimation
from numpy.typing import NDArray

__all__ = [
    "plot_inverted_pendulum_results",
    "animate_inverted_pendulum_simulation",
    "animate_full_inverted_pendulum_simulation",
]


def plot_inverted_pendulum_results(
    T: NDArray,
    reference: float,
    observations: NDArray,
    actions: NDArray,
) -> None:
    """As its name suggests, this function plots the results
    of a run of the inverted pendulum environment.
    """
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, sharex=True)
    ax1.plot(T, observations[:, 0])
    ax1.hlines(reference, T[0], T[-1], "r")
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Angle")
    if observations.shape[1] == 2:
        ax2.plot(T, observations[:, 1])
    ax2.set_xlabel("Time")
    ax2.set_ylabel("Angular Velocity")
    ax3.plot(T[1:], actions)
    ax3.set_xlabel("Time")
    ax3.set_ylabel("Force")
    fig.tight_layout()


def animate_inverted_pendulum_simulation(
    data: do_mpc.data.MPCData | do_mpc.data.Data,
) -> HTML:
    """Animated plots of inverted pendulum simulation."""
    plt.close()
    plt.ioff()
    fig = plt.figure()
    graphics = do_mpc.graphics.Graphics(data)

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

    ax1.set_xlim(-1, 1)
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
        # Get the x,y coordinates of the bar for the given state x.
        x = x_arr[t_ind]
        line_x = np.array(
            [
                0,
                0.3 * np.sin(x[0]),
            ],
        )
        line_y = np.array(
            [
                0,
                0.3 * np.cos(x[0]),
            ],
        )
        line = np.stack([line_x, line_y])
        bar[0].set_data(line)
        graphics.plot_results(t_ind)
        if isinstance(data, do_mpc.data.MPCData):
            graphics.plot_predictions(t_ind)

    anim = FuncAnimation(
        fig, update, frames=len(data["_time"]), repeat=False, interval=100
    )
    return HTML(anim.to_html5_video())


def animate_full_inverted_pendulum_simulation(
    data: do_mpc.data.MPCData | do_mpc.data.Data,
) -> HTML:
    """Animated plots of full inverted pendulum simulation with angle and position."""
    plt.close()
    plt.ioff()
    fig = plt.figure()
    graphics = do_mpc.graphics.Graphics(data)

    ax1 = plt.subplot2grid((5, 2), (0, 0), rowspan=5)
    ax2 = plt.subplot2grid((5, 2), (0, 1))
    ax3 = plt.subplot2grid((5, 2), (1, 1))
    ax4 = plt.subplot2grid((5, 2), (2, 1))
    ax5 = plt.subplot2grid((5, 2), (3, 1))
    ax6 = plt.subplot2grid((5, 2), (4, 1))

    ax2.set_ylabel("$y$")
    ax3.set_ylabel("$\\theta$")
    ax4.set_ylabel("$\\dot{y}$")
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
    graphics.add_line(var_type="_x", var_name="theta", axis=ax3)
    graphics.add_line(var_type="_x", var_name="velocity", axis=ax4)
    graphics.add_line(var_type="_x", var_name="dtheta", axis=ax5)
    graphics.add_line(var_type="_u", var_name="force", axis=ax6)

    # reference
    ax2.axhline(0.0, color="red")
    ax3.axhline(0.0, color="red")

    # Inverted Pendulum
    ax1.axhline(0, color="black")
    bar = ax1.plot([], [], "-o", linewidth=5, markersize=10)

    ax1.set_xlim(-1, 1)
    ax1.set_ylim(-1, 1)
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
                x[0] + 0.3 * np.sin(x[1]),
            ],
        )
        line_y = np.array(
            [
                0,
                0.3 * np.cos(x[1]),
            ],
        )
        line = np.stack([line_x, line_y])
        bar[0].set_data(line)
        graphics.plot_results(t_ind)
        if isinstance(data, do_mpc.data.MPCData):
            graphics.plot_predictions(t_ind)

    anim = FuncAnimation(
        fig, update, frames=len(data["_time"]), repeat=False, interval=100
    )
    return HTML(anim.to_html5_video())
