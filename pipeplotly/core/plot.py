"""
Main Plot class for PipePlotly.

This module provides the core Plot class that supports verb-based API
for creating visualizations with method chaining and pipe operators.
"""
from typing import Any, Optional, Union
import pandas as pd
from pipeplotly.core.state import PlotState


class Plot:
    """
    Main visualization class supporting verb-based, pipe-friendly API.
    
    The Plot class uses an immutable state pattern where each verb operation
    returns a new Plot instance with updated state. This allows for both
    method chaining and pipe operator usage.
    
    Examples:
        Method chaining:
        >>> plot = (Plot(df)
        ...     .plot_points('x', 'y')
        ...     .add_color('category')
        ...     .set_theme('minimal')
        ...     .show())
        
        Pipe operator:
        >>> from pipeplotly.verbs import plot_points, add_color, show
        >>> plot = df >> Plot() >> plot_points('x', 'y') >> add_color('category') >> show()
    
    Attributes:
        state (PlotState): The current plot configuration state
    """
    
    def __init__(self, data: Optional[pd.DataFrame] = None, state: Optional[PlotState] = None):
        """
        Initialize a Plot instance.
        
        Args:
            data: pandas DataFrame containing the data to plot
            state: Existing PlotState (used internally for creating copies)
        """
        if state is not None:
            self.state = state
        else:
            self.state = PlotState(data=data)
    
    def _copy(self, **updates) -> 'Plot':
        """
        Create a new Plot instance with updated state.
        
        Args:
            **updates: Fields to update in the new state
            
        Returns:
            New Plot instance with updated state
        """
        new_state = self.state.copy(**updates)
        return Plot(state=new_state)
    
    # ============================================================
    # INITIALIZATION VERBS - Define the plot type
    # ============================================================
    
    def plot_points(self, x: str, y: str, **kwargs) -> 'Plot':
        """
        Create a scatter plot.
        
        Args:
            x: Column name for x-axis
            y: Column name for y-axis
            **kwargs: Additional parameters passed to the geometry
            
        Returns:
            New Plot instance configured for scatter plot
            
        Examples:
            >>> Plot(df).plot_points('x', 'y')
        """
        return self._copy(geom_type='point', x=x, y=y, **kwargs)
    
    def plot_lines(self, x: str, y: str, **kwargs) -> 'Plot':
        """
        Create a line plot.
        
        Args:
            x: Column name for x-axis
            y: Column name for y-axis
            **kwargs: Additional parameters
            
        Returns:
            New Plot instance configured for line plot
        """
        return self._copy(geom_type='line', x=x, y=y, **kwargs)
    
    def plot_bars(self, x: str, y: Optional[str] = None, **kwargs) -> 'Plot':
        """
        Create a bar chart.
        
        Args:
            x: Column name for x-axis (categories)
            y: Column name for y-axis (values). If None, counts are used
            **kwargs: Additional parameters
            
        Returns:
            New Plot instance configured for bar chart
        """
        return self._copy(geom_type='bar', x=x, y=y, **kwargs)
    
    def plot_histogram(self, x: str, bins: Optional[int] = None, **kwargs) -> 'Plot':
        """
        Create a histogram.
        
        Args:
            x: Column name for values
            bins: Number of bins (optional)
            **kwargs: Additional parameters
            
        Returns:
            New Plot instance configured for histogram
        """
        extra = {'bins': bins} if bins else {}
        return self._copy(geom_type='histogram', x=x, y=None, **{**extra, **kwargs})
    
    def plot_box(self, x: Optional[str] = None, y: Optional[str] = None, **kwargs) -> 'Plot':
        """
        Create a box plot.
        
        Args:
            x: Column name for categories (optional)
            y: Column name for values
            **kwargs: Additional parameters
            
        Returns:
            New Plot instance configured for box plot
        """
        return self._copy(geom_type='box', x=x, y=y, **kwargs)
    
    def plot_violin(self, x: Optional[str] = None, y: Optional[str] = None, **kwargs) -> 'Plot':
        """
        Create a violin plot.
        
        Args:
            x: Column name for categories (optional)
            y: Column name for values
            **kwargs: Additional parameters
            
        Returns:
            New Plot instance configured for violin plot
        """
        return self._copy(geom_type='violin', x=x, y=y, **kwargs)
    
    def plot_density(self, x: str, **kwargs) -> 'Plot':
        """
        Create a density plot.
        
        Args:
            x: Column name for values
            **kwargs: Additional parameters
            
        Returns:
            New Plot instance configured for density plot
        """
        return self._copy(geom_type='density', x=x, y=None, **kwargs)
    
    def plot_heatmap(self, x: str, y: str, color: str, **kwargs) -> 'Plot':
        """
        Create a heatmap.
        
        Args:
            x: Column name for x-axis
            y: Column name for y-axis
            color: Column name for color values
            **kwargs: Additional parameters
            
        Returns:
            New Plot instance configured for heatmap
        """
        return self._copy(geom_type='heatmap', x=x, y=y, color=color, **kwargs)
    
    # ============================================================
    # AESTHETIC VERBS - Map data to visual properties
    # ============================================================
    
    def add_color(self, column: Optional[str] = None, value: Optional[str] = None, 
                  palette: Optional[Union[str, list]] = None, **kwargs) -> 'Plot':
        """
        Map a column to color or set a fixed color.
        
        Args:
            column: Column name to map to color
            value: Fixed color value (if not mapping to data)
            palette: Color palette name or list of colors
            **kwargs: Additional parameters
            
        Returns:
            New Plot instance with color aesthetic added
            
        Examples:
            >>> plot.add_color('species')  # Map to column
            >>> plot.add_color(value='red')  # Fixed color
        """
        updates = {}
        if column:
            updates['color'] = column
        if value:
            updates['color_value'] = value
        if palette:
            updates['color_palette'] = palette
        return self._copy(**{**updates, **kwargs})
    
    def add_size(self, column: Optional[str] = None, value: Optional[float] = None, **kwargs) -> 'Plot':
        """
        Map a column to size or set a fixed size.
        
        Args:
            column: Column name to map to size
            value: Fixed size value
            **kwargs: Additional parameters
            
        Returns:
            New Plot instance with size aesthetic added
        """
        updates = {}
        if column:
            updates['size'] = column
        if value:
            updates['size_value'] = value
        return self._copy(**{**updates, **kwargs})
    
    def add_shape(self, column: str, **kwargs) -> 'Plot':
        """
        Map a column to point shape.
        
        Args:
            column: Column name to map to shape
            **kwargs: Additional parameters
            
        Returns:
            New Plot instance with shape aesthetic added
        """
        return self._copy(shape=column, **kwargs)
    
    def add_alpha(self, column: Optional[str] = None, value: Optional[float] = None, **kwargs) -> 'Plot':
        """
        Map a column to transparency or set fixed alpha.
        
        Args:
            column: Column name to map to alpha
            value: Fixed alpha value (0-1)
            **kwargs: Additional parameters
            
        Returns:
            New Plot instance with

 aesthetic added
        """
        updates = {}
        if column:
            updates['alpha'] = column
        if value:
            updates['alpha_value'] = value
        return self._copy(**{**updates, **kwargs})
    
    def add_facets(self, rows: Optional[str] = None, cols: Optional[str] = None, 
                   wrap: Optional[str] = None, **kwargs) -> 'Plot':
        """
        Add faceting to create small multiples.
        
        Args:
            rows: Column name for row facets
            cols: Column name for column facets
            wrap: Column name for wrapped facets
            **kwargs: Additional parameters
            
        Returns:
            New Plot instance with facets added
        """
        return self._copy(facet_rows=rows, facet_cols=cols, facet_wrap=wrap, **kwargs)
    
    def add_labels(self, title: Optional[str] = None, x: Optional[str] = None, 
                   y: Optional[str] = None, **kwargs) -> 'Plot':
        """
        Add or modify plot labels.
        
        Args:
            title: Plot title
            x: X-axis label
            y: Y-axis label
            **kwargs: Additional parameters
            
        Returns:
            New Plot instance with labels updated
        """
        updates = {}
        if title is not None:
            updates['title'] = title
        if x is not None:
            updates['x_label'] = x
        if y is not None:
            updates['y_label'] = y
        return self._copy(**{**updates, **kwargs})
    
    def add_smooth(self, method: str = 'loess', **kwargs) -> 'Plot':
        """
        Add a smoothing trend line.
        
        Args:
            method: Smoothing method ('loess', 'lm', etc.)
            **kwargs: Additional parameters for smoothing
            
        Returns:
            New Plot instance with smooth layer added
        """
        return self._copy(smooth=True, smooth_method=method, smooth_params=kwargs)
    
    # ============================================================
    # TRANSFORMATION VERBS - Modify scales and coordinates
    # ============================================================
    
    def scale_x_log(self) -> 'Plot':
        """Apply logarithmic scale to x-axis."""
        return self._copy(x_scale='log')
    
    def scale_y_log(self) -> 'Plot':
        """Apply logarithmic scale to y-axis."""
        return self._copy(y_scale='log')
    
    def scale_x_reverse(self) -> 'Plot':
        """Reverse the x-axis."""
        return self._copy(x_scale='reverse')
    
    def scale_y_reverse(self) -> 'Plot':
        """Reverse the y-axis."""
        return self._copy(y_scale='reverse')
    
    def xlim(self, min_val: float, max_val: float) -> 'Plot':
        """
        Set x-axis limits.
        
        Args:
            min_val: Minimum value
            max_val: Maximum value
            
        Returns:
            New Plot instance with x limits set
        """
        return self._copy(x_limits=(min_val, max_val))
    
    def ylim(self, min_val: float, max_val: float) -> 'Plot':
        """
        Set y-axis limits.
        
        Args:
            min_val: Minimum value
            max_val: Maximum value
            
        Returns:
            New Plot instance with y limits set
        """
        return self._copy(y_limits=(min_val, max_val))
    
    def coord_flip(self) -> 'Plot':
        """Flip the coordinate system (swap x and y axes)."""
        return self._copy(coord_flip=True)
    
    def coord_fixed(self, ratio: float = 1.0) -> 'Plot':
        """
        Set fixed aspect ratio.
        
        Args:
            ratio: Aspect ratio (y/x)
            
        Returns:
            New Plot instance with fixed coordinates
        """
        return self._copy(coord_fixed=ratio)
    
    # ============================================================
    # THEME VERBS - Customize appearance
    # ============================================================
    
    def set_theme(self, theme: str = 'default') -> 'Plot':
        """
        Set the plot theme.
        
        Args:
            theme: Theme name ('default', 'minimal', 'dark', 'classic', etc.)
            
        Returns:
            New Plot instance with theme set
        """
        return self._copy(theme=theme)
    
    # ============================================================
    # OUTPUT VERBS - Render and export
    # ============================================================
    
    def show(self) -> 'Plot':
        """
        Display the plot.
        
        Returns:
            Self for potential chaining
        """
        self.state.validate()
        
        # Import backend lazily
        if self.state.backend == 'plotnine':
            from pipeplotly.backends.plotnine_backend import PlotnineBackend
            backend = PlotnineBackend()
        else:
            from pipeplotly.backends.plotly_backend import PlotlyBackend
            backend = PlotlyBackend()
        
        backend.render(self.state)
        return self
    
    def save(self, filename: str, width: Optional[float] = None, 
             height: Optional[float] = None, dpi: int = 300, **kwargs) -> 'Plot':
        """
        Save the plot to a file.
        
        Args:
            filename: Output filename
            width: Plot width
            height: Plot height
            dpi: Resolution (dots per inch)
            **kwargs: Additional parameters
            
        Returns:
            Self for potential chaining
        """
        self.state.validate()
        
        # Import backend lazily
        if self.state.backend == 'plotnine':
            from pipeplotly.backends.plotnine_backend import PlotnineBackend
            backend = PlotnineBackend()
        else:
            from pipeplotly.backends.plotly_backend import PlotlyBackend
            backend = PlotlyBackend()
        
        backend.save(self.state, filename, width=width, height=height, dpi=dpi, **kwargs)
        return self
    
    def to_interactive(self) -> 'Plot':
        """
        Convert to interactive Plotly visualization.
        
        Returns:
            New Plot instance with Plotly backend
        """
        return self._copy(backend='plotly')
    
    def to_static(self) -> 'Plot':
        """
        Convert to static plotnine visualization.
        
        Returns:
            New Plot instance with plotnine backend
        """
        return self._copy(backend='plotnine')
    
    def to_html(self, filename: Optional[str] = None) -> str:
        """
        Export as HTML (primarily for interactive plots).
        
        Args:
            filename: Optional filename to save HTML
            
        Returns:
            HTML string representation
        """
        if self.state.backend != 'plotly':
            # Convert to plotly first
            plot = self.to_interactive()
        else:
            plot = self
        
        from pipeplotly.backends.plotly_backend import PlotlyBackend
        backend = PlotlyBackend()
        return backend.to_html(plot.state, filename)
    
    # ============================================================
    # PIPE OPERATOR SUPPORT
    # ============================================================
    
    def __rshift__(self, other):
        """
        Support for >> pipe operator (Plot on the left).
        
        This allows: Plot(df) >> plot_points('x', 'y')
        
        Args:
            other: Either a verb function or another operation
            
        Returns:
            Result of applying other to self
        """
        if callable(other):
            return other(self)
        return NotImplemented
    
    def __rrshift__(self, other):
        """
        Support for >> pipe operator (Plot on the right).
        
        This allows: 
        - df >> Plot()  (pandas DataFrame)
        - pf >> Plot()  (pipeframe DataFrame)
        
        When a DataFrame is piped into Plot(), this method is called
        because DataFrame doesn't have __rshift__ for Plot objects.
        
        Args:
            other: The object being piped (DataFrame, pipeframe, etc.)
            
        Returns:
            New Plot instance with the piped data
        """
        # Check if it's a pandas DataFrame
        if isinstance(other, pd.DataFrame):
            return Plot(data=other)
        
        # Check if it's a pipeframe DataFrame or similar (has _df attribute)
        try:
            if hasattr(other, '_df') and isinstance(other._df, pd.DataFrame):
                # pipeframe stores the underlying DataFrame in _df
                return Plot(data=other._df)
            elif hasattr(other, 'to_pandas') and callable(other.to_pandas):
                # Some libraries have to_pandas() method
                return Plot(data=other.to_pandas())
        except (AttributeError, TypeError):
            pass
        
        # If it's callable, apply it
        if callable(other):
            return other(self)
        
        return NotImplemented
    
    def __repr__(self) -> str:
        """String representation of the Plot."""
        geom = self.state.geom_type or 'uninitialized'
        backend = self.state.backend
        data_shape = self.state.data.shape if self.state.data is not None else 'None'
        return f"Plot(geom='{geom}', backend='{backend}', data_shape={data_shape})"
