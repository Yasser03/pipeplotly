"""
Plotly Express backend implementation for interactive plots.
"""
from typing import Optional
from pipeplotly.backends.base import PlotBackend
from pipeplotly.core.state import PlotState


class PlotlyBackend(PlotBackend):
    """
    Backend that renders interactive plots using Plotly Express.
    
    This backend translates the Plot state into Plotly Express function calls
    and returns interactive Plotly Figure objects.
    """
    
    def render(self, plot_state: PlotState):
        """
        Render the plot using Plotly Express and display it.
        
        Args:
            plot_state: The current plot state to render
            
        Returns:
            plotly.graph_objects.Figure
        """
        import plotly.express as px
        
        plot_state.validate()
        
        # Create the figure based on geom_type
        fig = self._create_figure(plot_state)
        
        # Apply customizations
        fig = self._apply_layout(fig, plot_state)
        
        # Display
        fig.show()
        
        return fig
    
    def save(self, plot_state: PlotState, filename: str, 
             width: Optional[float] = None, height: Optional[float] = None,
             dpi: int = 300, **kwargs):
        """
        Save the plot to a file using Plotly.
        
        Args:
            plot_state: The current plot state to save
            filename: Output filename
            width: Plot width in pixels
            height: Plot height in pixels
            dpi: Resolution (not directly used by Plotly)
            **kwargs: Additional parameters
        """
        fig = self.render(plot_state)
        
        # Determine format from filename
        if filename.endswith('.html'):
            fig.write_html(filename, **kwargs)
        elif filename.endswith('.png'):
            # Convert inches to pixels if width/height provided
            save_kwargs = {}
            if width:
                save_kwargs['width'] = int(width * dpi)
            if height:
                save_kwargs['height'] = int(height * dpi)
            fig.write_image(filename, **{**save_kwargs, **kwargs})
        elif filename.endswith('.pdf'):
            fig.write_image(filename, **kwargs)
        elif filename.endswith('.svg'):
            fig.write_image(filename, **kwargs)
        else:
            # Default to HTML
            fig.write_html(filename, **kwargs)
    
    def to_html(self, plot_state: PlotState, filename: Optional[str] = None) -> str:
        """
        Export plot as HTML.
        
        Args:
            plot_state: The current plot state
            filename: Optional filename to save
            
        Returns:
            HTML string
        """
        fig = self._create_figure(plot_state)
        fig = self._apply_layout(fig, plot_state)
        
        html = fig.to_html()
        
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html)
        
        return html
    
    def _create_figure(self, state: PlotState):
        """Create Plotly Express figure based on geometry type."""
        import plotly.express as px
        
        # Build common parameters
        params = {
            'data_frame': state.data,
            'x': state.x,
            'y': state.y,
        }
        
        # Add color if specified
        if state.color:
            params['color'] = state.color
            if state.color_palette and isinstance(state.color_palette, list):
                params['color_discrete_sequence'] = state.color_palette
        
        # Add size if specified
        if state.size:
            params['size'] = state.size
        
        # Add facets
        if state.facet_rows:
            params['facet_row'] = state.facet_rows
        if state.facet_cols:
            params['facet_col'] = state.facet_cols
        
        # Create figure based on geometry type
        geom_type = state.geom_type
        
        if geom_type == 'point':
            fig = px.scatter(**params)
        elif geom_type == 'line':
            fig = px.line(**params)
        elif geom_type == 'bar':
            if state.y is None:
                # Count plot
                fig = px.histogram(data_frame=state.data, x=state.x, 
                                  color=state.color if state.color else None)
            else:
                fig = px.bar(**params)
        elif geom_type == 'histogram':
            bins = state.extra_params.get('bins', None)
            hist_params = {'data_frame': state.data, 'x': state.x}
            if state.color:
                hist_params['color'] = state.color
            if bins:
                hist_params['nbins'] = bins
            fig = px.histogram(**hist_params)
        elif geom_type == 'box':
            fig = px.box(**params)
        elif geom_type == 'violin':
            fig = px.violin(**params)
        elif geom_type == 'density':
            # Plotly doesn't have a direct density plot, use histogram with KDE
            # This is a simplified version
            fig = px.histogram(data_frame=state.data, x=state.x, 
                              marginal='violin',
                              color=state.color if state.color else None)
        elif geom_type == 'heatmap':
            # For heatmap, we need a pivot or aggregation
            # Simple version using density_heatmap
            fig = px.density_heatmap(data_frame=state.data, 
                                     x=state.x, y=state.y,
                                     z=state.color if state.color else None)
        else:
            raise ValueError(f"Unsupported geometry type for Plotly: {geom_type}")
        
        return fig
    
    def _apply_layout(self, fig, state: PlotState):
        """Apply layout customizations to the figure."""
        
        # Prepare layout updates
        layout_updates = {}
        
        # Title
        if state.title:
            layout_updates['title'] = state.title
        
        # Axis labels
        if state.x_label:
            layout_updates['xaxis_title'] = state.x_label
        if state.y_label:
            layout_updates['yaxis_title'] = state.y_label
        
        # Axis ranges
        if state.x_limits:
            layout_updates['xaxis_range'] = list(state.x_limits)
        if state.y_limits:
            layout_updates['yaxis_range'] = list(state.y_limits)
        
        # Axis scales
        if state.x_scale == 'log':
            layout_updates['xaxis_type'] = 'log'
        elif state.x_scale == 'reverse':
            layout_updates['xaxis_autorange'] = 'reversed'
        
        if state.y_scale == 'log':
            layout_updates['yaxis_type'] = 'log'
        elif state.y_scale == 'reverse':
            layout_updates['yaxis_autorange'] = 'reversed'
        
        # Legend position
        if state.legend_position == 'none':
            layout_updates['showlegend'] = False
        else:
            # Map position to Plotly legend settings
            position_map = {
                'right': {'x': 1.02, 'y': 1, 'xanchor': 'left'},
                'left': {'x': -0.02, 'y': 1, 'xanchor': 'right'},
                'top': {'x': 0.5, 'y': 1.02, 'yanchor': 'bottom', 'xanchor': 'center', 'orientation': 'h'},
                'bottom': {'x': 0.5, 'y': -0.02, 'yanchor': 'top', 'xanchor': 'center', 'orientation': 'h'},
            }
            if state.legend_position in position_map:
                layout_updates['legend'] = position_map[state.legend_position]
        
        # Apply theme template
        theme_map = {
            'default': 'plotly',
            'minimal': 'simple_white',
            'classic': 'plotly_white',
            'dark': 'plotly_dark',
            'light': 'plotly_white',
            'void': 'none',
        }
        template = theme_map.get(state.theme, 'plotly')
        layout_updates['template'] = template
        
        # Apply all updates
        if layout_updates:
            fig.update_layout(**layout_updates)
        
        return fig
