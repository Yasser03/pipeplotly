"""
plotnine backend implementation for static Grammar of Graphics plots.
"""
from typing import Optional
from pipeplotly.backends.base import PlotBackend
from pipeplotly.core.state import PlotState


class PlotnineBackend(PlotBackend):
    """
    Backend that renders plots using plotnine (Grammar of Graphics).
    
    This backend translates the Plot state into plotnine ggplot objects
    and applies the appropriate geometry, aesthetics, scales, and themes.
    """
    
    def render(self, plot_state: PlotState):
        """
        Render the plot using plotnine and display it.
        
        Args:
            plot_state: The current plot state to render
            
        Returns:
            plotnine ggplot object
        """
        import plotnine as p9
        
        plot_state.validate()
        
        # Start with data
        gg = p9.ggplot(plot_state.data)
        
        # Build aesthetic mapping
        aes_mapping = self._build_aesthetics(plot_state)
        
        # Add geometry based on geom_type
        geom = self._get_geometry(plot_state, aes_mapping)
        gg = gg + geom
        
        # Add smooth if requested
        if plot_state.smooth:
            smooth_aes = p9.aes(x=plot_state.x, y=plot_state.y)
            gg = gg + p9.geom_smooth(smooth_aes, method=plot_state.smooth_method, 
                                     **plot_state.smooth_params)
        
        # Apply scales
        gg = self._apply_scales(gg, plot_state)
        
        # Apply coordinate transformations
        gg = self._apply_coords(gg, plot_state)
        
        # Apply facets
        gg = self._apply_facets(gg, plot_state)
        
        # Apply labels
        gg = self._apply_labels(gg, plot_state)
        
        # Apply theme
        gg = self._apply_theme(gg, plot_state)
        
        # Display - Use IPython display for Jupyter notebooks
        try:
            from IPython.display import display
            display(gg)
        except (ImportError, NameError):
            # Fallback for non-Jupyter environments
            # In regular Python, ggplot objects auto-display when evaluated
            print(gg)
        
        return gg
    
    def save(self, plot_state: PlotState, filename: str, 
             width: Optional[float] = None, height: Optional[float] = None,
             dpi: int = 300, **kwargs):
        """
        Save the plot to a file using plotnine.
        
        Args:
            plot_state: The current plot state to save
            filename: Output filename
            width: Plot width in inches
            height: Plot height in inches
            dpi: Resolution
            **kwargs: Additional parameters
        """
        # Render to get ggplot object
        gg = self.render(plot_state)
        
        # Save
        save_params = {'dpi': dpi, 'verbose': False}
        if width:
            save_params['width'] = width
        if height:
            save_params['height'] = height
        
        gg.save(filename, **{**save_params, **kwargs})
    
    def _build_aesthetics(self, state: PlotState) -> dict:
        """Build plotnine aesthetic mapping from state."""
        import plotnine as p9
        
        aes_dict = {}
        
        if state.x:
            aes_dict['x'] = state.x
        if state.y:
            aes_dict['y'] = state.y
        if state.color:
            aes_dict['color'] = state.color
        if state.fill:
            aes_dict['fill'] = state.fill
        if state.size:
            aes_dict['size'] = state.size
        if state.shape:
            aes_dict['shape'] = state.shape
        if state.alpha:
            aes_dict['alpha'] = state.alpha
        
        return p9.aes(**aes_dict)
    
    def _get_geometry(self, state: PlotState, aes_mapping):
        """Get the appropriate plotnine geometry based on geom_type."""
        import plotnine as p9
        
        # Fixed aesthetics (non-mapped)
        geom_params = {}
        if state.color_value:
            geom_params['color'] = state.color_value
        if state.size_value:
            geom_params['size'] = state.size_value
        if state.alpha_value:
            geom_params['alpha'] = state.alpha_value
        
        geom_type = state.geom_type
        
        if geom_type == 'point':
            return p9.geom_point(aes_mapping, **geom_params)
        elif geom_type == 'line':
            return p9.geom_line(aes_mapping, **geom_params)
        elif geom_type == 'bar':
            if state.y is None:
                return p9.geom_bar(aes_mapping, stat='count', **geom_params)
            else:
                return p9.geom_col(aes_mapping, **geom_params)
        elif geom_type == 'histogram':
            bins = state.extra_params.get('bins', 30)
            return p9.geom_histogram(aes_mapping, bins=bins, **geom_params)
        elif geom_type == 'box':
            return p9.geom_boxplot(aes_mapping, **geom_params)
        elif geom_type == 'violin':
            return p9.geom_violin(aes_mapping, **geom_params)
        elif geom_type == 'density':
            return p9.geom_density(aes_mapping, **geom_params)
        elif geom_type == 'heatmap':
            return p9.geom_tile(aes_mapping, **geom_params)
        else:
            raise ValueError(f"Unsupported geometry type: {geom_type}")
    
    def _apply_scales(self, gg, state: PlotState):
        """Apply scale transformations."""
        import plotnine as p9
        
        # X scale
        if state.x_scale == 'log':
            gg = gg + p9.scale_x_log10()
        elif state.x_scale == 'reverse':
            gg = gg + p9.scale_x_reverse()
        
        if state.x_limits:
            gg = gg + p9.xlim(state.x_limits)
        
        # Y scale
        if state.y_scale == 'log':
            gg = gg + p9.scale_y_log10()
        elif state.y_scale == 'reverse':
            gg = gg + p9.scale_y_reverse()
        
        if state.y_limits:
            gg = gg + p9.ylim(state.y_limits)
        
        # Color palette
        if state.color and state.color_palette:
            if isinstance(state.color_palette, str):
                # Check if the color column is categorical or continuous
                is_categorical = state.data[state.color].dtype.name in ['object', 'category', 'bool', 'str']
                
                # Matplotlib colormaps
                matplotlib_cmaps = ['viridis', 'plasma', 'inferno', 'magma', 'cividis', 
                                   'twilight', 'coolwarm', 'seismic', 'rainbow', 'jet']
                
                if state.color_palette in matplotlib_cmaps:
                    if is_categorical:
                        # For categorical data, sample discrete colors from the colormap
                        import matplotlib.pyplot as plt
                        n_colors = state.data[state.color].nunique()
                        cmap = plt.get_cmap(state.color_palette)
                        colors = [cmap(i / (n_colors - 1 if n_colors > 1 else 1)) for i in range(n_colors)]
                        # Convert to hex
                        import matplotlib.colors as mcolors
                        colors_hex = [mcolors.to_hex(c) for c in colors]
                        gg = gg + p9.scale_color_manual(values=colors_hex)
                    else:
                        # For continuous data, use colormap scale
                        gg = gg + p9.scale_color_cmap(cmap_name=state.color_palette)
                else:
                    # Try ColorBrewer palette (always discrete)
                    try:
                        gg = gg + p9.scale_color_brewer(type='qual', palette=state.color_palette)
                    except (ValueError, AttributeError):
                        # If palette not found, skip it and use default
                        pass
            else:
                # Custom color list
                gg = gg + p9.scale_color_manual(values=state.color_palette)
        
        return gg
    
    def _apply_coords(self, gg, state: PlotState):
        """Apply coordinate system transformations."""
        import plotnine as p9
        
        if state.coord_flip:
            gg = gg + p9.coord_flip()
        elif state.coord_fixed:
            gg = gg + p9.coord_fixed(ratio=state.coord_fixed)
        
        return gg
    
    def _apply_facets(self, gg, state: PlotState):
        """Apply faceting."""
        import plotnine as p9
        
        if state.facet_wrap:
            gg = gg + p9.facet_wrap(f'~{state.facet_wrap}')
        elif state.facet_rows or state.facet_cols:
            row_var = state.facet_rows if state.facet_rows else '.'
            col_var = state.facet_cols if state.facet_cols else '.'
            gg = gg + p9.facet_grid(f'{row_var}~{col_var}')
        
        return gg
    
    def _apply_labels(self, gg, state: PlotState):
        """Apply labels to the plot."""
        import plotnine as p9
        
        labels = {}
        if state.title:
            labels['title'] = state.title
        if state.x_label:
            labels['x'] = state.x_label
        if state.y_label:
            labels['y'] = state.y_label
        
        if labels:
            gg = gg + p9.labs(**labels)
        
        return gg
    
    def _apply_theme(self, gg, state: PlotState):
        """Apply theme to the plot."""
        import plotnine as p9
        
        theme_map = {
            'default': p9.theme_gray,
            'minimal': p9.theme_minimal,
            'classic': p9.theme_classic,
            'dark': p9.theme_dark,
            'light': p9.theme_light,
            'void': p9.theme_void,
            'bw': p9.theme_bw,
        }
        
        theme_func = theme_map.get(state.theme, p9.theme_gray)
        gg = gg + theme_func()
        
        # Apply legend position
        if state.legend_position == 'none':
            gg = gg + p9.theme(legend_position='none')
        else:
            gg = gg + p9.theme(legend_position=state.legend_position)
        
        return gg
