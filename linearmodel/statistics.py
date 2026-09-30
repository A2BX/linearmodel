"""
Module Name: statistics

This module provides functions for descriptive statistics and correlation analysis.

"""

import numpy as np

def descriptive_statistics(data):
    """
    Compute descriptive statistics for the given data.

    Args:
    - data: numpy array, pandas DataFrame...

    Returns:
    - dict: Dictionary containing descriptive statistics
    """
    statistics = {
        "mean": np.mean(data),
        "median": np.median(data),
        "standard_deviation": np.std(data).apply(lambda x: '    ' + str(x)),
        "min": np.min(data),
        "max": np.max(data),
        "variance": np.var(data),
        "quartiles": np.percentile(data, [25, 50, 75]),
        "coefficient_of_variation": np.std(data) / np.mean(data)
    }
    return statistics

def correlation_analysis(data):
    """
    Compute correlation matrix for the given data.

    Args:
    - data: numpy array, pandas DataFrame...

    Returns:
    - numpy array: Correlation matrix
    """
    correlation_matrix = np.corrcoef(data, rowvar=False)
    return correlation_matrix
