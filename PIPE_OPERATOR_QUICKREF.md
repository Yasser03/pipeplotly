# Pipe Operator Quick Reference

## ✅ What Works

### 1. DataFrame to Plot
```python
df >> Plot() >> plot_points('x', 'y') >> show()
```

### 2. Plot to Verb Functions
```python
Plot(df) >> plot_points('x', 'y') >> add_color('category') >> show()
```

### 3. Pandas Methods Then Plot
```python
df.filter(...).sort_values(...) >> Plot() >> plot_points('x', 'y') >> show()
```

### 4. Method Chaining (Always Works)
```python
Plot(df).plot_points('x', 'y').add_color('category').show()
```

## ❌ What Doesn't Work

### DataFrame with Lambda Functions 
```python
# WRONG - pandas doesn't support this
df >> (lambda d: d[d['x'] > 0]) >> Plot()  # TypeError!
```

**Why:** Pandas DataFrames don't natively support the `>>` operator with functions.

## 🔧 Solutions

### Option 1: Use Pandas Methods First (Recommended)
```python
# CORRECT
filtered_df = df[df['x'] > 0].sort_values('y')
plot = filtered_df >> Plot() >> plot_points('x', 'y') >> show()

# Or in one chain:
plot = (df[df['x'] > 0]
    .sort_values('y')
    >> Plot()
    >> plot_points('x', 'y')
    >> show())
```

### Option 2: Use PipeFrame Package
```bash
pip install pipeframe
```

```python
from pipeframe import DataFrame as pf_df

plot = (pf_df(df)
    >> (lambda d: d[d._df['x'] > 0])  # Now lambdas work!
    >> (lambda d: d.sort_values('y'))
    >> Plot()
    >> plot_points('x', 'y')
    >> show())
```

### Option 3: Separate Data & Viz
```python
# Traditional approach
filtered = df[df['x'] > 0]
plot = Plot(filtered).plot_points('x', 'y').show()
```

## 📝 Key Imports

```python
from pipeplotly import Plot
from pipeplotly.verbs import (
    plot_points, plot_lines, plot_bars,
    add_color, add_size, add_labels,
    set_theme, show, save
)
```

## 🎯 Best Practices

1. **For simple viz:** Use method chaining (`.`)
2. **For data + viz:** Use pandas methods then pipe to Plot
3. **For complex pipelines:** Use pipeframe package
4. **Restart kernel:** After code changes to pipeplotly source

## Examples

### Simple Plot
```python
df >> Plot() >> plot_points('x', 'y') >> show()
```

### With Styling
```python
df >> Plot() >> plot_points('x', 'y') >> add_color('cat', palette='viridis') >> set_theme('dark') >> show()
```

### Data Transformation
```python
df[df['x'] > 10].sort_values('y') >> Plot() >> plot_lines('x', 'y') >> show()
```

### Interactive
```python
df >> Plot() >> plot_points('x', 'y') >> to_interactive() >> show()
```
