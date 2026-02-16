import pytest
import pandas as pd
from pipeplotly import Plot
from pipeplotly.verbs import add_alpha, add_size, add_color

@pytest.fixture
def df():
    return pd.DataFrame({
        'x': [1, 2, 3],
        'y': [4, 5, 6],
        'category': ['A', 'B', 'A']
    })

def test_add_alpha_fixed_positional(df):
    """Test add_alpha(0.7) where numeric is positional."""
    plot = (df >> Plot() >> add_alpha(0.7))
    assert plot.state.alpha_value == 0.7
    assert plot.state.alpha is None
    # Validation should not raise
    plot.state.geom_type = 'point' # Minimal state for validation
    plot.state.validate()

def test_add_size_fixed_positional(df):
    """Test add_size(10) where numeric is positional."""
    plot = (df >> Plot() >> add_size(10))
    assert plot.state.size_value == 10.0
    assert plot.state.size is None
    plot.state.geom_type = 'point'
    plot.state.validate()

def test_state_clearing_alpha(df):
    """Test that setting fixed alpha clears alpha mapping and vice versa."""
    # 1. Start with mapping
    plot = (df >> Plot() >> add_alpha('category'))
    assert plot.state.alpha == 'category'
    assert plot.state.alpha_value is None
    
    # 2. Add fixed value - should clear mapping
    plot = (plot >> add_alpha(0.5))
    assert plot.state.alpha_value == 0.5
    assert plot.state.alpha is None
    
    # 3. Add mapping again - should clear fixed value
    plot = (plot >> add_alpha('category'))
    assert plot.state.alpha == 'category'
    assert plot.state.alpha_value is None

def test_state_clearing_size(df):
    """Test that setting fixed size clears size mapping and vice versa."""
    plot = (df >> Plot() >> add_size('y'))
    assert plot.state.size == 'y'
    assert plot.state.size_value is None
    
    plot = (plot >> add_size(value=20))
    assert plot.state.size_value == 20.0
    assert plot.state.size is None

def test_state_clearing_color(df):
    """Test that setting fixed color clears color mapping and vice versa."""
    plot = (df >> Plot() >> add_color('category'))
    assert plot.state.color == 'category'
    assert plot.state.color_value is None
    
    plot = (plot >> add_color(value='red'))
    assert plot.state.color_value == 'red'
    assert plot.state.color is None
