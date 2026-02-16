"""
Abstract base class for plot backends.
"""
from abc import ABC, abstractmethod
from typing import Optional
from pipeplotly.core.state import PlotState


class PlotBackend(ABC):
    """
    Abstract base class defining the interface for plot backends.
    
    Backends are responsible for translating the Plot state into
    actual visualizations using specific libraries (plotnine, Plotly, etc.).
    """
    
    @abstractmethod
    def render(self, plot_state: PlotState):
        """
        Render the plot and display it.
        
        Args:
            plot_state: The current plot state to render
            
        Returns:
            The rendered plot object (specific to backend)
        """
        pass
    
    @abstractmethod
    def save(self, plot_state: PlotState, filename: str, 
             width: Optional[float] = None, height: Optional[float] = None,
             dpi: int = 300, **kwargs):
        """
        Save the plot to a file.
        
        Args:
            plot_state: The current plot state to save
            filename: Output filename
            width: Plot width
            height: Plot height
            dpi: Resolution (dots per inch)
            **kwargs: Additional backend-specific parameters
        """
        pass
