"""
Module Name: ordinary_least_squares

This module provides a class for Ordinary Least Squares (OLS) regression model.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t


class OrdinaryLeastSquares:
    """
    Ordinary Least Squares (OLS) regression model.

    This class implements the Ordinary Least Squares regression model for linear regression.
    """

    def __init__(self, intercept=True):
        """
        Initialize the OLS regression model.

        Args:
        - intercept (bool): Indicates whether to include an intercept term in the regression model.
        """
        self.intercept = intercept
        self.coefficients = None

    def fit(self, X, y):
        """
        Fit the regression model to the given training data.

        Args:
        - X: array-like, shape (n_samples, n_features), Training data
        - y: array-like, shape (n_samples,), Target values
        """
        if self.intercept:
            X = np.column_stack((np.ones(len(X)), X))
        self.coefficients = np.linalg.inv(X.T.dot(X)).dot(X.T).dot(y)

    def predict(self, X_test):
        """
        Predict the target variable for the given test data.

        Args:
        - X_test: array-like, shape (n_samples, n_features), Test data

        Returns:
        - array-like, Predicted target values
        """
        if self.intercept:
            X_test = np.column_stack((np.ones(len(X_test)), X_test))
        return X_test.dot(self.coefficients)

    def get_coefficients(self):
        """
        Get the coefficients of the fitted regression model.

        Returns:
        - array-like, Coefficients of the regression model.
        """
        return self.coefficients

    def determination_coefficient(self, X, y):
        """
        Calculate the coefficient of determination (R-squared) for the fitted model.

        Args:
        - X: array-like, shape (n_samples, n_features), Input data
        - y: array-like, shape (n_samples,), Target values

        Returns:
        - float, Coefficient of determination (R-squared)
        """
        y_pred = self.predict(X)
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r_squared = 1 - (ss_res / ss_tot)
        return r_squared

    def confidence_intervals(self, X, y, alpha=0.05):
        """
        Calculate confidence intervals for the coefficients of the fitted model.

        Args:
        - X: array-like, shape (n_samples, n_features), Input data
        - y: array-like, shape (n_samples,), Target values
        - alpha: float, significance level for confidence intervals (default: 0.05)

        Returns:
        - array-like, shape (n_features, 2), Confidence intervals for the coefficients
        """
        if self.intercept:
            X = np.column_stack((np.ones(len(X)), X))

        n, p = X.shape
        dof = n - p  # degrees of freedom
        t_critical = t.ppf(1 - alpha / 2, dof)

        coefficients = self.coefficients
        std_errors = np.sqrt(np.sum((y - X.dot(coefficients)) ** 2) / dof)
    
        # Calculate denominator avoiding division by zero
        denom = np.sqrt(np.sum((X - X.mean(axis=0)) ** 2, axis=0))
        denom[denom == 0] = 1  # Replace zero with 1 to avoid division by zero
        ci_half_width = t_critical * std_errors / denom

        ci_lower = coefficients - ci_half_width
        ci_upper = coefficients + ci_half_width

        return np.column_stack((ci_lower, ci_upper))
    
    def plot_residuals(self, X, y):
        """
        Plot residuals (difference between observed and predicted values) against predicted values.

        Args:
        - X: array-like, shape (n_samples, n_features), Input data
        - y: array-like, shape (n_samples,), Target values
        """
        y_pred = self.predict(X)
        residuals = y - y_pred
        plt.scatter(y_pred, residuals)
        plt.axhline(y=0, color='r', linestyle='--')
        plt.xlabel("Predicted Values")
        plt.ylabel("Residuals")
        plt.title("Residual Plot")
        plt.show()

    def plot_qq_plot(self, X, y):
        """
        Plot a Q-Q plot to check the normality assumption of residuals.

        Args:
        - X: array-like, shape (n_samples, n_features), Input data
        - y: array-like, shape (n_samples,), Target values
        """
        y_pred = self.predict(X)
        residuals = y - y_pred

        # Sort residuals
        sorted_residuals = np.sort(residuals)

        # Calculate quantiles for normal distribution
        quantiles = np.random.normal(loc=0, scale=np.std(residuals), size=len(residuals))
        sorted_quantiles = np.sort(quantiles)

        # Plot Q-Q plot
        plt.scatter(sorted_quantiles, sorted_residuals)
        plt.xlabel("Theoretical Quantiles")
        plt.ylabel("Sample Quantiles")
        plt.title("Q-Q Plot")
        plt.show()
