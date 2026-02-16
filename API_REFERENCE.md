# PipePlotly API Reference

This document provides a comprehensive reference for the PipePlotly API, prioritizing the **Pipe Operator (`>>`)** interface.

## 1. Core Entry Points (The `>>` Interface)

PipePlotly's primary interface uses the pipe operator to flow data from a DataFrame through a `Plot` object and into visualization verbs.

### Initialization

```python
from pipeplotly import Plot
from pipeplotly.verbs import *

# The Standard Pipe Pattern:
# df >> Plot() >> [Visualization Verb] >> [Aesthetic Verb] >> show()

df >> Plot() >> plot_points('x', 'y') >> show()
```

---

## 2. Standalone Verb Functions

These functions are designed specifically for use with the `>>` operator.

### 📊 Initialization Verbs (Geometry)
These verbs define the "what" of your visualization. They must follow `Plot()` in a pipeline.

| Verb | Description | Parameters |
| :--- | :--- | :--- |
| `plot_points(x, y)` | Scatter plot | `x`, `y` (column names) |
| `plot_lines(x, y)` | Line plot | `x`, `y` (column names) |
| `plot_bars(x, y)` | Bar chart | `x` (category), `y` (values, optional) |
| `plot_histogram(x)` | Distribution | `x` (column name) |
| `plot_box(x, y)` | Box plot | `x` (category), `y` (values) |
| `plot_violin(x, y)` | Violin plot | `x` (category), `y` (values) |
| `plot_density(x)` | Density plot | `x` (column name) |
| `plot_heatmap(x, y, z)`| Heatmap | `x`, `y`, `z` (column names) |

### 🎨 Aesthetic Verbs
Modify the "how" of your visualization (mapping data to visual properties).

| Verb | Description | Usage Example |
| :--- | :--- | :--- |
| `add_color(col)` | Map column to color | `>> add_color('species')` |
| `add_size(col)` | Map column to size | `>> add_size('population')` |
| `add_shape(col)` | Map column to shape | `>> add_shape('type')` |
| `add_facets(cols)` | Create subplots | `>> add_facets(cols='category')` |
| `add_labels(...)` | Set titles/axes | `>> add_labels(title='My Plot')` |
| `add_smooth()` | Add trend line | `>> add_smooth(method='loess')` |

### 🛠️ Transformation Verbs
Adjust coordinates, scales, and limits.

| Verb | Description | Usage Example |
| :--- | :--- | :--- |
| `scale_x_log()` | Logarithmic X axis | `>> scale_x_log()` |
| `scale_y_log()` | Logarithmic Y axis | `>> scale_y_log()` |
| `xlim(min, max)` | X axis limits | `>> xlim(0, 100)` |
| `coord_flip()` | Swap X and Y axes | `>> coord_flip()` |

---

## 3. Output & Backend Control

These verbs determine how and where the plot is rendered.

| Verb | Description | Backend |
| :--- | :--- | :--- |
| `show()` | Display the plot | Both |
| `to_interactive()` | Switch to Plotly | Interactive |
| `to_static()` | Switch to plotnine | Static |
| `save(path)` | Export to file | Both |
| `to_html(path)` | Export as HTML | Interactive |

---

## 4. Alternative: Method Chaining (The `.` Interface)

While the pipe operator is the primary focus, all verbs are also available as methods on the `Plot` class:

```python
# Chaining Style:
plot = (Plot(df)
        .plot_points('x', 'y')
        .add_color('category')
        .show())
```

---

## 📚 Comparisons

| Feature | Pipe Operator (`>>`) | Method Chaining (`.`) |
| :--- | :--- | :--- |
| **Logic** | Functional (Data Flow) | Object-Oriented (Modification) |
| **Readability** | Reads left-to-right | Reads top-to-bottom |
| **Integrations** | Seamless with `pipeframe` | Standard Python |

For more examples, check out the [Tutorial Notebook](examples/pipe_operator_examples.ipynb).
