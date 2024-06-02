import re

import numpy as np
from casadi import constpow
from do_mpc.model import Model

__all__ = ["build_sindy_model"]


def build_sindy_model(
    sindy_model,
) -> Model:
    model = Model("continuous")

    # Declare model variables
    variables = dict()
    for variable_name in sindy_model.feature_names:
        if variable_name.startswith("x"):
            variable = model.set_variable(var_type="_x", var_name=variable_name)
        else:
            variable = model.set_variable(var_type="_u", var_name=variable_name)
        variables[variable_name] = variable

    feature_regex = re.compile(r"([xu]\d+)(\^(\d+))?")

    features = []
    for feature in sindy_model.get_feature_names():
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
    equations = sindy_model.coefficients() @ features

    for i, equation in enumerate(equations):
        model.set_rhs(f"x{i}", equation)

    model.setup()
    return model
