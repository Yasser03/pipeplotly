"""
Tests for the core Plot class.
"""
import pytest
import pandas as pd
from pipeplotly import Plot
from pipeplotly.core.state import PlotState


class TestPlotInitialization:
    """Test Plot class initialization."""
    
    def test_plot_with_dataframe(self):
        """Test creating a Plot with a DataFrame."""
        df = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
        plot = Plot(df)
        
        assert plot.state.data is not None
        assert isinstance(plot.state, PlotState)
        assert plot.state.backend == 'plotnine'
    
    def test_plot_without_data(self):
        """Test creating a Plot without data."""
        plot = Plot()
        assert plot.state.data is None
    
    def test_plot_repr(self):
        """Test Plot string representation."""
        df = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
        plot = Plot(df).plot_points('x', 'y')
        repr_str = repr(plot)
        
        assert 'point' in repr_str
        assert 'plotnine' in repr_str


class TestInitializationVerbs:
    """Test initialization verbs (plot_* methods)."""
    
    @pytest.fixture
    def sample_df(self):
        """Create sample DataFrame for testing."""
        return pd.DataFrame({
            'x': range(10),
            'y': [i**2 for i in range(10)],
            'category': ['A', 'B'] * 5
        })
    
    def test_plot_points(self, sample_df):
        """Test plot_points creates scatter plot config."""
        plot = Plot(sample_df).plot_points('x', 'y')
        
        assert plot.state.geom_type == 'point'
        assert plot.state.x == 'x'
        assert plot.state.y == 'y'
    
    def test_plot_lines(self, sample_df):
        """Test plot_lines creates line plot config."""
        plot = Plot(sample_df).plot_lines('x', 'y')
        
        assert plot.state.geom_type == 'line'
        assert plot.state.x == 'x'
        assert plot.state.y == 'y'
    
    def test_plot_bars(self, sample_df):
        """Test plot_bars creates bar chart config."""
        plot = Plot(sample_df).plot_bars('category', 'y')
        
        assert plot.state.geom_type == 'bar'
        assert plot.state.x == 'category'
        assert plot.state.y == 'y'
    
    def test_plot_histogram(self, sample_df):
        """Test plot_histogram creates histogram config."""
        plot = Plot(sample_df).plot_histogram('y', bins=20)
        
        assert plot.state.geom_type == 'histogram'
        assert plot.state.x == 'y'
        assert plot.state.extra_params['bins'] == 20


class TestAestheticVerbs:
    """Test aesthetic verbs (add_* methods)."""
    
    @pytest.fixture
    def base_plot(self):
        """Create base plot for testing."""
        df = pd.DataFrame({
            'x': range(10),
            'y': [i**2 for i in range(10)],
            'category': ['A', 'B'] * 5,
            'size_val': range(10)
        })
        return Plot(df).plot_points('x', 'y')
    
    def test_add_color_by_column(self, base_plot):
        """Test adding color mapped to column."""
        plot = base_plot.add_color('category')
        
        assert plot.state.color == 'category'
    
    def test_add_color_fixed_value(self, base_plot):
        """Test adding fixed color value."""
        plot = base_plot.add_color(value='red')
        
        assert plot.state.color_value == 'red'
    
    def test_add_color_with_palette(self, base_plot):
        """Test adding color with palette."""
        plot = base_plot.add_color('category', palette='viridis')
        
        assert plot.state.color == 'category'
        assert plot.state.color_palette == 'viridis'
    
    def test_add_size(self, base_plot):
        """Test adding size aesthetic."""
        plot = base_plot.add_size('size_val')
        
        assert plot.state.size == 'size_val'
    
    def test_add_facets(self, base_plot):
        """Test adding facets."""
        plot = base_plot.add_facets(cols='category')
        
        assert plot.state.facet_cols == 'category'
    
    def test_add_labels(self, base_plot):
        """Test adding labels."""
        plot = base_plot.add_labels(title='Test Plot', x='X Axis', y='Y Axis')
        
        assert plot.state.title == 'Test Plot'
        assert plot.state.x_label == 'X Axis'
        assert plot.state.y_label == 'Y Axis'


