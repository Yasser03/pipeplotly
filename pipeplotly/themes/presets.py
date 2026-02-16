"""Theme presets for PipePlotly."""

# Map theme names to both backends
PLOTNINE_THEMES = {
    'default': 'gray',
    'minimal': 'minimal',
    'classic': 'classic',
    'dark': 'dark',
    'light': 'light',
    'void': 'void',
    'bw': 'bw',
}

PLOTLY_THEMES = {
    'default': 'plotly',
    'minimal': 'simple_white',
    'classic': 'plotly_white',
    'dark': 'plotly_dark',
    'light': 'plotly_white',
    'void': 'none',
}

# Common color palettes that work across backends
COLOR_PALETTES = {
    'default': None,
    'viridis': ['#440154', '#414487', '#2a788e', '#22a884', '#7ad151', '#fde725'],
    'plasma': ['#0d0887', '#5302a3', '#8b0aa5', '#b83289', '#db5c68', '#f48849', '#febd2a', '#f0f921'],
    'colorblind': ['#0173B2', '#DE8F05', '#029E73', '#CC78BC', '#CA9161', '#949494', '#ECE133'],
    'pastel': ['#B4E7CE', '#FFD6BA', '#F7D4D4', '#C5D5EA', '#F5E6CC'],
}


def get_theme_for_backend(theme_name: str, backend: str) -> str:
    """
    Get the appropriate theme string for a given backend.
    
    Args:
        theme_name: Theme name (e.g., 'minimal', 'dark')
        backend: Backend name ('plotnine' or 'plotly')
        
    Returns:
        Theme string for the backend
    """
    if backend == 'plotnine':
        return PLOTNINE_THEMES.get(theme_name, 'gray')
    elif backend == 'plotly':
        return PLOTLY_THEMES.get(theme_name, 'plotly')
    else:
        raise ValueError(f"Unknown backend: {backend}")


def get_color_palette(palette_name: str):
    """
    Get a color palette by name.
    
    Args:
        palette_name: Palette name
        
    Returns:
        List of color values or None for default
    """
    return COLOR_PALETTES.get(palette_name, None)
