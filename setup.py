"""
Package setup script for linearmodel.

This script defines the metadata and dependencies required for packaging and distribution
of the linearmodel package using setuptools.

"""

from setuptools import setup, find_packages

setup(
    name='linearmodel',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    package_data={'linearmodel': ['*.csv', '*.py', '*.md']},
    install_requires=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'seaborn',
        'colorama'
    ],
    entry_points={
        'console_scripts': [
            'linearmodel = linearmodel.main:main',
            'linearmodel_main = linearmodel.main:main'
        ]
    },
    author='ABBADI Ahmed',
    author_email='abbadi.ax@gmail.com',
    description='Package for linearmodel',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
)
