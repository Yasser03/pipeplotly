"""
PipePlotly - A verb-based, pipe-friendly API for creating visualizations.

This package provides an intuitive interface for creating both static (plotnine) 
and interactive (Plotly Express) visualizations with natural language-like syntax.

Quick Start:
    Method chaining style:
    >>> from pipeplotly import Plot
    >>> plot = (Plot(df)
    ...     .plot_points('x', 'y')
    ...     .add_color('category')
    ...     .show())
    
    Pipe operator style:
    >>> from pipeplotly import Plot
    >>> from pipeplotly.verbs import plot_points, add_color, show
    >>> plot = df >> Plot() >> plot_points('x', 'y') >> add_color('category') >> show()
"""
from pipeplotly.core.plot import Plot
from pipeplotly.core.state import PlotState

# Import verb functions for pipe operator usage
from pipeplotly import verbs

__version__ = "0.2.0"
__all__ = [
    'Plot', 
    'PlotState',
    'verbs',  # All verb functions available via pipeplotly.verbs
]
