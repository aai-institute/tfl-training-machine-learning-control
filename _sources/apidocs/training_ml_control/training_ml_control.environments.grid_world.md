# {py:mod}`training_ml_control.environments.grid_world`

```{py:module} training_ml_control.environments.grid_world
```

```{autodoc2-docstring} training_ml_control.environments.grid_world
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`SimplifiedActions <training_ml_control.environments.grid_world.SimplifiedActions>`
  -
* - {py:obj}`SimplifiedGridEnv <training_ml_control.environments.grid_world.SimplifiedGridEnv>`
  -
* - {py:obj}`GridWorldEnv <training_ml_control.environments.grid_world.GridWorldEnv>`
  -
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`convert_graph_to_directed <training_ml_control.environments.grid_world.convert_graph_to_directed>`
  - ```{autodoc2-docstring} training_ml_control.environments.grid_world.convert_graph_to_directed
    :summary:
    ```
* - {py:obj}`plot_grid_graph <training_ml_control.environments.grid_world.plot_grid_graph>`
  - ```{autodoc2-docstring} training_ml_control.environments.grid_world.plot_grid_graph
    :summary:
    ```
* - {py:obj}`plot_grid_all_paths_graph <training_ml_control.environments.grid_world.plot_grid_all_paths_graph>`
  - ```{autodoc2-docstring} training_ml_control.environments.grid_world.plot_grid_all_paths_graph
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`__all__ <training_ml_control.environments.grid_world.__all__>`
  - ```{autodoc2-docstring} training_ml_control.environments.grid_world.__all__
    :summary:
    ```
````

### API

````{py:data} __all__
:canonical: training_ml_control.environments.grid_world.__all__
:value: >
   ['GridWorldEnv', 'plot_grid_graph', 'convert_graph_to_directed', 'plot_grid_all_paths_graph']

```{autodoc2-docstring} training_ml_control.environments.grid_world.__all__
```

````

`````{py:class} SimplifiedActions()
:canonical: training_ml_control.environments.grid_world.SimplifiedActions

Bases: {py:obj}`enum.IntEnum`

````{py:attribute} right
:canonical: training_ml_control.environments.grid_world.SimplifiedActions.right
:value: >
   0

```{autodoc2-docstring} training_ml_control.environments.grid_world.SimplifiedActions.right
```

````

````{py:attribute} down
:canonical: training_ml_control.environments.grid_world.SimplifiedActions.down
:value: >
   1

```{autodoc2-docstring} training_ml_control.environments.grid_world.SimplifiedActions.down
```

````

````{py:attribute} left
:canonical: training_ml_control.environments.grid_world.SimplifiedActions.left
:value: >
   2

```{autodoc2-docstring} training_ml_control.environments.grid_world.SimplifiedActions.left
```

````

````{py:attribute} up
:canonical: training_ml_control.environments.grid_world.SimplifiedActions.up
:value: >
   3

```{autodoc2-docstring} training_ml_control.environments.grid_world.SimplifiedActions.up
```

````

`````

`````{py:class} SimplifiedGridEnv(mission_space: minigrid.core.mission.MissionSpace, grid_size: int | None = None, width: int | None = None, height: int | None = None, max_steps: int = 100, see_through_walls: bool = False, agent_view_size: int = 7, render_mode: str | None = None, screen_size: int | None = 640, highlight: bool = True, tile_size: int = TILE_PIXELS, agent_pov: bool = False)
:canonical: training_ml_control.environments.grid_world.SimplifiedGridEnv

Bases: {py:obj}`minigrid.minigrid_env.MiniGridEnv`

````{py:method} step(action: gymnasium.core.ActType) -> tuple[gymnasium.core.ObsType, typing.SupportsFloat, bool, bool, dict[str, typing.Any]]
:canonical: training_ml_control.environments.grid_world.SimplifiedGridEnv.step

````

`````

`````{py:class} GridWorldEnv(max_steps: int | None = None, **kwargs)
:canonical: training_ml_control.environments.grid_world.GridWorldEnv

Bases: {py:obj}`training_ml_control.environments.grid_world.SimplifiedGridEnv`

````{py:method} _gen_mission()
:canonical: training_ml_control.environments.grid_world.GridWorldEnv._gen_mission
:staticmethod:

```{autodoc2-docstring} training_ml_control.environments.grid_world.GridWorldEnv._gen_mission
```

````

````{py:method} _gen_grid(width: int, height: int) -> None
:canonical: training_ml_control.environments.grid_world.GridWorldEnv._gen_grid

```{autodoc2-docstring} training_ml_control.environments.grid_world.GridWorldEnv._gen_grid
```

````

````{py:method} get_graph() -> networkx.DiGraph
:canonical: training_ml_control.environments.grid_world.GridWorldEnv.get_graph

```{autodoc2-docstring} training_ml_control.environments.grid_world.GridWorldEnv.get_graph
```

````

`````

````{py:function} convert_graph_to_directed(G: networkx.Graph) -> networkx.DiGraph
:canonical: training_ml_control.environments.grid_world.convert_graph_to_directed

```{autodoc2-docstring} training_ml_control.environments.grid_world.convert_graph_to_directed
```
````

````{py:function} plot_grid_graph(G: networkx.Graph | networkx.DiGraph) -> None
:canonical: training_ml_control.environments.grid_world.plot_grid_graph

```{autodoc2-docstring} training_ml_control.environments.grid_world.plot_grid_graph
```
````

````{py:function} plot_grid_all_paths_graph(G: networkx.Graph, *, show_solution: bool = False) -> None
:canonical: training_ml_control.environments.grid_world.plot_grid_all_paths_graph

```{autodoc2-docstring} training_ml_control.environments.grid_world.plot_grid_all_paths_graph
```
````
