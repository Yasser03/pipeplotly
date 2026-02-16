"""
Core state management for PipePlotly plots.
"""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
import pandas as pd


@dataclass
class PlotState:
    """
    Immutable state object for plot configuration.
    
    This dataclass holds all the information needed to render a plot,
    including data, aesthetics, layers, theme settings, and backend type.
    """
    
    # Data
    data: Optional[pd.DataFrame] = None
    
    # Main geometry type
    geom_type: Optional[str] = None  # 'point', 'line', 'bar', etc.
    
    # Aesthetic mappings
    x: Optional[str] = None
    y: Optional[str] = None
    color: Optional[str] = None
    size: Optional[str] = None
    shape: Optional[str] = None
    alpha: Optional[str] = None
    fill: Optional[str] = None
    
    # Aesthetic parameters (non-mapped)
    color_value: Optional[str] = None
    size_value: Optional[float] = None
    alpha_value: Optional[float] = None
    
    # Faceting
    facet_rows: Optional[str] = None
    facet_cols: Optional[str] = None
    facet_wrap: Optional[str] = None
    
    # Labels
    title: Optional[str] = None
    x_label: Optional[str] = None
    y_label: Optional[str] = None
    
    # Scales
    x_scale: str = 'linear'  # 'linear', 'log', 'reverse'
    y_scale: str = 'linear'
    x_limits: Optional[tuple] = None
    y_limits: Optional[tuple] = None
    x_breaks: Optional[List] = None
    y_breaks: Optional[List] = None
    
    # Coordinate system
    coord_flip: bool = False
    coord_fixed: Optional[float] = None  # aspect ratio
    
    # Theme
    theme: str = 'default'
    
    # Additional layers (smooth, etc.)
    smooth: bool = False
    smooth_method: str = 'loess'
    smooth_params: Dict[str, Any] = field(default_factory=dict)
    
    # Legend
    legend_position: str = 'right'  # 'right', 'left', 'top', 'bottom', 'none'
    legend_title: Optional[str] = None
    
    # Backend
    backend: str = 'plotnine'  # 'plotnine' or 'plotly'
    
    # Color palette
    color_palette: Optional[Union[str, List]] = None
    
    # Additional parameters for specific plot types
    extra_params: Dict[str, Any] = field(default_factory=dict)
    
    def copy(self, **updates) -> 'PlotState':
        """
        Create a copy of this state with updated fields.
        
        Args:
            **updates: Fields to update in the new state
            
        Returns:
            New PlotState instance with updates applied
        """
        import copy
        new_state = copy.deepcopy(self)
        for key, value in updates.items():
            if hasattr(new_state, key):
                setattr(new_state, key, value)
            else:
                # Store unknown parameters in extra_params
                new_state.extra_params[key] = value
        return new_state
    
    def validate(self) -> None:
        """
        Validate the current plot state.
        
        Raises:
            ValueError: If state is invalid (e.g., missing required fields)
        """
        if self.data is None:
            raise ValueError("Plot data cannot be None")
        
        if self.geom_type is None:
            raise ValueError("Plot geometry type must be specified (use plot_points, plot_lines, etc.)")
        
        # Validate that mapped aesthetics exist as columns
        if self.x and isinstance(self.x, str) and self.x not in self.data.columns:
            raise ValueError(f"Column '{self.x}' not found in data")
        
        if self.y and isinstance(self.y, str) and self.y not in self.data.columns:
            raise ValueError(f"Column '{self.y}' not found in data")
        
        if self.color and isinstance(self.color, str) and self.color not in self.data.columns:
            raise ValueError(f"Column '{self.color}' not found in data")
        
        if self.size and isinstance(self.size, str) and self.size not in self.data.columns:
            raise ValueError(f"Column '{self.size}' not found in data")
        
        if self.shape and isinstance(self.shape, str) and self.shape not in self.data.columns:
            raise ValueError(f"Column '{self.shape}' not found in data")
        
        if self.alpha and isinstance(self.alpha, str) and self.alpha not in self.data.columns:
            raise ValueError(f"Column '{self.alpha}' not found in data")
