# {py:mod}`training_ml_control.control`

```{py:module} training_ml_control.control
```

```{autodoc2-docstring} training_ml_control.control
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`FeedbackController <training_ml_control.control.FeedbackController>`
  -
* - {py:obj}`Observer <training_ml_control.control.Observer>`
  -
* - {py:obj}`ConstantController <training_ml_control.control.ConstantController>`
  - ```{autodoc2-docstring} training_ml_control.control.ConstantController
    :summary:
    ```
* - {py:obj}`SineController <training_ml_control.control.SineController>`
  - ```{autodoc2-docstring} training_ml_control.control.SineController
    :summary:
    ```
* - {py:obj}`SumOfSineController <training_ml_control.control.SumOfSineController>`
  - ```{autodoc2-docstring} training_ml_control.control.SumOfSineController
    :summary:
    ```
* - {py:obj}`SchroederSweepController <training_ml_control.control.SchroederSweepController>`
  - ```{autodoc2-docstring} training_ml_control.control.SchroederSweepController
    :summary:
    ```
* - {py:obj}`PRBSController <training_ml_control.control.PRBSController>`
  - ```{autodoc2-docstring} training_ml_control.control.PRBSController
    :summary:
    ```
* - {py:obj}`RandomController <training_ml_control.control.RandomController>`
  - ```{autodoc2-docstring} training_ml_control.control.RandomController
    :summary:
    ```
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`build_lqr_controller <training_ml_control.control.build_lqr_controller>`
  - ```{autodoc2-docstring} training_ml_control.control.build_lqr_controller
    :summary:
    ```
* - {py:obj}`build_mpc_controller <training_ml_control.control.build_mpc_controller>`
  - ```{autodoc2-docstring} training_ml_control.control.build_mpc_controller
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`__all__ <training_ml_control.control.__all__>`
  - ```{autodoc2-docstring} training_ml_control.control.__all__
    :summary:
    ```
````

### API

````{py:data} __all__
:canonical: training_ml_control.control.__all__
:value: >
   ['FeedbackController', 'Observer', 'ConstantController', 'SineController', 'SumOfSineController', 'S...

```{autodoc2-docstring} training_ml_control.control.__all__
```

````

`````{py:class} FeedbackController
:canonical: training_ml_control.control.FeedbackController

Bases: {py:obj}`typing.Protocol`

````{py:method} control(measurement: numpy.typing.NDArray) -> numpy.typing.NDArray
:canonical: training_ml_control.control.FeedbackController.control

```{autodoc2-docstring} training_ml_control.control.FeedbackController.control
```

````

`````

`````{py:class} Observer
:canonical: training_ml_control.control.Observer

Bases: {py:obj}`typing.Protocol`

````{py:method} observe(measurement: numpy.typing.NDArray) -> numpy.typing.NDArray
:canonical: training_ml_control.control.Observer.observe

```{autodoc2-docstring} training_ml_control.control.Observer.observe
```

````

`````

`````{py:class} ConstantController(u: numpy.typing.NDArray = np.zeros(1))
:canonical: training_ml_control.control.ConstantController

```{autodoc2-docstring} training_ml_control.control.ConstantController
```

```{rubric} Initialization
```

```{autodoc2-docstring} training_ml_control.control.ConstantController.__init__
```

````{py:method} act(measurement: numpy.typing.NDArray) -> numpy.typing.NDArray
:canonical: training_ml_control.control.ConstantController.act

```{autodoc2-docstring} training_ml_control.control.ConstantController.act
```

````

`````

`````{py:class} SineController(env: gymnasium.Env, u_max: numpy.typing.NDArray = np.asarray([10]), frequency: float = 1)
:canonical: training_ml_control.control.SineController

```{autodoc2-docstring} training_ml_control.control.SineController
```

```{rubric} Initialization
```

```{autodoc2-docstring} training_ml_control.control.SineController.__init__
```

````{py:method} act(measurement: numpy.typing.NDArray) -> numpy.typing.NDArray
:canonical: training_ml_control.control.SineController.act

```{autodoc2-docstring} training_ml_control.control.SineController.act
```

````

`````

`````{py:class} SumOfSineController(env: gymnasium.Env, u_max: numpy.typing.NDArray = np.asarray([10]), frequencies: list[float] = [1.0])
:canonical: training_ml_control.control.SumOfSineController

```{autodoc2-docstring} training_ml_control.control.SumOfSineController
```

```{rubric} Initialization
```

```{autodoc2-docstring} training_ml_control.control.SumOfSineController.__init__
```

````{py:method} act(measurement: numpy.typing.NDArray) -> numpy.typing.NDArray
:canonical: training_ml_control.control.SumOfSineController.act

```{autodoc2-docstring} training_ml_control.control.SumOfSineController.act
```

````

`````

`````{py:class} SchroederSweepController(env: gymnasium.Env, n_time_steps: int = 200, input_power: float = 10, n_harmonics: int = 3, frequency: float = 1)
:canonical: training_ml_control.control.SchroederSweepController

```{autodoc2-docstring} training_ml_control.control.SchroederSweepController
```

```{rubric} Initialization
```

```{autodoc2-docstring} training_ml_control.control.SchroederSweepController.__init__
```

````{py:method} act(measurement: numpy.typing.NDArray) -> numpy.typing.NDArray
:canonical: training_ml_control.control.SchroederSweepController.act

```{autodoc2-docstring} training_ml_control.control.SchroederSweepController.act
```

````

`````

`````{py:class} PRBSController(u_max: numpy.typing.NDArray = np.asarray([10]), seed: int = 16)
:canonical: training_ml_control.control.PRBSController

```{autodoc2-docstring} training_ml_control.control.PRBSController
```

```{rubric} Initialization
```

```{autodoc2-docstring} training_ml_control.control.PRBSController.__init__
```

````{py:method} act(measurement: numpy.typing.NDArray) -> numpy.typing.NDArray
:canonical: training_ml_control.control.PRBSController.act

```{autodoc2-docstring} training_ml_control.control.PRBSController.act
```

````

`````

`````{py:class} RandomController(env: gymnasium.Env)
:canonical: training_ml_control.control.RandomController

```{autodoc2-docstring} training_ml_control.control.RandomController
```

```{rubric} Initialization
```

```{autodoc2-docstring} training_ml_control.control.RandomController.__init__
```

````{py:method} act(measurement: numpy.typing.NDArray) -> numpy.typing.NDArray
:canonical: training_ml_control.control.RandomController.act

```{autodoc2-docstring} training_ml_control.control.RandomController.act
```

````

`````

````{py:function} build_lqr_controller(model: do_mpc.model.LinearModel, t_step: float, n_horizon: int | None, setpoint: numpy.typing.NDArray, Q: numpy.typing.NDArray, R: numpy.typing.NDArray) -> do_mpc.controller.LQR
:canonical: training_ml_control.control.build_lqr_controller

```{autodoc2-docstring} training_ml_control.control.build_lqr_controller
```
````

````{py:function} build_mpc_controller(model: do_mpc.model.Model, t_step: float, n_horizon: int | None, terminal_cost, stage_cost, x_limits: dict[str, numpy.typing.NDArray] | None = None, u_limits: dict[str, numpy.typing.NDArray] | None = None, u_penalty: dict[str, float] | None = None, *, uncertainty_values: dict[str, numpy.typing.NDArray] | None = None, n_robust: int = 1) -> do_mpc.controller.MPC
:canonical: training_ml_control.control.build_mpc_controller

```{autodoc2-docstring} training_ml_control.control.build_mpc_controller
```
````
