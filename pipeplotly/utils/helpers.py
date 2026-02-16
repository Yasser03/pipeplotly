"""Helper utility functions."""
from typing import Any, Dict


def merge_dicts(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge multiple dictionaries, with later dicts taking precedence.
    
    Args:
        *dicts: Dictionaries to merge
        
    Returns:
        Merged dictionary
    """
    result = {}
    for d in dicts:
        if d:
            result.update(d)
    return result


def clean_none_values(d: Dict[str, Any]) -> Dict[str, Any]:
    """
    Remove None values from a dictionary.
    
    Args:
        d: Dictionary to clean
        
    Returns:
        Dictionary with None values removed
    """
    return {k: v for k, v in d.items() if v is not None}
