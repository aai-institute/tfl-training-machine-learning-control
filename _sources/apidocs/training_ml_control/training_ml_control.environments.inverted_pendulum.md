# {py:mod}`training_ml_control.environments.inverted_pendulum`

```{py:module} training_ml_control.environments.inverted_pendulum
```

```{autodoc2-docstring} training_ml_control.environments.inverted_pendulum
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`InvertedPendulumEnv <training_ml_control.environments.inverted_pendulum.InvertedPendulumEnv>`
  - ```{autodoc2-docstring} training_ml_control.environments.inverted_pendulum.InvertedPendulumEnv
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`__all__ <training_ml_control.environments.inverted_pendulum.__all__>`
  - ```{autodoc2-docstring} training_ml_control.environments.inverted_pendulum.__all__
    :summary:
    ```
* - {py:obj}`logger <training_ml_control.environments.inverted_pendulum.logger>`
  - ```{autodoc2-docstring} training_ml_control.environments.inverted_pendulum.logger
    :summary:
    ```
````

### API

````{py:data} __all__
:canonical: training_ml_control.environments.inverted_pendulum.__all__
:value: >
   ['InvertedPendulumEnv']

```{autodoc2-docstring} training_ml_control.environments.inverted_pendulum.__all__
```

````

````{py:data} logger
:canonical: training_ml_control.environments.inverted_pendulum.logger
:value: >
   'getLogger(...)'

```{autodoc2-docstring} training_ml_control.environments.inverted_pendulum.logger
```

````

`````{py:class} InvertedPendulumEnv(render_mode: typing.Optional[str] = None, *, masspole: float | None = None, masscart: float | None = None, length: float | None = None, theta_initial: float = 0.0, x_threshold: float = 3, theta_threshold: float = 24, force_max: float = 30.0)
:canonical: training_ml_control.environments.inverted_pendulum.InvertedPendulumEnv

Bases: {py:obj}`gymnasium.envs.classic_control.cartpole.CartPoleEnv`

```{autodoc2-docstring} training_ml_control.environments.inverted_pendulum.InvertedPendulumEnv
```

```{rubric} Initialization
```

```{autodoc2-docstring} training_ml_control.environments.inverted_pendulum.InvertedPendulumEnv.__init__
```

````{py:attribute} DEFAULT_MASSPOLE
:canonical: training_ml_control.environments.inverted_pendulum.InvertedPendulumEnv.DEFAULT_MASSPOLE
:value: >
   0.5

```{autodoc2-docstring} training_ml_control.environments.inverted_pendulum.InvertedPendulumEnv.DEFAULT_MASSPOLE
```

````

````{py:attribute} DEFAULT_MASSCART
:canonical: training_ml_control.environments.inverted_pendulum.InvertedPendulumEnv.DEFAULT_MASSCART
:value: >
   1.0

```{autodoc2-docstring} training_ml_control.environments.inverted_pendulum.InvertedPendulumEnv.DEFAULT_MASSCART
```

````

````{py:attribute} DEFAULT_LENGTH
:canonical: training_ml_control.environments.inverted_pendulum.InvertedPendulumEnv.DEFAULT_LENGTH
:value: >
   0.7

```{autodoc2-docstring} training_ml_control.environments.inverted_pendulum.InvertedPendulumEnv.DEFAULT_LENGTH
```

````

````{py:method} step(action: float) -> tuple[numpy.typing.NDArray, float, bool, bool, dict]
:canonical: training_ml_control.environments.inverted_pendulum.InvertedPendulumEnv.step

````

````{py:method} reset(*, seed: typing.Optional[int] = None, options: typing.Optional[dict] = None) -> tuple[numpy.typing.NDArray, dict]
:canonical: training_ml_control.environments.inverted_pendulum.InvertedPendulumEnv.reset

````

`````
