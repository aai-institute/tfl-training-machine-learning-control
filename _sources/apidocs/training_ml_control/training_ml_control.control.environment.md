# {py:mod}`training_ml_control.control.environment`

```{py:module} training_ml_control.control.environment
```

```{autodoc2-docstring} training_ml_control.control.environment
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`InvertedPendulumEnvWithInitialAndCutoffAngle <training_ml_control.control.environment.InvertedPendulumEnvWithInitialAndCutoffAngle>`
  - ```{autodoc2-docstring} training_ml_control.control.environment.InvertedPendulumEnvWithInitialAndCutoffAngle
    :summary:
    ```
* - {py:obj}`MassSpringDamperEnv <training_ml_control.control.environment.MassSpringDamperEnv>`
  - ```{autodoc2-docstring} training_ml_control.control.environment.MassSpringDamperEnv
    :summary:
    ```
* - {py:obj}`FeedbackController <training_ml_control.control.environment.FeedbackController>`
  -
* - {py:obj}`EnvironmentSimulationResults <training_ml_control.control.environment.EnvironmentSimulationResults>`
  - ```{autodoc2-docstring} training_ml_control.control.environment.EnvironmentSimulationResults
    :summary:
    ```
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`show_video <training_ml_control.control.environment.show_video>`
  - ```{autodoc2-docstring} training_ml_control.control.environment.show_video
    :summary:
    ```
* - {py:obj}`create_inverted_pendulum_environment <training_ml_control.control.environment.create_inverted_pendulum_environment>`
  - ```{autodoc2-docstring} training_ml_control.control.environment.create_inverted_pendulum_environment
    :summary:
    ```
* - {py:obj}`create_mass_spring_damper_environment <training_ml_control.control.environment.create_mass_spring_damper_environment>`
  - ```{autodoc2-docstring} training_ml_control.control.environment.create_mass_spring_damper_environment
    :summary:
    ```
* - {py:obj}`simulate_environment <training_ml_control.control.environment.simulate_environment>`
  - ```{autodoc2-docstring} training_ml_control.control.environment.simulate_environment
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`__all__ <training_ml_control.control.environment.__all__>`
  - ```{autodoc2-docstring} training_ml_control.control.environment.__all__
    :summary:
    ```
* - {py:obj}`ASSETS_DIR <training_ml_control.control.environment.ASSETS_DIR>`
  - ```{autodoc2-docstring} training_ml_control.control.environment.ASSETS_DIR
    :summary:
    ```
````

### API

