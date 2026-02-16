# PipePlotly

A **verb-based, pipe-friendly** Python package for creating beautiful static and interactive visualizations with an intuitive, functional API.

[![PyPI version](https://img.shields.io/pypi/v/pipeplotly.svg)](https://pypi.org/project/pipeplotly/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pipeplotly)](https://pypi.org/project/pipeplotly/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/pipeplotly)](https://pypi.org/project/pipeplotly/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## About

**PipePlotly** is a high-level, verb-based visualization library for Python that prioritizes developer experience and code readability. It bridges the gap between the structured **Grammar of Graphics** (via `plotnine`) and modern **interactive dashboards** (via `Plotly Express`).

By leveraging a functional API and the `>>` pipe operator, PipePlotly allows you to build complex data visualizations that read like natural language, making your analysis pipelines more maintainable and expressive.

### Why PipePlotly?
- 🔗 **Functional First**: Built from the ground up to support the `>>` pipe operator
- 📊 **Hybrid Power**: Seamlessly switch between publication-quality static plots and interactive exploration
- 🎨 **Declarative Verbs**: Clear, expressive functions like `plot_points`, `add_color`, and `set_theme`
- 🧩 **Ecosystem Ready**: First-class integration with `pandas` and `pipeframe`

## Installation

```bash
pip install pipeplotly
```

### Dependencies
- `plotnine>=0.12.0` - Grammar of Graphics for Python
- `plotly>=5.0.0` - Interactive visualizations
- `pandas>=1.3.0` - Data manipulation

### Optional
```bash
pip install pipeplotly[pipeframe]  # For enhanced pipe operator support
pip install pipeplotly[full]       # For all features
pip install pipeplotly[dev]        # Development dependencies
```

## Quick Start (Functional Style)

PipePlotly is designed to be used with the pipe operator (`>>`) for a clean, readable data pipeline.

```python
import pandas as pd
from pipeplotly import Plot
from pipeplotly.verbs import plot_points, add_color, add_labels, set_theme, show

# Create sample data
df = pd.DataFrame({
    'x': range(10),
    'y': [i**2 for i in range(10)],
    'category': ['A', 'B'] * 5
})

# Create a static plot using the pipe operator
(df 
 >> Plot() 
 >> plot_points('x', 'y') 
 >> add_color('category') 
 >> add_labels(title='My First Pipe Plot', x='X Values', y='Y Values')
 >> set_theme('minimal')
 >> show())
```


> [!TIP]
> **How to read the `>>` operator:** Think of it as **"pipe to"** or **"and then"**. 
> For example: `df >> Plot() >> show()` is read as *"take the dataframe, **pipe it to** a Plot, **and then** show it."*

### Alternative: Method Chaining
If you prefer traditional object-oriented syntax, PipePlotly also supports method chaining:

```python
plot = (Plot(df)
    .plot_points('x', 'y')
    .add_color('category')
    .show())
```

## Core Concepts

### Verb Categories

PipePlotly organizes its API into four verb categories, all designed for use with `>>`.

#### 1. **Initialization Verbs** - Define plot type
```python
df >> Plot() >> plot_points(x, y)      # Scatter plot
df >> Plot() >> plot_lines(x, y)       # Line plot
df >> Plot() >> plot_bars(y=column)    # Bar chart
df >> Plot() >> plot_histogram(x)      # Histogram
df >> Plot() >> plot_box(x, y)         # Box plot
df >> Plot() >> plot_violin(x, y)      # Violin plot
```

#### 2. **Aesthetic Verbs** - Map data to visuals
```python
>> add_color(column)      # Color mapping
>> add_size(column)       # Size mapping
>> add_shape(column)      # Shape mapping
>> add_facets(rows, cols) # Small multiples
>> add_labels(title, x, y) # Titles and labels
>> add_smooth()           # Statistical smoothing
```

#### 3. **Transformation Verbs** - Modify scales
```python
>> scale_x_log()          # Log scales
>> xlim(min, max)         # Axis limits
>> coord_flip()           # Swap axes
```

#### 4. **Output Verbs** - Render and export
```python
>> show()                 # Display
>> save(filename)         # Export
>> to_interactive()       # Switch to Plotly
>> to_static()            # Switch to plotnine
```

## Examples

### Multi-faceted Scatter Plot
```python
from pipeplotly import Plot
from pipeplotly.verbs import *
import seaborn as sns

iris = sns.load_dataset('iris')

(iris
 >> Plot()
 >> plot_points('sepal_length', 'sepal_width')
 >> add_color('species')
 >> add_facets(cols='species')
 >> add_labels(title='Iris Dataset Analysis')
 >> set_theme('minimal')
 >> show())
```

### Interactive Time Series
```python
(df 
 >> Plot()
 >> plot_lines('date', 'value')
 >> add_color('category')
 >> to_interactive()  # Switch to Plotly backend
 >> show())
```

## 📚 Documentation

Detailed documentation and guides are available:

*   [**API Reference**](API_REFERENCE.md) - Full list of all verbs and options (Pipe-first).
*   [**Tutorial Notebook**](examples/pipe_operator_examples.ipynb) - 13 sections and 40+ examples of pipe usage.
*   [**Quick Reference**](PIPE_OPERATOR_QUICKREF.md) - Cheat sheet for common operations.

## Development

```bash
# Clone the repository
git clone https://github.com/Yasser03/pipeplotly.git
cd pipeplotly

# Install in development mode
pip install -e .[dev]

# Run tests
pytest tests/ -v
```

## 👨‍💻 Author

**Dr. Yasser Mustafa**

AI & Data Science Specialist | Theoretical Physics PhD

*   🎓 **PhD in Theoretical Nuclear Physics**
*   💼 **10+ years** in production AI/ML systems
*   🔬 **48+ research publications**
*   🏢 **Experience:** Government (Abu Dhabi), Media (Track24), Recruitment (Reed), Energy (ADNOC)
*   📍 Based in Newcastle Upon Tyne, UK
*   ✉️ [yasser.mustafan@gmail.com](mailto:yasser.mustafan@gmail.com)
*   🔗 [LinkedIn](https://www.linkedin.com/in/yasser-mustafa-phd-72886344/) | [GitHub](https://github.com/Yasser03)

## Coming Later

PipePlotly is actively evolving. Here’s what’s on the horizon:
- 🌈 **More Backends**: Upcoming support for Altair and Bokeh
- 📑 **Auto-Reporting**: Generate full HTML/PDF reports directly from piped pipelines
- 🧪 **Advanced Stats**: More complex statistical geoms and transformations
- 🔌 **Plugin System**: Easily add your own custom verbs and backends

---

## License

MIT License - see [LICENSE](LICENSE) file for details.