class TestTransformationVerbs:
    """Test transformation verbs (scale_*, coord_*, xlim, ylim)."""
    
    @pytest.fixture
    def base_plot(self):
        """Create base plot for testing."""
        df = pd.DataFrame({'x': range(1, 11), 'y': [i**2 for i in range(1, 11)]})
        return Plot(df).plot_points('x', 'y')
    
    def test_scale_x_log(self, base_plot):
        """Test applying log scale to x-axis."""
        plot = base_plot.scale_x_log()
        
        assert plot.state.x_scale == 'log'
    
    def test_scale_y_log(self, base_plot):
        """Test applying log scale to y-axis."""
        plot = base_plot.scale_y_log()
        
        assert plot.state.y_scale == 'log'
    
    def test_xlim(self, base_plot):
        """Test setting x-axis limits."""
        plot = base_plot.xlim(0, 10)
        
        assert plot.state.x_limits == (0, 10)
    
    def test_ylim(self, base_plot):
        """Test setting y-axis limits."""
        plot = base_plot.ylim(0, 100)
        
        assert plot.state.y_limits == (0, 100)
    
    def test_coord_flip(self, base_plot):
        """Test flipping coordinates."""
        plot = base_plot.coord_flip()
        
        assert plot.state.coord_flip is True
    
    def test_coord_fixed(self, base_plot):
        """Test setting fixed aspect ratio."""
        plot = base_plot.coord_fixed(ratio=1.5)
        
        assert plot.state.coord_fixed == 1.5


class TestThemeVerbs:
    """Test theme-related verbs."""
    
    def test_set_theme(self):
        """Test setting theme."""
        df = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
        plot = Plot(df).plot_points('x', 'y').set_theme('minimal')
        
        assert plot.state.theme == 'minimal'


class TestBackendSwitching:
    """Test switching between backends."""
    
    @pytest.fixture
    def base_plot(self):
        """Create base plot for testing."""
        df = pd.DataFrame({'x': range(10), 'y': range(10)})
        return Plot(df).plot_points('x', 'y')
    
    def test_default_backend_is_plotnine(self, base_plot):
        """Test that default backend is plotnine."""
        assert base_plot.state.backend == 'plotnine'
    
    def test_to_interactive(self, base_plot):
        """Test converting to interactive (Plotly)."""
        plot = base_plot.to_interactive()
        
        assert plot.state.backend == 'plotly'
    
    def test_to_static(self, base_plot):
        """Test converting to static (plotnine)."""
        plot = base_plot.to_interactive().to_static()
        
        assert plot.state.backend == 'plotnine'


class TestMethodChaining:
    """Test method chaining functionality."""
    
    def test_full_chain(self):
        """Test a complete method chain."""
        df = pd.DataFrame({
            'x': range(10),
            'y': [i**2 for i in range(10)],
            'category': ['A', 'B'] * 5
        })
        
        plot = (Plot(df)
            .plot_points('x', 'y')
            .add_color('category')
            .add_labels(title='Test', x='X', y='Y')
            .set_theme('minimal')
            .xlim(0, 10)
            .ylim(0, 100))
        
        assert plot.state.geom_type == 'point'
        assert plot.state.color == 'category'
        assert plot.state.title == 'Test'
        assert plot.state.theme == 'minimal'
        assert plot.state.x_limits == (0, 10)
        assert plot.state.y_limits == (0, 100)
    
    def test_each_verb_returns_plot(self):
        """Test that each verb returns a Plot instance."""
        df = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
        plot = Plot(df)
        
        assert isinstance(plot.plot_points('x', 'y'), Plot)
        assert isinstance(plot.plot_points('x', 'y').add_color(value='red'), Plot)
        assert isinstance(plot.plot_points('x', 'y').set_theme('minimal'), Plot)


class TestStateValidation:
    """Test state validation."""
    
    def test_validate_missing_data(self):
        """Test validation fails with missing data."""
        plot = Plot()
        
        with pytest.raises(ValueError, match="data cannot be None"):
            plot.state.validate()
    
    def test_validate_missing_geom_type(self):
        """Test validation fails with missing geometry type."""
        df = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
        plot = Plot(df)
        
        with pytest.raises(ValueError, match="geometry type must be specified"):
            plot.state.validate()
    
    def test_validate_missing_column(self):
        """Test validation fails with non-existent column."""
        df = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
        plot = Plot(df).plot_points('x', 'nonexistent')
        
        with pytest.raises(ValueError, match="not found in data"):
            plot.state.validate()
    
    def test_validate_success(self):
        """Test validation succeeds with valid state."""
        df = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
        plot = Plot(df).plot_points('x', 'y')
        
        # Should not raise
        plot.state.validate()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
