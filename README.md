# PipePlotly

A **verb-based, pipe-friendly** Python package for creating beautiful static and interactive visualizations with an intuitive, natural language-like API.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## Overview

PipePlotly bridges the gap between **Grammar of Graphics** (via plotnine) and modern **interactive visualizations** (via Plotly Express) with a consistent, readable syntax inspired by the tidyverse and pipeframe packages.

**Why PipePlotly?**
- 📊 **Dual backends**: Static plots (plotnine) and interactive plots (Plotly Express)
- 🔗 **Method chaining**: Compose visualizations naturally
- 🎨 **Verb-based API**: Code reads like natural language
- 🚀 **Production-ready**: Type hints, error handling, comprehensive docs
- 🧩 **Grammar of Graphics**: Familiar to R/ggplot2 users

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
pip install pipeplotly[full]       # For all features (includes scikit-misc for smoothing)
pip install pipeplotly[dev]        # Development dependencies
```

> [!NOTE]
> For `loess` smoothing (the default in `add_smooth()`), you must have `scikit-misc` installed.

## Quick Start

```python
import pandas as pd
from pipeplotly import Plot

# Create sample data
df = pd.DataFrame({
    'x': range(10),
    'y': [i**2 for i in range(10)],
    'category': ['A', 'B'] * 5
})

# Create a static plot (Grammar of Graphics)
plot = (Plot(df)
    .plot_points('x', 'y')
    .add_color('category')
    .add_labels(title='My First Plot', x='X Values', y='Y Values')
    .set_theme('minimal')
    .show())

# Convert to interactive with one method
plot.to_interactive().show()
```

## Core Concepts

### Verb Categories

PipePlotly organizes its API into four verb categories:

#### 1. **Initialization Verbs** - Define plot type
```python
.plot_points(x, y)      # Scatter plot
.plot_lines(x, y)       # Line plot
.plot_bars(x, y)        # Bar chart
.plot_histogram(x)      # Histogram
.plot_box(x, y)         # Box plot
.plot_violin(x, y)      # Violin plot
.plot_density(x)        # Density plot
.plot_heatmap(x, y, color)  # Heatmap
```

#### 2. **Aesthetic Verbs** - Map data to visuals
```python
.add_color(column)      # Color by column
.add_size(column)       # Size by column
.add_shape(column)      # Shape by column
.add_facets(rows, cols) # Small multiples
.add_labels(title, x, y)  # Axis labels
.add_smooth()           # Trend line
```

#### 3. **Transformation Verbs** - Modify scales
```python
.scale_x_log()          # Log scale for x
.scale_y_log()          # Log scale for y
.xlim(min, max)         # Set x limits
.ylim(min, max)         # Set y limits
.coord_flip()           # Flip coordinates
```

#### 4. **Output Verbs** - Render and export
```python
.show()                 # Display plot
.save(filename)         # Save to file
.to_interactive()       # Convert to Plotly
.to_static()            # Convert to plotnine
.to_html(filename)      # Export as HTML
```

## Examples

### Static Scatter Plot with Facets
```python
from pipeplotly import Plot
import pandas as pd
import seaborn as sns

# Load iris dataset
iris = sns.load_dataset('iris')

# Create multi-faceted scatter plot
plot = (Plot(iris)
    .plot_points('sepal_length', 'sepal_width')
    .add_color('species')
    .add_facets(cols='species')
    .add_labels(
        title='Iris Dataset Analysis',
        x='Sepal Length (cm)',
        y='Sepal Width (cm)'
    )
    .set_theme('minimal')
    .show())
```

### Interactive Time Series
```python
# Create time series data
df = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=100),
    'value': np.cumsum(np.random.randn(100)),
    'category': np.random.choice(['A', 'B', 'C'], 100)
})

# Create interactive line plot
plot = (Plot(df)
    .plot_lines('date', 'value')
    .add_color('category')
    .add_labels(title='Time Series Trends')
    .to_interactive()  # Switch to Plotly backend
    .show())
```

### Distribution Analysis
```python
# Create histogram with density overlay
plot = (Plot(df)
    .plot_histogram('value')
    .add_color('category')
    .add_facets(rows='category')
    .set_theme('dark')
    .show())
```

### Saving Plots
```python
# Save as static PNG
plot.save('my_plot.png', width=10, height=6, dpi=300)

# Save as interactive HTML
plot.to_interactive().to_html('my_plot.html')

