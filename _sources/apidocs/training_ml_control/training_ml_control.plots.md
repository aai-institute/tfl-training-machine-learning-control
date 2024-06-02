# {py:mod}`training_ml_control.plots`

```{py:module} training_ml_control.plots
```

```{autodoc2-docstring} training_ml_control.plots
:allowtitles:
```

## Module Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`plot_cart_results <training_ml_control.plots.plot_cart_results>`
  - ```{autodoc2-docstring} training_ml_control.plots.plot_cart_results
    :summary:
    ```
* - {py:obj}`plot_inverted_pendulum_results <training_ml_control.plots.plot_inverted_pendulum_results>`
  - ```{autodoc2-docstring} training_ml_control.plots.plot_inverted_pendulum_results
    :summary:
    ```
* - {py:obj}`animate_cart_simulation <training_ml_control.plots.animate_cart_simulation>`
  - ```{autodoc2-docstring} training_ml_control.plots.animate_cart_simulation
    :summary:
    ```
* - {py:obj}`animate_inverted_pendulum_simulation <training_ml_control.plots.animate_inverted_pendulum_simulation>`
  - ```{autodoc2-docstring} training_ml_control.plots.animate_inverted_pendulum_simulation
    :summary:
    ```
* - {py:obj}`animate_full_inverted_pendulum_simulation <training_ml_control.plots.animate_full_inverted_pendulum_simulation>`
  - ```{autodoc2-docstring} training_ml_control.plots.animate_full_inverted_pendulum_simulation
    :summary:
    ```
* - {py:obj}`animate_pendulum_simulation <training_ml_control.plots.animate_pendulum_simulation>`
  - ```{autodoc2-docstring} training_ml_control.plots.animate_pendulum_simulation
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`__all__ <training_ml_control.plots.__all__>`
  - ```{autodoc2-docstring} training_ml_control.plots.__all__
    :summary:
    ```
````

### API

````{py:data} __all__
:canonical: training_ml_control.plots.__all__
:value: >
   ['plot_cart_results', 'plot_inverted_pendulum_results', 'animate_cart_simulation', 'animate_inverted...

```{autodoc2-docstring} training_ml_control.plots.__all__
```

````

````{py:function} plot_cart_results(T: numpy.typing.NDArray, reference: float, observations: numpy.typing.NDArray, actions: numpy.typing.NDArray) -> None
:canonical: training_ml_control.plots.plot_cart_results

```{autodoc2-docstring} training_ml_control.plots.plot_cart_results
```
````

````{py:function} plot_inverted_pendulum_results(T: numpy.typing.NDArray, reference: float, observations: numpy.typing.NDArray, actions: numpy.typing.NDArray) -> None
:canonical: training_ml_control.plots.plot_inverted_pendulum_results

```{autodoc2-docstring} training_ml_control.plots.plot_inverted_pendulum_results
```
````

````{py:function} animate_cart_simulation(data: do_mpc.data.Data | do_mpc.data.MPCData, *, reference: float | None = None) -> IPython.display.HTML
:canonical: training_ml_control.plots.animate_cart_simulation

```{autodoc2-docstring} training_ml_control.plots.animate_cart_simulation
```
````

````{py:function} animate_inverted_pendulum_simulation(data: do_mpc.data.Data | do_mpc.data.MPCData) -> IPython.display.HTML
:canonical: training_ml_control.plots.animate_inverted_pendulum_simulation

```{autodoc2-docstring} training_ml_control.plots.animate_inverted_pendulum_simulation
```
````

````{py:function} animate_full_inverted_pendulum_simulation(data: do_mpc.data.Data | do_mpc.data.MPCData) -> IPython.display.HTML
:canonical: training_ml_control.plots.animate_full_inverted_pendulum_simulation

```{autodoc2-docstring} training_ml_control.plots.animate_full_inverted_pendulum_simulation
```
````

````{py:function} animate_pendulum_simulation(data: do_mpc.data.Data | do_mpc.data.MPCData) -> IPython.display.HTML
:canonical: training_ml_control.plots.animate_pendulum_simulation

```{autodoc2-docstring} training_ml_control.plots.animate_pendulum_simulation
```
````
