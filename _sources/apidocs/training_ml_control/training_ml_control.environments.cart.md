# {py:mod}`training_ml_control.environments.cart`

```{py:module} training_ml_control.environments.cart
```

```{autodoc2-docstring} training_ml_control.environments.cart
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`CartEnv <training_ml_control.environments.cart.CartEnv>`
  - ```{autodoc2-docstring} training_ml_control.environments.cart.CartEnv
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`__all__ <training_ml_control.environments.cart.__all__>`
  - ```{autodoc2-docstring} training_ml_control.environments.cart.__all__
    :summary:
    ```
* - {py:obj}`logger <training_ml_control.environments.cart.logger>`
  - ```{autodoc2-docstring} training_ml_control.environments.cart.logger
    :summary:
    ```
````

### API

````{py:data} __all__
:canonical: training_ml_control.environments.cart.__all__
:value: >
   ['CartEnv']

```{autodoc2-docstring} training_ml_control.environments.cart.__all__
```

````

````{py:data} logger
:canonical: training_ml_control.environments.cart.logger
:value: >
   'getLogger(...)'

```{autodoc2-docstring} training_ml_control.environments.cart.logger
```

````

`````{py:class} CartEnv(render_mode: str | None = None, *, goal_velocity: float = 5, max_position: float = 200, max_speed: float = 10, max_force: float = 10, goal_position: float = 9.0)
:canonical: training_ml_control.environments.cart.CartEnv

Bases: {py:obj}`gymnasium.envs.classic_control.continuous_mountain_car.Continuous_MountainCarEnv`

```{autodoc2-docstring} training_ml_control.environments.cart.CartEnv
```

```{rubric} Initialization
```

```{autodoc2-docstring} training_ml_control.environments.cart.CartEnv.__init__
```

````{py:method} _height(xs: numpy.typing.NDArray) -> numpy.typing.NDArray
:canonical: training_ml_control.environments.cart.CartEnv._height

```{autodoc2-docstring} training_ml_control.environments.cart.CartEnv._height
```

````

````{py:method} step(action: numpy.typing.NDArray) -> tuple[numpy.typing.NDArray, float, bool, bool, dict]
:canonical: training_ml_control.environments.cart.CartEnv.step

````

````{py:method} render()
:canonical: training_ml_control.environments.cart.CartEnv.render

````

`````