# Save as PDF
plot.save('my_plot.pdf')
```

## 📚 Documentation

Detailed documentation and guides are available:

*   [**API Reference**](file:///c:/Yasser-SSD/PipePlotly/API_REFERENCE.md) - Full list of all verbs and options.
*   [**Pipe Operator Guide**](file:///c:/Yasser-SSD/PipePlotly/PIPE_OPERATOR_GUIDE.md) - Deep dive into functional plotting with `>>`.
*   [**Quick Reference**](file:///c:/Yasser-SSD/PipePlotly/PIPE_OPERATOR_QUICKREF.md) - Cheat sheet for common operations.

### Pipe Operator (`>>`)
PipePlotly now fully supports the pipe operator for a functional programming style:

```python
from pipeplotly.verbs import plot_points, add_color, show

# Use the >> operator for a natural data flow
plot = (df 
    >> Plot() 
    >> plot_points('x', 'y') 
    >> add_color('category') 
    >> show())
```

See [PIPE_OPERATOR_GUIDE.md](PIPE_OPERATOR_GUIDE.md) and the [Tutorial Notebook](examples/pipe_operator_examples_local.ipynb) for more details.

## Switching Between Static and Interactive

```python
# Start with static
plot = Plot(df).plot_points('x', 'y').add_color('category')

# View as static (plotnine)
plot.show()

# View as interactive (Plotly)
plot.to_interactive().show()

# Switch back to static
plot.to_static().show()
```

## Themes

Built-in themes work across both backends:
- `default` - Default theme
- `minimal` - Clean, minimal design
- `classic` - Classic look
- `dark` - Dark mode
- `light` - Light background
- `bw` - Black and white
- `void` - No axes or grids

```python
plot = Plot(df).plot_points('x', 'y').set_theme('dark')
```

## Color Palettes

```python
# Use built-in palettes
plot = (Plot(df)
    .plot_points('x', 'y')
    .add_color('category', palette='viridis'))

# Custom colors
plot = (Plot(df)
    .plot_points('x', 'y')
    .add_color('category', palette=['#FF5733', '#33FF57', '#3357FF']))

# Fixed color (non-mapped)
plot = (Plot(df)
    .plot_points('x', 'y')
    .add_color(value='steelblue'))
```

## API Reference

### Plot Class

The main entry point for creating visualizations.

```python
class Plot:
    def __init__(data=None, state=None)
    
    # Initialization verbs
    def plot_points(x, y, **kwargs) -> Plot
    def plot_lines(x, y, **kwargs) -> Plot
    def plot_bars(x, y=None, **kwargs) -> Plot
    # ... more geometry types
    
    # Aesthetic verbs
    def add_color(column=None, value=None, palette=None) -> Plot
    def add_size(column=None, value=None) -> Plot
    # ... more aesthetics
    
    # Transformation verbs
    def scale_x_log() -> Plot
    def xlim(min, max) -> Plot
    # ... more transformations
    
    # Output verbs
    def show() -> Plot
    def save(filename, width=None, height=None, dpi=300) -> Plot
    def to_interactive() -> Plot
    def to_static() -> Plot
```

## Comparison with Other Libraries

| Feature | PipePlotly | plotnine | Plotly Express |
|---------|-----------|----------|----------------|
| Grammar of Graphics | ✅ | ✅ | ❌ |
| Interactive plots | ✅ | ❌ | ✅ |
| Method chaining | ✅ | ⚠️ (via `+`) | ⚠️ (limited) |
| Verb-based API | ✅ | ❌ | ❌ |
| Backend switching | ✅ | ❌ | ❌ |
| Natural language syntax | ✅ | ⚠️ | ⚠️ |

## Development

```bash
# Clone the repository
git clone https://github.com/Yasser03/pipeplotly.git
cd pipeplotly

# Install in development mode
pip install -e .[dev]

# Run tests
pytest tests/ -v --cov=pipeplotly

# Format code
black pipeplotly/
```

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) file for details.

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

## Acknowledgments

- Inspired by [pipeframe](https://github.com/pipeframe) for verb-based APIs
- Built on [plotnine](https://plotnine.readthedocs.io/) for Grammar of Graphics
- Powered by [Plotly Express](https://plotly.com/python/plotly-express/) for interactivity
- Design philosophy from R's [ggplot2](https://ggplot2.tidyverse.org/) and [tidyverse](https://www.tidyverse.org/)

## Citation

If you use PipePlotly in your research, please cite:

```bibtex
@software{pipeplotly2026,
  title = {PipePlotly: Verb-Based Visualization for Python},
  author = {Yasser Mustafa},
  year = {2026},
  url = {https://github.com/Yasser03/pipeplotly}
}
```

## Support

- 📚 [Documentation](https://pipeplotly.readthedocs.io)
- 🐛 [Issue Tracker](https://github.com/Yasser03/pipeplotly/issues)
- 💬 [Discussions](https://github.com/Yasser03/pipeplotly/discussions)
