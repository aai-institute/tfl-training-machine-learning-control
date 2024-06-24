import casadi
import numpy as np
from do_mpc.model import LinearModel, Model

from training_ml_control.environments.cart import CartEnv
from training_ml_control.environments.inverted_pendulum import InvertedPendulumEnv

__all__ = [
    "build_cart_model",
    "build_inverted_pendulum_linear_model",
    "build_inverted_pendulum_nonlinear_model",
]


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
    C = np.array([[1, 0], [0, 1]])
    D = np.zeros(1)

    model = LinearModel("continuous")
    model.set_variable(var_type="_x", var_name="position")
    model.set_variable(var_type="_x", var_name="velocity")
    model.set_variable(var_type="_u", var_name="force")

    model.setup(A, B, C, D)
    model = model.discretize(env.dt)
    return model


def build_inverted_pendulum_linear_model(env: InvertedPendulumEnv) -> LinearModel:
    g, l, m_p, m_c = env.gravity, env.length, env.masspole, env.masscart
    # Dynamics matrix
    A = np.array(
        [
            [0, 1],
            [
                (m_c + m_p) * g / (m_c * l),
                0,
            ],
        ]
    )
    # Input matrix
    B = np.array([[0, -1 / (m_c * l)]]).transpose()
    # Output matrices
    C = np.array([[1, 0], [0, 1]])
    D = np.zeros(2)

    model = LinearModel("continuous")
    theta = model.set_variable(var_type="_x", var_name="theta")
    dtheta = model.set_variable(var_type="_x", var_name="dtheta")
    model.set_variable(var_type="_u", var_name="force")

    # Inertia
    J = (m_p * l**2) / 3
    # Energies
    E_kin = 0.5 * J * dtheta**2 + 0.5 * m_p * (
        (l * dtheta * casadi.cos(theta)) ** 2 + (l * dtheta * casadi.sin(theta)) ** 2
    )
    E_pot = m_p * g * l * casadi.cos(theta)

    model.set_expression("E_kinetic", E_kin)
    model.set_expression("E_potential", E_pot)
    model.setup(A, B, C, D)
    model = model.discretize(env.dt)
    return model


def build_inverted_pendulum_nonlinear_model(
    env: InvertedPendulumEnv, *, with_uncertainty: bool = False
) -> Model:
    g, l, m_p, m_c = env.gravity, env.length, env.masspole, env.masscart

    model = Model("continuous")
    pos = model.set_variable(var_type="_x", var_name="position")
    dpos = model.set_variable(var_type="_x", var_name="velocity")
    theta = model.set_variable(var_type="_x", var_name="theta")
    dtheta = model.set_variable(var_type="_x", var_name="dtheta")
    force = model.set_variable(var_type="_u", var_name="force")
    if with_uncertainty:
        # Uncertain parameters
        m_p = model.set_variable("_p", "m_p")

    total_mass = m_c + m_p
    half_length = l / 2
    polemass_length = m_p * half_length

    numerator = (total_mass) * g * casadi.sin(theta) - casadi.cos(theta) * (
        force + m_p * l * dtheta**2 * casadi.sin(theta)
    )
    denominator = (4 / 3) * (total_mass) * l - m_p * l * casadi.cos(theta) ** 2
    ddtheta = numerator / denominator

    numerator = m_c * g * casadi.cos(theta) * casadi.sin(theta) - (4 / 3) * (
        force + m_c * l * dtheta**2 * casadi.sin(theta)
    )
    denominator = m_c * casadi.cos(theta) ** 2 - (4 / 3) * (total_mass)
    ddpos = numerator / denominator

    model.set_rhs("position", dpos)
    model.set_rhs("velocity", ddpos)
    model.set_rhs("theta", dtheta)
    model.set_rhs("dtheta", ddtheta)

    # Inertia
    J = (m_p * l**2) / 3
    # Energies
    E_kin = (
        0.5 * J * dtheta**2
        + 0.5 * m_c * dpos**2
        + 0.5
        * m_p
        * (
            (dpos + l * dtheta * casadi.cos(theta)) ** 2
            + (l * dtheta * casadi.sin(theta)) ** 2
        )
    )
    E_pot = m_p * g * l * casadi.cos(theta)

    model.set_expression("E_kinetic", E_kin)
    model.set_expression("E_potential", E_pot)
    model.setup()
    return model