````{py:data} __all__
:canonical: training_ml_control.control.environment.__all__
:value: >
   ['show_video', 'create_inverted_pendulum_environment', 'create_mass_spring_damper_environment', 'sim...

```{autodoc2-docstring} training_ml_control.control.environment.__all__
```

````

````{py:data} ASSETS_DIR
:canonical: training_ml_control.control.environment.ASSETS_DIR
:value: >
   None

```{autodoc2-docstring} training_ml_control.control.environment.ASSETS_DIR
```

````

````{py:function} show_video(frames: list[numpy.typing.NDArray], fps: float) -> None
:canonical: training_ml_control.control.environment.show_video

```{autodoc2-docstring} training_ml_control.control.environment.show_video
```
````

````{py:function} create_inverted_pendulum_environment(render_mode: str | None = 'rgb_array', max_steps: int = 100, cutoff_angle: float = 0.8, initial_angle: float = 0.0) -> gymnasium.Env
:canonical: training_ml_control.control.environment.create_inverted_pendulum_environment

```{autodoc2-docstring} training_ml_control.control.environment.create_inverted_pendulum_environment
```
````

````{py:function} create_mass_spring_damper_environment(render_mode: str | None = 'rgb_array', max_steps: int = 100) -> gymnasium.Env
:canonical: training_ml_control.control.environment.create_mass_spring_damper_environment

```{autodoc2-docstring} training_ml_control.control.environment.create_mass_spring_damper_environment
```
````

`````{py:class} InvertedPendulumEnvWithInitialAndCutoffAngle(**kwargs)
:canonical: training_ml_control.control.environment.InvertedPendulumEnvWithInitialAndCutoffAngle

Bases: {py:obj}`gymnasium.envs.mujoco.inverted_pendulum_v4.InvertedPendulumEnv`

```{autodoc2-docstring} training_ml_control.control.environment.InvertedPendulumEnvWithInitialAndCutoffAngle
```

```{rubric} Initialization
```

```{autodoc2-docstring} training_ml_control.control.environment.InvertedPendulumEnvWithInitialAndCutoffAngle.__init__
```

````{py:method} step(a)
:canonical: training_ml_control.control.environment.InvertedPendulumEnvWithInitialAndCutoffAngle.step

````

`````

`````{py:class} MassSpringDamperEnv(**kwargs)
:canonical: training_ml_control.control.environment.MassSpringDamperEnv

Bases: {py:obj}`gymnasium.envs.mujoco.MujocoEnv`, {py:obj}`gymnasium.utils.EzPickle`

```{autodoc2-docstring} training_ml_control.control.environment.MassSpringDamperEnv
```

```{rubric} Initialization
```

```{autodoc2-docstring} training_ml_control.control.environment.MassSpringDamperEnv.__init__
```

````{py:attribute} metadata
:canonical: training_ml_control.control.environment.MassSpringDamperEnv.metadata
:type: typing.ClassVar
:value: >
   None

```{autodoc2-docstring} training_ml_control.control.environment.MassSpringDamperEnv.metadata
```

````

````{py:attribute} default_camera_config
:canonical: training_ml_control.control.environment.MassSpringDamperEnv.default_camera_config
:type: typing.ClassVar
:value: >
   None

```{autodoc2-docstring} training_ml_control.control.environment.MassSpringDamperEnv.default_camera_config
```

````

````{py:method} step(a)
:canonical: training_ml_control.control.environment.MassSpringDamperEnv.step

````

````{py:method} reset_model()
:canonical: training_ml_control.control.environment.MassSpringDamperEnv.reset_model

````

````{py:method} _get_obs()
:canonical: training_ml_control.control.environment.MassSpringDamperEnv._get_obs

```{autodoc2-docstring} training_ml_control.control.environment.MassSpringDamperEnv._get_obs
```

````

`````

`````{py:class} FeedbackController
:canonical: training_ml_control.control.environment.FeedbackController

Bases: {py:obj}`typing.Protocol`

````{py:method} act(observation: numpy.typing.NDArray) -> numpy.typing.NDArray
:canonical: training_ml_control.control.environment.FeedbackController.act

```{autodoc2-docstring} training_ml_control.control.environment.FeedbackController.act
```

````

`````

`````{py:class} EnvironmentSimulationResults
:canonical: training_ml_control.control.environment.EnvironmentSimulationResults

```{autodoc2-docstring} training_ml_control.control.environment.EnvironmentSimulationResults
```

````{py:attribute} frames
:canonical: training_ml_control.control.environment.EnvironmentSimulationResults.frames
:type: list[numpy.typing.NDArray]
:value: >
   None

```{autodoc2-docstring} training_ml_control.control.environment.EnvironmentSimulationResults.frames
```

````

````{py:attribute} observations
:canonical: training_ml_control.control.environment.EnvironmentSimulationResults.observations
:type: numpy.typing.NDArray
:value: >
   None

```{autodoc2-docstring} training_ml_control.control.environment.EnvironmentSimulationResults.observations
```

````

````{py:attribute} actions
:canonical: training_ml_control.control.environment.EnvironmentSimulationResults.actions
:type: numpy.typing.NDArray
:value: >
   None

```{autodoc2-docstring} training_ml_control.control.environment.EnvironmentSimulationResults.actions
```

````

`````

````{py:function} simulate_environment(env: gymnasium.Env, *, controller: training_ml_control.control.environment.FeedbackController, max_steps: int = 500) -> training_ml_control.control.environment.EnvironmentSimulationResults
:canonical: training_ml_control.control.environment.simulate_environment

```{autodoc2-docstring} training_ml_control.control.environment.simulate_environment
```
````
