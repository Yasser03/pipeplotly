# PipePlotly + PipeFrame Integration Examples

This document demonstrates how to use PipePlotly with the `>>` pipe operator, both standalone and integrated with the pipeframe package.

## Installation

```bash
# Install PipePlotly
pip install pipeplotly

# Install pipeframe (optional but recommended)
pip install pipeframe
```

## Option 1: Using >> Operator (Built-in PipePlotly Support)

PipePlotly natively supports the `>>` operator through verb functions:

```python
import pandas as pd
from pipeplotly import Plot
from pipeplotly.verbs import plot_points, add_color, add_labels, set_theme, show

# Create data
df = pd.DataFrame({
    'x': range(10),
    'y': [i**2 for i in range(10)],
    'category': ['A', 'B'] * 5
})

# Use pipe operator instead of method chaining
plot = (df 
    >> Plot()
    >> plot_points('x', 'y')
    >> add_color('category')
    >> add_labels(title='My First Plot', x='X', y='Y')
    >> set_theme('minimal')
    >> show())
```

## Option 2: Integration with PipeFrame

PipeFrame extends pandas DataFrames with pipe-friendly operations. Here's how to combine both packages:

### Basic Example

```python
import pandas as pd
from pipeframe import PipeFrame
from pipeplotly import Plot
from pipeplotly.verbs import plot_points, add_color, show

# Wrap DataFrame in PipeFrame
df = PipeFrame({
    'x': range(100),
    'y': range(100),
    'category': ['A', 'B', 'C', 'D'] * 25
})

# Chain data manipulation with visualization
plot = (df
    >> (lambda d: d[d['x'] > 20])  # Filter
    >> (lambda d: d.sort_values('y'))  # Sort
    >> Plot()  # Switch to plotting
    >> plot_points('x', 'y')
    >> add_color('category', palette='viridis')
    >> show())
```

### Advanced Example: Data Pipeline + Visualization

```python
from pipeframe import PipeFrame, filter, mutate, group_by, summarise
from pipeplotly import Plot
from pipeplotly.verbs import *

# Complete data pipeline
result = (PipeFrame(raw_data)
    >> filter(lambda d: d['value'] > 0)  # Filter data
    >> mutate(log_value=lambda d: np.log(d['value']))  # Transform
    >> group_by('category')  # Group
    >> summarise(
        mean_val=lambda d: d['value'].mean(),
        std_val=lambda d: d['value'].std()
    )
    >> Plot()  # Start plotting
    >> plot_bars('category', 'mean_val')
    >> add_color('category', palette='Set2')
    >> add_labels(
        title='Mean Values by Category',
        x='Category',
        y='Mean Value'
    )
    >> set_theme('minimal')
    >> show())
```

### Time Series Example

```python
from pipeframe import PipeFrame
from pipeplotly import Plot
from pipeplotly.verbs import plot_lines, add_color, add_smooth, show

# Time series data pipeline
plot = (
    PipeFrame(sales_data)
    >> (lambda d: d.set_index('date'))
    >> (lambda d: d.resample('M').sum().reset_index())
    >> Plot()
    >> plot_lines('date', 'sales')
    >> add_color('region')
    >> add_smooth(method='loess')
    >> add_labels(title='Monthly Sales by Region')
    >> show()
)
```

## Comparison: Method Chaining vs Pipe Operator

### Method Chaining (Recommended for beginners)

```python
plot = (Plot(df)
    .plot_points('x', 'y')
    .add_color('category')
    .set_theme('minimal')
    .show())
```

**Pros:**
- More familiar to Python developers
- Better IDE autocomplete support
- Clear object ownership

### Pipe Operator (Recommended for data pipelines)

```python
from pipeplotly.verbs import *

plot = (df
    >> Plot()
    >> plot_points('x', 'y')
    >> add_color('category')
    >> set_theme('minimal')
    >> show())
```

**Pros:**
- Consistent with pipeframe and R's tidyverse
- Better for combining data manipulation + viz
- More functional programming style
- Natural data flow (left to right, top to bottom)

## All Available Verbs for Pipe Operator

Import from `pipeplotly.verbs`:

```python
from pipeplotly.verbs import (
    # Initialization
    plot_points, plot_lines, plot_bars, plot_histogram,
    plot_box, plot_violin, plot_density, plot_heatmap,
    
    # Aesthetics
    add_color, add_size, add_shape, add_alpha,
    add_facets, add_labels, add_smooth,
    
    # Transformations
    scale_x_log, scale_y_log, scale_x_reverse, scale_y_reverse,
    xlim, ylim, coord_flip, coord_fixed,
    
    # Theme
    set_theme,
    
    # Output
    show, save, to_interactive, to_static, to_html
)
```

## Complex Real-World Example

```python
import pandas as pd
import numpy as np
from pipeframe import PipeFrame
from pipeplotly import Plot
from pipeplotly.verbs import *

# Complete analysis pipeline
(
    PipeFrame(pd.read_csv('sales_data.csv'))
    # Data cleaning
    >> (lambda d: d.dropna())
    >> (lambda d: d[d['sales'] > 0])
    
    # Feature engineering
    >> (lambda d: d.assign(
        log_sales=np.log(d['sales']),
        month=pd.to_datetime(d['date']).dt.month
    ))
    
    # Aggregation
    >> (lambda d: d.groupby(['region', 'month'])
        .agg({'log_sales': 'mean'})
        .reset_index())
    
    # Visualization
    >> Plot()
    >> plot_points('month', 'log_sales')
    >> add_color('region', palette='viridis')
    >> add_facets(cols='region')
    >> add_smooth(method='loess')
    >> add_labels(
        title='Sales Trends by Region',
        x='Month',
        y='Log Sales'
    )
    >> set_theme('minimal')
    >> save('sales_analysis.png', width=12, height=6, dpi=300)
    >> show()
)
```

## Tips for Using Pipe Operators

1. **Import verbs explicitly** for better readability:
   ```python
   from pipeplotly.verbs import plot_points, add_color, show
   ```

2. **Mix with lambda functions** for custom transformations:
   ```python
   df >> (lambda d: d[d['x'] > 0]) >> Plot() >> ...
   ```

3. **Both styles can coexist** - use what's appropriate:
   ```python
   # Data pipeline with pipes
   clean_df = df >> filter(...) >> mutate(...)
   
   # Plotting with methods (if you prefer)
   plot = Plot(clean_df).plot_points('x', 'y').show()
   ```

4. **Backend conversion** works with both styles:
   ```python
   # Pipe style
   df >> Plot() >> plot_points('x', 'y') >> to_interactive() >> show()
   
   # Method style  
   Plot(df).plot_points('x', 'y').to_interactive().show()
   ```

## Summary

- **Use method chaining (`.`)** when working primarily with visualization
- **Use pipe operator (`>>`)** when combining data manipulation with visualization
- **Both are fully supported** - choose based on your workflow
- **pipeframe integration** is seamless for complex data pipelines
