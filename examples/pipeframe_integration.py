"""
PipeFrame Integration Examples

This example demonstrates how PipePlotly seamlessly integrates with the pipeframe package
for advanced data manipulation pipelines combined with visualization.
"""

import pandas as pd
import numpy as np

# First, let's show it works with regular pandas
print("="*60)
print("Example 1: Regular Pandas DataFrame")
print("="*60)

from pipeplotly import Plot
from pipeplotly.verbs import plot_points, add_color, show

df = pd.DataFrame({
    'x': range(20),
    'y': np.random.randn(20).cumsum(),
    'category': np.random.choice(['A', 'B'], 20)
})

# Works with pandas DataFrame
plot = (df
    >> Plot()
    >> plot_points('x', 'y')
    >> add_color('category')
    >> show())

print("[OK] Pandas DataFrame works!")

# Now with pipeframe (if installed)
print("\n" + "="*60)
print("Example 2: PipeFrame Integration (if installed)")
print("="*60)

try:
    from pipeframe import DataFrame as pf_df
    
    # Wrap DataFrame in PipeFrame
    pf = pf_df(df)
    
    # Can pipe directly from PipeFrame to Plot!
    plot = (pf
        >> Plot()
        >> plot_points('x', 'y')
        >> add_color('category')
        >> show())
    
    print("✓ PipeFrame integration works!")
    
    # Advanced: Combine pipeframe operations with plotting
    print("\n" + "="*60)
    print("Example 3: Data Manipulation + Visualization Pipeline")
    print("="*60)
    
    result = (pf_df({
        'x': range(100),
        'y': np.random.randn(100),
        'category': np.random.choice(['A', 'B', 'C'], 100)
    })
    # Data manipulation with pipeframe
    >> (lambda pf: pf[pf._df['x'] > 25])  # Filter
    >> (lambda pf: pf.sort_values('y'))     # Sort
    # Visualization with pipeplotly
    >> Plot()
    >> plot_points('x', 'y')
    >> add_color('category', palette='viridis')
    >> show())
    
    print("✓ Combined pipeline works!")

except ImportError:
    print("⚠ PipeFrame not installed")
    print("Install with: pip install pipeframe")
    print("\nPipePlotly works fine without it - you can still use:")
    print("  df >> Plot() >> plot_points('x', 'y') >> show()")

print("\n" + "="*60)
print("Summary")
print("="*60)
print("""
PipePlotly supports piping from:
✓ pandas DataFrames (df >> Plot())
✓ pipeframe DataFrames (pf >> Plot()) 
✓ Any DataFrame-like object with ._df or .to_pandas()

Both styles work:
1. Method chaining: Plot(df).plot_points('x', 'y').show()
2. Pipe operator:   df >> Plot() >> plot_points('x', 'y') >> show()

Choose what fits your workflow!
""")
