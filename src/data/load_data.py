"""
Módulo para cargar y preparar datos del dataset Iris
"""
import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def load_iris_data():
    """
    Carga el dataset Iris de sklearn
    
    Returns:
        X (np.array): Features (150, 4)
        y (np.array): Target (150,)
        feature_names (list): Nombres de las features
        target_names (list): Nombres de las clases
    """
    logger.info("Cargando dataset Iris...")
    iris = load_iris()
    X = iris.data
    y = iris.target
    feature_names = iris.feature_names
    target_names = iris.target_names
    
    logger.info(f"Dataset cargado. Shape: {X.shape}")
    logger.info(f"Features: {feature_names}")
    logger.info(f"Clases: {target_names}")
    
    # Verificar integridad
    assert X.shape == (150, 4), "Shape incorrecto"
    assert y.shape == (150,), "Shape incorrecto"
    
    return X, y, feature_names, target_names


def load_iris_dataframe():
    """
    Carga el dataset Iris como DataFrame de pandas
    
    Returns:
        df (pd.DataFrame): DataFrame con todas las features
        target_names (list): Nombres de las clases
    """
    logger.info("Cargando dataset Iris como DataFrame...")
    iris = load_iris()
    df = pd.DataFrame(iris.data, columns=iris.feature_names)
    df['target'] = iris.target
    df['target_name'] = df['target'].map(dict(enumerate(iris.target_names)))
    
    logger.info(f"DataFrame cargado. Shape: {df.shape}")
    return df, iris.target_names


def split_data(X, y, test_size=0.2, random_state=42):
    """
    Divide los datos en train y test
    
    Args:
        X (np.array): Features
        y (np.array): Target
        test_size (float): Porcentaje de test (default 0.2)
        random_state (int): Seed para reproducibilidad
        
    Returns:
        tuple: (X_train, X_test, y_train, y_test)
        
    Raises:
        ValueError: Si test_size no está entre 0 y 1
    """
    if not 0 < test_size < 1:
        raise ValueError("test_size debe estar entre 0 y 1")
    
    logger.info(f"Dividiendo datos: test_size={test_size}, random_state={random_state}")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    logger.info(f"Train size: {X_train.shape[0]}, Test size: {X_test.shape[0]}")
    logger.info(f"Distribución train: {np.bincount(y_train)}")
    logger.info(f"Distribución test: {np.bincount(y_test)}")
    
    return X_train, X_test, y_train, y_test


def scale_data(X_train, X_test):
    """
    Normaliza los datos usando StandardScaler
    
    Aplica StandardScaler (media=0, SD=1) a los datos.
    Primero fit en train, luego transform en test.
    
    Args:
        X_train (np.array): Features de entrenamiento
        X_test (np.array): Features de test
        
    Returns:
        tuple: (X_train_scaled, X_test_scaled, scaler)
        
    Raises:
        ValueError: Si los datos no tienen la forma correcta
    """
    if X_train.ndim != 2 or X_test.ndim != 2:
        raise ValueError("X_train y X_test deben ser 2D")
    
    if X_train.shape[1] != X_test.shape[1]:
        raise ValueError("X_train y X_test deben tener el mismo número de features")
    
    logger.info("Normalizando datos con StandardScaler...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    logger.info(f"Train - Media: {X_train_scaled.mean(axis=0)}, SD: {X_train_scaled.std(axis=0)}")
    logger.info("Datos normalizados correctamente")
    
    return X_train_scaled, X_test_scaled, scaler


def save_scaler(scaler, filepath: str):
    """
    Guarda el scaler para usar en producción
    
    Args:
        scaler (StandardScaler): Scaler entrenado
        filepath (str): Ruta donde guardar
    """
    import joblib
    logger.info(f"Guardando scaler en {filepath}")
    joblib.dump(scaler, filepath)
    logger.info("Scaler guardado exitosamente")


def load_scaler(filepath: str):
    """
    Carga un scaler previamente guardado
    
    Args:
        filepath (str): Ruta del scaler
        
    Returns:
        StandardScaler: Scaler cargado
    """
    import joblib
    logger.info(f"Cargando scaler desde {filepath}")
    scaler = joblib.load(filepath)
    logger.info("Scaler cargado exitosamente")
    return scaler
