from typing import Callable

import numpy as np
import optuna
import pykoopman as pk
import pysindy as ps
from gymnasium import Env
from numpy.typing import NDArray
from sklearn.metrics import mean_squared_error

__all__ = ["create_sindy_objective", "create_dmd_objective"]


def create_sindy_objective(
    env: Env,
    X_train: NDArray,
    X_test: NDArray,
    U_train: NDArray,
    U_test: NDArray,
    t_train: NDArray,
) -> Callable[[optuna.Trial], tuple[float, float]]:
    def objective(trial: optuna.Trial) -> tuple[float, float]:
        threshold = trial.suggest_float("threshold", 0.05, 0.5)
        alpha = trial.suggest_float("threshold", 0.01, 0.5)
        max_iter = trial.suggest_int("max_iter", 50, 300)

        opt = ps.STLSQ(threshold=threshold, max_iter=max_iter, alpha=alpha)

        feature_library_cls_name = trial.suggest_categorical(
            "feature_library", ["polynomial", "fourier", "hybrid"]
        )
        if feature_library_cls_name == "polynomial":
            degree = trial.suggest_int("degree", 1, 5)
            feature_library = ps.PolynomialLibrary(degree=degree)
        elif feature_library_cls_name == "fourier":
            n_frequencies = trial.suggest_int("n_frequencies", 1, 5)
            feature_library = ps.FourierLibrary(n_frequencies=n_frequencies)
        elif feature_library_cls_name == "hybrid":
            degree = trial.suggest_int("degree", 1, 5)
            n_frequencies = trial.suggest_int("n_frequencies", 1, 5)
            feature_library = ps.PolynomialLibrary(degree=degree) + ps.FourierLibrary(
                n_frequencies=n_frequencies
            )
        else:
            raise ValueError(f"Unknown feature_library: {feature_library_cls_name}")

        order = trial.suggest_int("order", 1, 3)
        differentiation_method = ps.FiniteDifference(order=order)

        model = ps.SINDy(
            optimizer=opt,
            feature_library=feature_library,
            differentiation_method=differentiation_method,
        )
        model.fit(X_train, u=U_train, t=t_train)
        score = model.score(
            X_test, u=U_test, t=env.dt, metric=mean_squared_error
        ).item()
        complexity = model.complexity
        coefficients = model.coefficients()
        coefficients_rows_all_zero_count = len(np.where(~coefficients.any(axis=1))[0])
        if coefficients_rows_all_zero_count > 0:
            raise optuna.TrialPruned()
        return score, complexity

    return objective


def create_dmd_objective(
    env: Env, X_train: NDArray, X_test: NDArray, U_train: NDArray, U_test: NDArray
) -> Callable[[optuna.Trial], float]:
    def objective(trial: optuna.Trial) -> float:
        observable_cls_name = trial.suggest_categorical(
            "observable", ["polynomial", "time-delay", "fourier"]
        )
        if observable_cls_name == "polynomial":
            degree = trial.suggest_int("degree", 1, 5)
            obsv = pk.observables.Polynomial(degree=degree)
        elif observable_cls_name == "time-delay":
            delay = trial.suggest_int("delay", 1, 5)
            n_delays = trial.suggest_int("n_delays", 1, 5)
            obsv = pk.observables.TimeDelay(delay=delay, n_delays=n_delays)
        elif observable_cls_name == "fourier":
            gamma = trial.suggest_float("gamma", 0.1, 2.0)
            D = trial.suggest_int("D", 1, 5)
            obsv = pk.observables.RandomFourierFeatures(
                include_state=True, gamma=gamma, D=D
            )
        else:
            raise ValueError(f"Unknown observable: {observable_cls_name}")

        EDMDc = pk.regression.EDMDc()
        model = pk.Koopman(observables=obsv, regressor=EDMDc)
        try:
            model.fit(X_train, u=U_train, dt=env.dt)
        except:
            raise optuna.TrialPruned()
        X_dmd = model.simulate(X_test[0], U_test, n_steps=X_test.shape[0] - 1)
        X_dmd = np.vstack([X_test[0][np.newaxis, :], X_dmd])

        score = mean_squared_error(X_test, X_dmd)
        return score

    return objective
