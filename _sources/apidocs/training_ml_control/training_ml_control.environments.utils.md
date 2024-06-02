# {py:mod}`training_ml_control.environments.utils`

```{py:module} training_ml_control.environments.utils
```

```{autodoc2-docstring} training_ml_control.environments.utils
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`SimulationResults <training_ml_control.environments.utils.SimulationResults>`
  - ```{autodoc2-docstring} training_ml_control.environments.utils.SimulationResults
    :summary:
    ```
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`create_cart_environment <training_ml_control.environments.utils.create_cart_environment>`
  - ```{autodoc2-docstring} training_ml_control.environments.utils.create_cart_environment
    :summary:
    ```
* - {py:obj}`create_pendulum_environment <training_ml_control.environments.utils.create_pendulum_environment>`
  - ```{autodoc2-docstring} training_ml_control.environments.utils.create_pendulum_environment
    :summary:
    ```
* - {py:obj}`create_grid_world_environment <training_ml_control.environments.utils.create_grid_world_environment>`
  - ```{autodoc2-docstring} training_ml_control.environments.utils.create_grid_world_environment
    :summary:
    ```
* - {py:obj}`create_inverted_pendulum_environment <training_ml_control.environments.utils.create_inverted_pendulum_environment>`
  - ```{autodoc2-docstring} training_ml_control.environments.utils.create_inverted_pendulum_environment
    :summary:
    ```
* - {py:obj}`simulate_environment <training_ml_control.environments.utils.simulate_environment>`
  - ```{autodoc2-docstring} training_ml_control.environments.utils.simulate_environment
    :summary:
    ```
* - {py:obj}`value_iteration <training_ml_control.environments.utils.value_iteration>`
  - ```{autodoc2-docstring} training_ml_control.environments.utils.value_iteration
    :summary:
    ```
* - {py:obj}`compute_best_path_and_actions_from_values <training_ml_control.environments.utils.compute_best_path_and_actions_from_values>`
  - ```{autodoc2-docstring} training_ml_control.environments.utils.compute_best_path_and_actions_from_values
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`__all__ <training_ml_control.environments.utils.__all__>`
  - ```{autodoc2-docstring} training_ml_control.environments.utils.__all__
    :summary:
    ```
````

### API

````{py:data} __all__
:canonical: training_ml_control.environments.utils.__all__
:value: >
   ['create_inverted_pendulum_environment', 'create_grid_world_environment', 'create_cart_environment',...

```{autodoc2-docstring} training_ml_control.environments.utils.__all__
```

````

````{py:function} create_cart_environment(render_mode: str | None = 'rgb_array', *, max_steps: int = 200, goal_velocity: float = 0, max_position: float = 10, max_speed: float = 10, max_force: float = 10, goal_position: float = 9.0) -> gymnasium.Env
:canonical: training_ml_control.environments.utils.create_cart_environment

```{autodoc2-docstring} training_ml_control.environments.utils.create_cart_environment
```
````

````{py:function} create_pendulum_environment(render_mode: str | None = 'rgb_array', *, max_steps: int = 200) -> gymnasium.Env
:canonical: training_ml_control.environments.utils.create_pendulum_environment

```{autodoc2-docstring} training_ml_control.environments.utils.create_pendulum_environment
```
````

````{py:function} create_grid_world_environment(render_mode: str | None = 'rgb_array', *, max_steps: int = 20) -> gymnasium.Env
:canonical: training_ml_control.environments.utils.create_grid_world_environment

```{autodoc2-docstring} training_ml_control.environments.utils.create_grid_world_environment
```
````

````{py:function} create_inverted_pendulum_environment(render_mode: str | None = 'rgb_array', *, max_steps: int = 500, masspole: float | None = None, masscart: float | None = None, length: float | None = None, x_threshold: float = 3, theta_initial: float = 0.0, theta_threshold: float = 24, force_max: float = 10.0) -> gymnasium.Env
:canonical: training_ml_control.environments.utils.create_inverted_pendulum_environment

```{autodoc2-docstring} training_ml_control.environments.utils.create_inverted_pendulum_environment
```
````

`````{py:class} SimulationResults
:canonical: training_ml_control.environments.utils.SimulationResults

```{autodoc2-docstring} training_ml_control.environments.utils.SimulationResults
```

````{py:attribute} frames
:canonical: training_ml_control.environments.utils.SimulationResults.frames
:type: list[numpy.typing.NDArray]
:value: >
   None

```{autodoc2-docstring} training_ml_control.environments.utils.SimulationResults.frames
```

````

````{py:attribute} observations
:canonical: training_ml_control.environments.utils.SimulationResults.observations
:type: numpy.typing.NDArray
:value: >
   None

```{autodoc2-docstring} training_ml_control.environments.utils.SimulationResults.observations
```

````

````{py:attribute} estimated_observations
:canonical: training_ml_control.environments.utils.SimulationResults.estimated_observations
:type: numpy.typing.NDArray
:value: >
   None

```{autodoc2-docstring} training_ml_control.environments.utils.SimulationResults.estimated_observations
```

````

````{py:attribute} actions
:canonical: training_ml_control.environments.utils.SimulationResults.actions
:type: numpy.typing.NDArray
:value: >
   None

```{autodoc2-docstring} training_ml_control.environments.utils.SimulationResults.actions
```

````

`````

````{py:function} simulate_environment(env: gymnasium.Env, *, max_steps: int = 500, controller: training_ml_control.control.FeedbackController | None = None, observer: training_ml_control.control.Observer | None = None, seed: int = 16) -> training_ml_control.environments.utils.SimulationResults
:canonical: training_ml_control.environments.utils.simulate_environment

```{autodoc2-docstring} training_ml_control.environments.utils.simulate_environment
```
````

````{py:function} value_iteration(G: networkx.DiGraph) -> dict[tuple[int, int], float]
:canonical: training_ml_control.environments.utils.value_iteration

```{autodoc2-docstring} training_ml_control.environments.utils.value_iteration
```
````

````{py:function} compute_best_path_and_actions_from_values(G: networkx.DiGraph, start_node: tuple[int, int], target_node: tuple[int, int], values: dict[tuple[int, int], float]) -> tuple[list[tuple[int, int]], list[int]]
:canonical: training_ml_control.environments.utils.compute_best_path_and_actions_from_values

```{autodoc2-docstring} training_ml_control.environments.utils.compute_best_path_and_actions_from_values
```
````
