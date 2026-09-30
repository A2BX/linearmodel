"""
Module Name: visualisation

This module provides functions for visualizing data using matplotlib and seaborn.

"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def histogram(data, xlabel='', ylabel='', title=''):
    """
    Generate a histogram for the given data.

    Args:
    - data: array-like, input data
    - xlabel: string, label for x-axis (optional)
    - ylabel: string, label for y-axis (optional)
    - title: string, title of the plot (optional)
    """
    plt.hist(data, bins='auto')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()

def boxplot(data, xlabel='', ylabel='', title=''):
    """
    Generate a box plot for the given data.

    Args:
    - data: array-like, input data
    - xlabel: string, label for x-axis (optional)
    - ylabel: string, label for y-axis (optional)
    - title: string, title of the plot (optional)
    """
    sns.boxplot(data)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()

def correlation_matrix(data):
    """
    Generate a correlation matrix heatmap for the given data.

    Args:
    - data: DataFrame, input data
    """
    sns.heatmap(data.corr(), annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Matrix')
    plt.show()

def bar_plot(data, xlabel='', ylabel='', title='', sample_size=None, bins=None):
    """
    Create a bar plot for categorical data.

    Parameters:
        data (pd.Series): The categorical data to be plotted.
        xlabel (str): Label for the x-axis.
        ylabel (str): Label for the y-axis.
        title (str): Title of the plot.
        sample_size (int): Optional. If specified, plot a random sample of the data with the given size.
        bins (int or list-like): Optional. If specified, group data into the given number of bins or defined bins.

    Returns:
        None
    """
    if sample_size:
        data = data.sample(sample_size)
    if bins:
        # Cut the data into specified bins
        data = pd.cut(data, bins=bins)
            
    value_counts = data.value_counts()
    value_counts = value_counts.sort_index()
    plt.figure(figsize=(10, 6))
    plt.bar(value_counts.index.astype(str), value_counts.values)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def density_plot(data, xlabel='', ylabel='', title='', sample_size=None):
    """
    Generate a density plot for the given data.

    Args:
    - data: array-like, input data
    - xlabel: string, label for x-axis (optional)
    - ylabel: string, label for y-axis (optional)
    - title: string, title of the plot (optional)
    - sample_size: int, number of samples to use (optional)
    """
    if sample_size:
        data = data.sample(n=sample_size, random_state=42)
    sns.kdeplot(data, shade=True)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()

def heatmap(data, xlabel='', ylabel='', title='', sample_size=None):
    """
    Generate a heatmap plot for the given data.

    Args:
    - data: 2D array-like, input data
    - xlabel: string, label for x-axis (optional)
    - ylabel: string, label for y-axis (optional)
    - title: string, title of the plot (optional)
    - sample_size: int, number of samples to use (optional)
    """
    if sample_size:
        data = data.sample(n=sample_size, random_state=42)
    sns.heatmap(data.corr(), annot=True, cmap='viridis')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()
