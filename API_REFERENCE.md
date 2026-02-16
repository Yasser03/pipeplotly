# PipePlotly API Reference

This document provides a comprehensive reference for the PipePlotly API, including the core `Plot` class and standalone verb functions.

## 1. Core API

### `Plot(data=None, state=None)`

The main visualization class. It uses an immutable state pattern where each method returns a new `Plot` instance.

**Initialization:**

```python
from pipeplotly import Plot
# Initialize with a pandas DataFrame
plot = Plot(df)

# Or use with pipe operator
plot = df >> Plot()
```

---

## 2. Standalone Verbs

Standalone verbs are available in `pipeplotly.verbs` and are designed to be used with the pipe operator (`>>`).

### Initialization Verbs (Geoms)

These verbs define the base geometry of the plot.

| Verb | Description | Parameters |
| :--- | :--- | :--- |
| `plot_points(x, y, **kwargs)` | Create a scatter plot. | `x` (str), `y` (str) |
| `plot_lines(x, y, **kwargs)` | Create a line plot. | `x` (str), `y` (str) |
| `plot_bars(x, y=None, **kwargs)` | Create a bar chart. | `x` (str), `y` (str, optional) |
| `plot_histogram(x, bins=None, **kwargs)` | Create a histogram. | `x` (str), `bins` (int, optional) |
| `plot_box(x=None, y=None, **kwargs)` | Create a box plot. | `x` (str, optional), `y` (str, optional) |
| `plot_violin(x=None, y=None, **kwargs)` | Create a violin plot. | `x` (str, optional), `y` (str, optional) |
| `plot_density(x, **kwargs)` | Create a density plot. | `x` (str) |
| `plot_heatmap(x, y, color, **kwargs)` | Create a heatmap. | `x` (str), `y` (str), `color` (str) |

### Aesthetic Verbs

Modify how data columns are mapped to visual properties.

| Verb | Description | Parameters |
| :--- | :--- | :--- |
| `add_color(column=None, value=None, palette=None)` | Set color mapping or fixed color. | `column` (str), `value` (str), `palette` (str/list) |
| `add_size(column=None, value=None)` | Set size mapping or fixed size. | `column` (str), `value` (float) |
| `add_shape(column)` | Map a column to point shape. | `column` (str) |
| `add_alpha(column=None, value=None)` | Set transparency. | `column` (str), `value` (float) |
| `add_facets(rows=None, cols=None, wrap=None)` | Create subplots based on categories. | `rows`, `cols`, `wrap` (str) |
| `add_labels(title=None, x=None, y=None)` | Update plot labels. | `title`, `x`, `y` (str) |
| `add_smooth(method='loess', **kwargs)` | Add a smoothing trend line. | `method` ('loess', 'lm', etc.) |

### Transformation Verbs

Modify axes, scales, and coordinates.

| Verb | Description |
| :--- | :--- |
| `scale_x_log()` / `scale_y_log()` | Apply logarithmic scale. |
| `scale_x_reverse()` / `scale_y_reverse()` | Reverse the axis. |
| `xlim(min, max)` / `ylim(min, max)` | Set axis limits. |
| `coord_flip()` | Swap X and Y axes. |
| `coord_fixed(ratio=1.0)` | Set fixed aspect ratio (y/x). |

### Theme Verbs

| Verb | Description |
| :--- | :--- |
| `set_theme(theme)` | Set plot theme ('default', 'minimal', 'dark', 'classic'). |

---

## 3. Output Verbs

Control how the plot is displayed or saved.

| Verb | Description |
| :--- | :--- |
| `show()` | Render the plot in the current environment. |
| `save(filename, width=None, height=None, dpi=300)` | Save the plot to a file (PNG, PDF, HTML, etc.). |
| `to_interactive()` | Switch to interactive Plotly backend. |
| `to_static()` | Switch to static plotnine backend. |
| `to_html(filename=None)` | Export plot as an HTML fragment or file. |

---

## 4. Method Reference (Plot Class)

Every standalone verb has a corresponding method on the `Plot` class for method chaining.

```python
# Equivalent behavior:
Plot(df).plot_points('x', 'y').add_color('category').show()
# vs
df >> Plot() >> plot_points('x', 'y') >> add_color('category') >> show()
```
