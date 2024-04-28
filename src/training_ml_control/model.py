import casadi
import numpy as np
from do_mpc.model import LinearModel, Model

from training_ml_control.environments.cart import CartEnv
from training_ml_control.environments.inverted_pendulum import InvertedPendulumEnv

__all__ = ["build_cart_model", "build_inverted_pendulum_linear_model"]


def build_cart_model(env: CartEnv) -> LinearModel:
    # Dynamics matrix
    A = np.array(
        [
            [0, 1],
            [0, 0],
        ]
    )
    # Input matrix
    B = np.array([[0, 1]]).transpose()
    # Output matrices
    C = np.array(
        [
            [1, 0],
        ]
    )
    D = np.zeros(1)

    model = LinearModel("continuous")
    pos = model.set_variable(var_type="_x", var_name="position")
    dpos = model.set_variable(var_type="_x", var_name="velocity")
    model.set_variable(var_type="_u", var_name="force")  # Inertia
    # Energy
    E_kin = 0.5 * dpos**2
    model.set_expression("E_kinetic", E_kin)

    model.setup(A, B, C, D)
    model = model.discretize(env.dt)
    return model


def build_inverted_pendulum_linear_model(env: InvertedPendulumEnv) -> LinearModel:
    g, l, m, M = env.gravity, env.length, env.masspole, env.masscart
    # Dynamics matrix
    A = np.array(
        [
            [0, 1],
            [
                (M + m) * g / (m * l),
                0,
            ],
        ]
    )
    # Input matrix
    B = np.array([[0, -1 / (M * l)]]).transpose()
    # Output matrices
    C = np.array([[1, 0], [0, 1]])
    D = np.zeros(2)

    model = LinearModel("continuous")
    theta = model.set_variable(var_type="_x", var_name="theta")
    dtheta = model.set_variable(var_type="_x", var_name="dtheta")
    model.set_variable(var_type="_u", var_name="force")

    # Inertia
    J = (m * l**2) / 3
    # Energies
    E_kin = 0.5 * J * dtheta**2 + 0.5 * m * (
        (l * dtheta * casadi.cos(theta)) ** 2 + (l * dtheta * casadi.sin(theta)) ** 2
    )
    E_pot = m * g * l * casadi.cos(theta)

    model.set_expression("E_kinetic", E_kin)
    model.set_expression("E_potential", E_pot)
    model.setup(A, B, C, D)
    model = model.discretize(env.dt)
    return model
