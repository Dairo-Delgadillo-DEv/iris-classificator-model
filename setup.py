"""
Setup.py para empaquetar el proyecto
"""
from setuptools import setup, find_packages

setup(
    name='iris-mlops',
    version='1.0.0',
    description='MLOps project for Iris Flower Classification',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.24.0',
        'pandas>=2.0.0',
        'scikit-learn>=1.3.0',
        'pyyaml>=6.0',
        'joblib>=1.3.0',
    ],
    python_requires='>=3.8',
)
