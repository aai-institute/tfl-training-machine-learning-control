# {py:mod}`training_ml_control.models.models`

```{py:module} training_ml_control.models.models
```

```{autodoc2-docstring} training_ml_control.models.models
:allowtitles:
```

## Module Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`build_cart_model <training_ml_control.models.models.build_cart_model>`
  - ```{autodoc2-docstring} training_ml_control.models.models.build_cart_model
    :summary:
    ```
* - {py:obj}`build_inverted_pendulum_linear_model <training_ml_control.models.models.build_inverted_pendulum_linear_model>`
  - ```{autodoc2-docstring} training_ml_control.models.models.build_inverted_pendulum_linear_model
    :summary:
    ```
* - {py:obj}`build_inverted_pendulum_nonlinear_model <training_ml_control.models.models.build_inverted_pendulum_nonlinear_model>`
  - ```{autodoc2-docstring} training_ml_control.models.models.build_inverted_pendulum_nonlinear_model
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`__all__ <training_ml_control.models.models.__all__>`
  - ```{autodoc2-docstring} training_ml_control.models.models.__all__
    :summary:
    ```
````

### API

````{py:data} __all__
:canonical: training_ml_control.models.models.__all__
:value: >
   ['build_cart_model', 'build_inverted_pendulum_linear_model', 'build_inverted_pendulum_nonlinear_mode...

```{autodoc2-docstring} training_ml_control.models.models.__all__
```

````

````{py:function} build_cart_model(env: training_ml_control.environments.cart.CartEnv) -> do_mpc.model.LinearModel
:canonical: training_ml_control.models.models.build_cart_model

```{autodoc2-docstring} training_ml_control.models.models.build_cart_model
```
````

````{py:function} build_inverted_pendulum_linear_model(env: training_ml_control.environments.inverted_pendulum.InvertedPendulumEnv) -> do_mpc.model.LinearModel
:canonical: training_ml_control.models.models.build_inverted_pendulum_linear_model

```{autodoc2-docstring} training_ml_control.models.models.build_inverted_pendulum_linear_model
```
````

````{py:function} build_inverted_pendulum_nonlinear_model(env: training_ml_control.environments.inverted_pendulum.InvertedPendulumEnv, *, with_uncertainty: bool = False) -> do_mpc.model.Model
:canonical: training_ml_control.models.models.build_inverted_pendulum_nonlinear_model

```{autodoc2-docstring} training_ml_control.models.models.build_inverted_pendulum_nonlinear_model
```
````
