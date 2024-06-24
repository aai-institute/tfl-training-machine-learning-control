import re

import numpy as np
from casadi import constpow
from do_mpc.model import Model

__all__ = ["build_dmd_model"]


def build_dmd_model(dmd_model) -> Model:
    model = Model("continuous")

    variable_regex = re.compile(r"x\d+")
    feature_regex = re.compile(r"([xu]\d+)(\^(\d+))?")

    # Declare model state variables
    variables = dict()
    for feature_name in dmd_model.get_feature_names():
        for match in re.finditer(variable_regex, feature_name):
            variable_name = match.group()
            if variable_name in variables:
                continue
            variables[variable_name] = model.set_variable(
                var_type="_x", var_name=variable_name
            )

    # Declare model input variables
    inputs = []
    for i in range(dmd_model.B.shape[1]):
        variable_name = f"u{i}"
        inputs.append(model.set_variable(var_type="_u", var_name=variable_name))

    inputs = np.asarray(inputs)

    features = []
    for feature in dmd_model.get_feature_names():
        if feature == "1":
            features.append(1.0)
            continue

        matches = feature_regex.findall(feature)
        feature_expression = 1.0
        for match in matches:
            variable_name, _, power = match
            if not power:
                feature_expression *= variables[variable_name]
            else:
                feature_expression *= constpow(variables[variable_name], int(power))
        features.append(feature_expression)

    features = np.asarray(features)

    equations = dmd_model.A @ features + dmd_model.B @ inputs
    equations = dmd_model.C @ equations

    for i, equation in enumerate(equations):
        model.set_rhs(f"x{i}", equation)

    model.setup()
    return model
