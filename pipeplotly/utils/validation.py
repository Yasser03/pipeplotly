"""Utility functions for data validation."""
import pandas as pd
from typing import List, Optional


def validate_dataframe(df: pd.DataFrame, required_columns: Optional[List[str]] = None) -> None:
    """
    Validate a DataFrame for use in plots.
    
    Args:
        df: DataFrame to validate
        required_columns: List of required column names
        
    Raises:
        TypeError: If df is not a DataFrame
        ValueError: If required columns are missing
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"Expected pandas DataFrame, got {type(df)}")
    
    if df.empty:
        raise ValueError("DataFrame is empty")
    
    if required_columns:
        missing = set(required_columns) - set(df.columns)
        if missing:
            raise ValueError(f"Required columns missing from DataFrame: {missing}")


def validate_column(df: pd.DataFrame, column: str, column_type: str = "column") -> None:
    """
    Validate that a column exists in a DataFrame.
    
    Args:
        df: DataFrame to check
        column: Column name
        column_type: Description of column type for error messages
        
    Raises:
        ValueError: If column doesn't exist
    """
    if column and column not in df.columns:
        available = ', '.join(df.columns.tolist()[:5])
        if len(df.columns) > 5:
            available += f', ... ({len(df.columns)} total)'
        raise ValueError(
            f"{column_type} '{column}' not found in DataFrame. "
            f"Available columns: {available}"
        )


def validate_numeric_column(df: pd.DataFrame, column: str) -> None:
    """
    Validate that a column is numeric.
    
    Args:
        df: DataFrame to check
        column: Column name
        
    Raises:
        ValueError: If column is not numeric
    """
    validate_column(df, column)
    if not pd.api.types.is_numeric_dtype(df[column]):
        raise ValueError(f"Column '{column}' must be numeric")
