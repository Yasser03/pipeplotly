"""
Verb functions for use with pipe operators.

This module provides standalone verb functions that can be used with the >> operator
for a more functional programming style. These are alternatives to method chaining.

Examples:
    Using pipe operator:
    >>> from pipeplotly import Plot
    >>> from pipeplotly.verbs import plot_points, add_color, add_labels, show
    >>> 
    >>> plot = (df 
    ...     >> Plot()
    ...     >> plot_points('x', 'y')
    ...     >> add_color('category')
    ...     >> add_labels(title='My Plot')
    ...     >> show())
"""
from typing import Optional, Union


# ============================================================
# INITIALIZATION VERBS
# ============================================================

def plot_points(x: str, y: str, **kwargs):
    """Create a scatter plot."""
    def _apply(plot):
        return plot.plot_points(x, y, **kwargs)
    return _apply


def plot_lines(x: str, y: str, **kwargs):
    """Create a line plot."""
    def _apply(plot):
        return plot.plot_lines(x, y, **kwargs)
    return _apply


def plot_bars(x: str, y: Optional[str] = None, **kwargs):
    """Create a bar chart."""
    def _apply(plot):
        return plot.plot_bars(x, y, **kwargs)
    return _apply


def plot_histogram(x: str, bins: Optional[int] = None, **kwargs):
    """Create a histogram."""
    def _apply(plot):
        return plot.plot_histogram(x, bins=bins, **kwargs)
    return _apply


def plot_box(x: Optional[str] = None, y: Optional[str] = None, **kwargs):
    """Create a box plot."""
    def _apply(plot):
        return plot.plot_box(x, y, **kwargs)
    return _apply


def plot_violin(x: Optional[str] = None, y: Optional[str] = None, **kwargs):
    """Create a violin plot."""
    def _apply(plot):
        return plot.plot_violin(x, y, **kwargs)
    return _apply


def plot_density(x: str, **kwargs):
    """Create a density plot."""
    def _apply(plot):
        return plot.plot_density(x, **kwargs)
    return _apply


def plot_heatmap(x: str, y: str, color: str, **kwargs):
    """Create a heatmap."""
    def _apply(plot):
        return plot.plot_heatmap(x, y, color, **kwargs)
    return _apply


# ============================================================
# AESTHETIC VERBS
# ============================================================

def add_color(column: Optional[str] = None, value: Optional[str] = None,
              palette: Optional[Union[str, list]] = None, **kwargs):
    """Map a column to color or set a fixed color."""
    def _apply(plot):
        return plot.add_color(column=column, value=value, palette=palette, **kwargs)
    return _apply


def add_size(column: Optional[str] = None, value: Optional[float] = None, **kwargs):
    """Map a column to size or set a fixed size."""
    def _apply(plot):
        return plot.add_size(column=column, value=value, **kwargs)
    return _apply


def add_shape(column: str, **kwargs):
    """Map a column to point shape."""
    def _apply(plot):
        return plot.add_shape(column, **kwargs)
    return _apply


def add_alpha(column: Optional[str] = None, value: Optional[float] = None, **kwargs):
    """Map a column to transparency or set fixed alpha."""
    def _apply(plot):
        return plot.add_alpha(column=column, value=value, **kwargs)
    return _apply


def add_facets(rows: Optional[str] = None, cols: Optional[str] = None,
               wrap: Optional[str] = None, **kwargs):
    """Add faceting to create small multiples."""
    def _apply(plot):
        return plot.add_facets(rows=rows, cols=cols, wrap=wrap, **kwargs)
    return _apply


def add_labels(title: Optional[str] = None, x: Optional[str] = None,
               y: Optional[str] = None, **kwargs):
    """Add or modify plot labels."""
    def _apply(plot):
        return plot.add_labels(title=title, x=x, y=y, **kwargs)
    return _apply


def add_smooth(method: str = 'loess', **kwargs):
    """Add a smoothing trend line."""
    def _apply(plot):
        return plot.add_smooth(method=method, **kwargs)
    return _apply


# ============================================================
# TRANSFORMATION VERBS
# ============================================================

def scale_x_log():
    """Apply logarithmic scale to x-axis."""
    def _apply(plot):
        return plot.scale_x_log()
    return _apply


def scale_y_log():
    """Apply logarithmic scale to y-axis."""
    def _apply(plot):
        return plot.scale_y_log()
    return _apply


def scale_x_reverse():
    """Reverse the x-axis."""
    def _apply(plot):
        return plot.scale_x_reverse()
    return _apply


def scale_y_reverse():
    """Reverse the y-axis."""
    def _apply(plot):
        return plot.scale_y_reverse()
    return _apply


def xlim(min_val: float, max_val: float):
    """Set x-axis limits."""
    def _apply(plot):
        return plot.xlim(min_val, max_val)
    return _apply


def ylim(min_val: float, max_val: float):
    """Set y-axis limits."""
    def _apply(plot):
        return plot.ylim(min_val, max_val)
    return _apply


def coord_flip():
    """Flip the coordinate system (swap x and y axes)."""
    def _apply(plot):
        return plot.coord_flip()
    return _apply


def coord_fixed(ratio: float = 1.0):
    """Set fixed aspect ratio."""
    def _apply(plot):
        return plot.coord_fixed(ratio=ratio)
    return _apply


# ============================================================
# THEME VERBS
# ============================================================

def set_theme(theme: str = 'default'):
    """Set the plot theme."""
    def _apply(plot):
        return plot.set_theme(theme=theme)
    return _apply


# ============================================================
# OUTPUT VERBS
# ============================================================

def show():
    """Display the plot."""
    def _apply(plot):
        return plot.show()
    return _apply


def save(filename: str, width: Optional[float] = None,
         height: Optional[float] = None, dpi: int = 300, **kwargs):
    """Save the plot to a file."""
    def _apply(plot):
        return plot.save(filename, width=width, height=height, dpi=dpi, **kwargs)
    return _apply


def to_interactive():
    """Convert to interactive Plotly visualization.""" 
    def _apply(plot):
        return plot.to_interactive()
    return _apply


def to_static():
    """Convert to static plotnine visualization."""
    def _apply(plot):
        return plot.to_static()
    return _apply


def to_html(filename: Optional[str] = None):
    """Export as HTML."""
    def _apply(plot):
        return plot.to_html(filename=filename)
    return _apply
