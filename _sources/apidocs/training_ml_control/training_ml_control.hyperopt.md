# {py:mod}`training_ml_control.hyperopt`

```{py:module} training_ml_control.hyperopt
```

```{autodoc2-docstring} training_ml_control.hyperopt
:allowtitles:
```

## Module Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`create_sindy_objective <training_ml_control.hyperopt.create_sindy_objective>`
  - ```{autodoc2-docstring} training_ml_control.hyperopt.create_sindy_objective
    :summary:
    ```
* - {py:obj}`create_dmd_objective <training_ml_control.hyperopt.create_dmd_objective>`
  - ```{autodoc2-docstring} training_ml_control.hyperopt.create_dmd_objective
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`__all__ <training_ml_control.hyperopt.__all__>`
  - ```{autodoc2-docstring} training_ml_control.hyperopt.__all__
    :summary:
    ```
````

### API

````{py:data} __all__
:canonical: training_ml_control.hyperopt.__all__
:value: >
   ['create_sindy_objective', 'create_dmd_objective']

```{autodoc2-docstring} training_ml_control.hyperopt.__all__
```

````

````{py:function} create_sindy_objective(env: gymnasium.Env, X_train: numpy.typing.NDArray, X_test: numpy.typing.NDArray, U_train: numpy.typing.NDArray, U_test: numpy.typing.NDArray, t_train: numpy.typing.NDArray) -> typing.Callable[[optuna.Trial], tuple[float, float]]
:canonical: training_ml_control.hyperopt.create_sindy_objective

```{autodoc2-docstring} training_ml_control.hyperopt.create_sindy_objective
```
````

````{py:function} create_dmd_objective(env: gymnasium.Env, X_train: numpy.typing.NDArray, X_test: numpy.typing.NDArray, U_train: numpy.typing.NDArray, U_test: numpy.typing.NDArray) -> typing.Callable[[optuna.Trial], float]
:canonical: training_ml_control.hyperopt.create_dmd_objective

```{autodoc2-docstring} training_ml_control.hyperopt.create_dmd_objective
```
````
