# {py:mod}`training_ml_control.nb_utils`

```{py:module} training_ml_control.nb_utils
```

```{autodoc2-docstring} training_ml_control.nb_utils
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`TflWorkshopMagic <training_ml_control.nb_utils.TflWorkshopMagic>`
  -
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`set_random_seed <training_ml_control.nb_utils.set_random_seed>`
  - ```{autodoc2-docstring} training_ml_control.nb_utils.set_random_seed
    :summary:
    ```
* - {py:obj}`display_dataframes_side_by_side <training_ml_control.nb_utils.display_dataframes_side_by_side>`
  - ```{autodoc2-docstring} training_ml_control.nb_utils.display_dataframes_side_by_side
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`__all__ <training_ml_control.nb_utils.__all__>`
  - ```{autodoc2-docstring} training_ml_control.nb_utils.__all__
    :summary:
    ```
````

### API

````{py:data} __all__
:canonical: training_ml_control.nb_utils.__all__
:value: >
   ['set_random_seed', 'TflWorkshopMagic', 'display_dataframes_side_by_side']

```{autodoc2-docstring} training_ml_control.nb_utils.__all__
```

````

````{py:function} set_random_seed(seed: int = 16) -> None
:canonical: training_ml_control.nb_utils.set_random_seed

```{autodoc2-docstring} training_ml_control.nb_utils.set_random_seed
```
````

`````{py:class} TflWorkshopMagic(shell)
:canonical: training_ml_control.nb_utils.TflWorkshopMagic

Bases: {py:obj}`IPython.core.magic.Magics`

````{py:method} set_random_seed(seed: str)
:canonical: training_ml_control.nb_utils.TflWorkshopMagic.set_random_seed

```{autodoc2-docstring} training_ml_control.nb_utils.TflWorkshopMagic.set_random_seed
```

````

````{py:method} load_latex_macros(line)
:canonical: training_ml_control.nb_utils.TflWorkshopMagic.load_latex_macros

```{autodoc2-docstring} training_ml_control.nb_utils.TflWorkshopMagic.load_latex_macros
```

````

````{py:method} view_hint(path: os.PathLike)
:canonical: training_ml_control.nb_utils.TflWorkshopMagic.view_hint

```{autodoc2-docstring} training_ml_control.nb_utils.TflWorkshopMagic.view_hint
```

````

````{py:method} presentation_style(style_file: str)
:canonical: training_ml_control.nb_utils.TflWorkshopMagic.presentation_style

```{autodoc2-docstring} training_ml_control.nb_utils.TflWorkshopMagic.presentation_style
```

````

`````

````{py:function} display_dataframes_side_by_side(dataframes: collections.abc.Sequence[pandas.DataFrame], captions: collections.abc.Sequence = ())
:canonical: training_ml_control.nb_utils.display_dataframes_side_by_side

```{autodoc2-docstring} training_ml_control.nb_utils.display_dataframes_side_by_side
```
````
