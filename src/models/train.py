"""
Módulo para entrenar el modelo Random Forest
"""
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score,
    roc_curve, auc
)
import joblib
import logging
import json
from pathlib import Path
from typing import Dict, Tuple
import numpy as np

logger = logging.getLogger(__name__)


class ModelTrainer:
    """
    Clase para entrenar y evaluar el modelo Random Forest
    """
    
    def __init__(self, n_estimators=100, max_depth=10, random_state=42, n_jobs=-1):
        """
        Inicializa el entrenador del modelo
        
        Args:
            n_estimators (int): Número de árboles en el bosque (default 100)
            max_depth (int): Profundidad máxima de los árboles (default 10)
            random_state (int): Seed para reproducibilidad (default 42)
            n_jobs (int): Número de jobs paralelos (default -1 = todos)
        """
        logger.info(f"Inicializando Random Forest")
        logger.info(f"  - n_estimators: {n_estimators}")
        logger.info(f"  - max_depth: {max_depth}")
        logger.info(f"  - random_state: {random_state}")
        
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=random_state,
            n_jobs=n_jobs
        )
        self.metrics = {}
        self.hyperparameters = {
            'n_estimators': n_estimators,
            'max_depth': max_depth,
            'random_state': random_state
        }
        self.is_trained = False
        
    def train(self, X_train, y_train):
        """
        Entrena el modelo con los datos de entrenamiento
        
        Args:
            X_train (np.array): Features de entrenamiento (n_samples, n_features)
            y_train (np.array): Target de entrenamiento (n_samples,)
            
        Raises:
            ValueError: Si los datos no tienen la forma correcta
        """
        if X_train.ndim != 2:
            raise ValueError("X_train debe ser 2D")
        if y_train.ndim != 1:
            raise ValueError("y_train debe ser 1D")
        if X_train.shape[0] != y_train.shape[0]:
            raise ValueError("X_train e y_train deben tener el mismo número de muestras")
        
        logger.info("Iniciando entrenamiento del modelo...")
        logger.info(f"  - X_train shape: {X_train.shape}")
        logger.info(f"  - y_train shape: {y_train.shape}")
        logger.info(f"  - Clases: {np.unique(y_train)}")
        
        self.model.fit(X_train, y_train)
        self.is_trained = True
        
        logger.info("Modelo entrenado exitosamente")
        logger.info(f"Feature importance: {self.get_feature_importance()}")
        
    def evaluate(self, X_test, y_test, target_names=None) -> Dict:
        """
        Evalúa el modelo en el conjunto de test
        
        Args:
            X_test (np.array): Features de test
            y_test (np.array): Target de test
            target_names (list): Nombres de las clases (opcional)
            
        Returns:
            dict: Métricas del modelo
            
        Raises:
            RuntimeError: Si el modelo no ha sido entrenado
        """
        if not self.is_trained:
            raise RuntimeError("El modelo debe ser entrenado antes de evaluar")
        
        logger.info("Evaluando modelo en test set...")
        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)
        
        # Calcular métricas
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        
        # Confusion matrix y classification report
        cm = confusion_matrix(y_test, y_pred)
        class_report = classification_report(y_test, y_pred, target_names=target_names, output_dict=True)
        
        self.metrics = {
            'accuracy': float(accuracy),
            'precision': float(precision),
            'recall': float(recall),
            'f1_score': float(f1),
            'confusion_matrix': cm.tolist(),
            'classification_report': class_report,
            'y_pred': y_pred.tolist(),
            'y_pred_proba': y_pred_proba.tolist(),
            'y_test': y_test.tolist() if isinstance(y_test, np.ndarray) else y_test
        }
        
        # Log de resultados
        logger.info(f"\n{'='*50}")
        logger.info("MÉTRICAS DE EVALUACIÓN")
        logger.info(f"{'='*50}")
        logger.info(f"Accuracy:  {accuracy:.4f}")
        logger.info(f"Precision: {precision:.4f}")
        logger.info(f"Recall:    {recall:.4f}")
        logger.info(f"F1-Score:  {f1:.4f}")
        logger.info(f"\nConfusion Matrix:\n{cm}")
        logger.info(f"\nClassification Report:\n{classification_report(y_test, y_pred, target_names=target_names)}")
        
        return self.metrics
    
    def predict(self, X):
        """
        Realiza predicciones
        
        Args:
            X (np.array): Features para predicción
            
        Returns:
            np.array: Predicciones (índices de clases)
            
        Raises:
            RuntimeError: Si el modelo no ha sido entrenado
        """
        if not self.is_trained:
            raise RuntimeError("El modelo debe ser entrenado antes de hacer predicciones")
        
        return self.model.predict(X)
    
    def predict_proba(self, X) -> np.ndarray:
        """
        Realiza predicciones con probabilidades
        
        Args:
            X (np.array): Features para predicción
            
        Returns:
            np.ndarray: Probabilidades de cada clase (n_samples, n_classes)
            
        Raises:
            RuntimeError: Si el modelo no ha sido entrenado
        """
        if not self.is_trained:
            raise RuntimeError("El modelo debe ser entrenado antes de hacer predicciones")
        
        return self.model.predict_proba(X)
    
    def get_feature_importance(self) -> Dict[str, float]:
        """
        Retorna la importancia de cada feature
        
        Returns:
            dict: Importancia de features
        """
        if not self.is_trained:
            return {}
        
        feature_importance = self.model.feature_importances_
        return feature_importance.tolist()
    
    def save_model(self, filepath: str):
        """
        Guarda el modelo entrenado
        
        Args:
            filepath (str): Ruta donde guardar el modelo
            
        Raises:
            RuntimeError: Si el modelo no ha sido entrenado
        """
        if not self.is_trained:
            raise RuntimeError("No hay modelo entrenado para guardar")
        
        logger.info(f"Guardando modelo en {filepath}")
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.model, filepath)
        logger.info("Modelo guardado exitosamente")
        
    def load_model(self, filepath: str):
        """
        Carga un modelo previamente entrenado
        
        Args:
            filepath (str): Ruta del modelo a cargar
            
        Raises:
            FileNotFoundError: Si el archivo no existe
        """
        logger.info(f"Cargando modelo desde {filepath}")
        if not Path(filepath).exists():
            raise FileNotFoundError(f"Modelo no encontrado en {filepath}")
        
        self.model = joblib.load(filepath)
        self.is_trained = True
        logger.info("Modelo cargado exitosamente")
        
    def save_metrics(self, filepath: str):
        """
        Guarda las métricas en formato JSON
        
        Args:
            filepath (str): Ruta donde guardar métricas
        """
        if not self.metrics:
            logger.warning("No hay métricas para guardar")
            return
        
        logger.info(f"Guardando métricas en {filepath}")
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(self.metrics, f, indent=2)
        
        logger.info("Métricas guardadas exitosamente")
    
    def get_model_info(self) -> Dict:
        """
        Retorna información del modelo
        
        Returns:
            dict: Información del modelo
        """
        return {
            'algorithm': 'RandomForestClassifier',
            'hyperparameters': self.hyperparameters,
            'is_trained': self.is_trained,
            'metrics': self.metrics if self.metrics else None
        }
