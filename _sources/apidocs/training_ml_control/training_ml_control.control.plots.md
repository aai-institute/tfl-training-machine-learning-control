# {py:mod}`training_ml_control.control.plots`

```{py:module} training_ml_control.control.plots
```

```{autodoc2-docstring} training_ml_control.control.plots
:allowtitles:
```

## Module Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`plot_influence_of_K_on_pendulum <training_ml_control.control.plots.plot_influence_of_K_on_pendulum>`
  - ```{autodoc2-docstring} training_ml_control.control.plots.plot_influence_of_K_on_pendulum
    :summary:
    ```
* - {py:obj}`plot_small_angle_approximation <training_ml_control.control.plots.plot_small_angle_approximation>`
  - ```{autodoc2-docstring} training_ml_control.control.plots.plot_small_angle_approximation
    :summary:
    ```
* - {py:obj}`plot_second_order_step_response <training_ml_control.control.plots.plot_second_order_step_response>`
  - ```{autodoc2-docstring} training_ml_control.control.plots.plot_second_order_step_response
    :summary:
    ```
* - {py:obj}`plot_estimator_response <training_ml_control.control.plots.plot_estimator_response>`
  - ```{autodoc2-docstring} training_ml_control.control.plots.plot_estimator_response
    :summary:
    ```
* - {py:obj}`plot_mass_spring_damper_results <training_ml_control.control.plots.plot_mass_spring_damper_results>`
  - ```{autodoc2-docstring} training_ml_control.control.plots.plot_mass_spring_damper_results
    :summary:
    ```
* - {py:obj}`plot_inverted_pendulum_results <training_ml_control.control.plots.plot_inverted_pendulum_results>`
  - ```{autodoc2-docstring} training_ml_control.control.plots.plot_inverted_pendulum_results
    :summary:
    ```
* - {py:obj}`animate_mass_spring_damper_simulation <training_ml_control.control.plots.animate_mass_spring_damper_simulation>`
  - ```{autodoc2-docstring} training_ml_control.control.plots.animate_mass_spring_damper_simulation
    :summary:
    ```
* - {py:obj}`animate_inverted_pendulum_simulation <training_ml_control.control.plots.animate_inverted_pendulum_simulation>`
  - ```{autodoc2-docstring} training_ml_control.control.plots.animate_inverted_pendulum_simulation
    :summary:
    ```
* - {py:obj}`animate_full_inverted_pendulum_simulation <training_ml_control.control.plots.animate_full_inverted_pendulum_simulation>`
  - ```{autodoc2-docstring} training_ml_control.control.plots.animate_full_inverted_pendulum_simulation
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`__all__ <training_ml_control.control.plots.__all__>`
  - ```{autodoc2-docstring} training_ml_control.control.plots.__all__
    :summary:
    ```
````

### API

````{py:data} __all__
:canonical: training_ml_control.control.plots.__all__
:value: >
   ['plot_influence_of_K_on_pendulum', 'plot_small_angle_approximation', 'plot_second_order_step_respon...

```{autodoc2-docstring} training_ml_control.control.plots.__all__
```

````

````{py:function} plot_influence_of_K_on_pendulum(K_values: list[float] | None = None) -> None
:canonical: training_ml_control.control.plots.plot_influence_of_K_on_pendulum

```{autodoc2-docstring} training_ml_control.control.plots.plot_influence_of_K_on_pendulum
```
````

````{py:function} plot_small_angle_approximation()
:canonical: training_ml_control.control.plots.plot_small_angle_approximation

```{autodoc2-docstring} training_ml_control.control.plots.plot_small_angle_approximation
```
````

````{py:function} plot_second_order_step_response() -> None
:canonical: training_ml_control.control.plots.plot_second_order_step_response

```{autodoc2-docstring} training_ml_control.control.plots.plot_second_order_step_response
```
````

````{py:function} plot_estimator_response(estimated_response: control.timeresp.TimeResponseData, *, labels: list[str], observations: numpy.typing.NDArray | None = None) -> None
:canonical: training_ml_control.control.plots.plot_estimator_response

```{autodoc2-docstring} training_ml_control.control.plots.plot_estimator_response
```
````

````{py:function} plot_mass_spring_damper_results(T: numpy.typing.NDArray, reference: float, observations: numpy.typing.NDArray, actions: numpy.typing.NDArray) -> None
:canonical: training_ml_control.control.plots.plot_mass_spring_damper_results

```{autodoc2-docstring} training_ml_control.control.plots.plot_mass_spring_damper_results
```
````

````{py:function} plot_inverted_pendulum_results(T: numpy.typing.NDArray, reference: float, observations: numpy.typing.NDArray, actions: numpy.typing.NDArray) -> None
:canonical: training_ml_control.control.plots.plot_inverted_pendulum_results

```{autodoc2-docstring} training_ml_control.control.plots.plot_inverted_pendulum_results
```
````

````{py:function} animate_mass_spring_damper_simulation(data: do_mpc.data.MPCData | do_mpc.data.Data) -> IPython.display.HTML
:canonical: training_ml_control.control.plots.animate_mass_spring_damper_simulation

```{autodoc2-docstring} training_ml_control.control.plots.animate_mass_spring_damper_simulation
```
````

````{py:function} animate_inverted_pendulum_simulation(data: do_mpc.data.MPCData | do_mpc.data.Data) -> IPython.display.HTML
:canonical: training_ml_control.control.plots.animate_inverted_pendulum_simulation

```{autodoc2-docstring} training_ml_control.control.plots.animate_inverted_pendulum_simulation
```
````

````{py:function} animate_full_inverted_pendulum_simulation(data: do_mpc.data.MPCData | do_mpc.data.Data) -> IPython.display.HTML
:canonical: training_ml_control.control.plots.animate_full_inverted_pendulum_simulation

```{autodoc2-docstring} training_ml_control.control.plots.animate_full_inverted_pendulum_simulation
```
````
