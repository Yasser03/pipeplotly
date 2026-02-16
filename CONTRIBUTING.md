# Contributing to PipePlotly

Thank you for your interest in contributing to PipePlotly! This document provides guidelines and instructions for contributing.

## 🌟 Ways to Contribute

- **Report bugs** - Found an issue? Let us know!
- **Suggest features** - Have an idea? We'd love to hear it!
- **Improve documentation** - Help make our docs clearer
- **Submit code** - Fix bugs or implement new features
- **Write tests** - Improve test coverage
- **Share examples** - Create tutorial notebooks

## 🚀 Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/Yasser03/pipeplotly.git
cd pipeplotly
```

### 2. Set Up Development Environment

```bash
# Create a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate
# Unix/MacOS
source venv/bin/activate

# Install in editable mode with dev dependencies
pip install -e .[dev]
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

## 📝 Development Guidelines

### Code Style

We follow PEP 8 with some modifications:

- Line length: 88 characters (Black default)
- Use type hints for all function parameters and return values
- Write docstrings for all public functions and classes

**Format code with Black:**

```bash
black pipeplotly/
```

**Lint with Ruff:**

```bash
ruff check pipeplotly/
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files as `test_*.py`
- Use descriptive test names: `test_plot_points_creates_scatter_plot`
- Aim for >80% code coverage

**Run tests:**

```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/test_plot.py -v

# With coverage
pip install pytest-cov
pytest tests/ -v --cov=pipeplotly --cov-report=html
```

### Documentation

- Update README.md for user-facing changes
- Add docstrings following Google style
- Include examples in docstrings
- Update type hints

**Example docstring:**

```python
def add_color(self, column: Optional[str] = None, 
              value: Optional[str] = None) -> 'Plot':
    """
    Map a column to color or set a fixed color.
    
    Args:
        column: Column name to map to color
        value: Fixed color value (if not mapping to data)
        
    Returns:
        New Plot instance with color aesthetic added
        
    Examples:
        >>> plot.add_color('species')  # Map to column
        >>> plot.add_color(value='red')  # Fixed color
    """
```

## 🧪 Testing Checklist

Before submitting a PR, ensure:

- [ ] All existing tests pass
- [ ] New features have tests
- [ ] Code is formatted with Black
- [ ] No linting errors from Ruff
- [ ] Documentation is updated
- [ ] Examples work correctly

## 📤 Submitting Changes

1. **Commit your changes**

   ```bash
   git add .
   git commit -m "feat: add support for contour plots"
   ```

   Use conventional commit messages:
   - `feat:` New feature
   - `fix:` Bug fix
   - `docs:` Documentation changes
   - `test:` Test additions/changes
   - `refactor:` Code refactoring
   - `style:` Code style changes

2. **Push to your fork**

   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create a Pull Request**

   - Go to the original repository on GitHub
   - Click "New Pull Request"
   - Select your fork and branch
   - Fill in the PR template
   - Link any related issues

## 🏗️ Architecture Overview

### Core Components

- **`core/plot.py`**: Main Plot class with all verb methods
- **`core/state.py`**: PlotState dataclass for configuration
- **`backends/`**: Backend implementations (plotnine, Plotly)
- **`utils/`**: Utility functions
- **`themes/`**: Theme and palette definitions

### Adding a New Plot Type

1. Add verb method to `Plot` class:

   ```python
   def plot_contour(self, x: str, y: str, z: str, **kwargs) -> 'Plot':
       """Create a contour plot."""
       return self._copy(geom_type='contour', x=x, y=y, color=z, **kwargs)
   ```

2. Implement in backends:

   ```python
   # plotnine_backend.py
   elif geom_type == 'contour':
       return p9.geom_contour(aes_mapping, **geom_params)
   
   # plotly_backend.py
   elif geom_type == 'contour':
       fig = px.density_contour(**params)
   ```

3. Add tests:

   ```python
   def test_plot_contour(self, sample_df):
       """Test plot_contour creates contour plot config."""
       plot = Plot(sample_df).plot_contour('x', 'y', 'z')
       assert plot.state.geom_type == 'contour'
   ```

## 🐛 Reporting Bugs

**Before submitting:**
- Check if the issue already exists
- Try the latest version
- Provide a minimal reproducible example

**Bug report should include:**
- PipePlotly version
- Python version
- Operating system
- Minimal code to reproduce
- Expected vs actual behavior
- Error messages/tracebacks

## 💡 Suggesting Features

Feature requests are welcome! Please include:
- Clear use case
- Example of desired API
- Why it would benefit users
- Any alternatives you've considered

## 📦 Release Process

(For maintainers)

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Create git tag: `git tag v0.2.0`
4. Push tag: `git push origin v0.2.0`
5. Build distribution: `python -m build`
6. Upload to PyPI: `twine upload dist/*`

## 💬 Questions?

- Open a GitHub issue
- Start a discussion in Discussions tab
- Reach out to maintainers

## 📜 Code of Conduct

Be respectful and professional. We're all here to learn and build something great together!

## 🙏 Thank You!

Your contributions make PipePlotly better for everyone. We appreciate your time and effort!
