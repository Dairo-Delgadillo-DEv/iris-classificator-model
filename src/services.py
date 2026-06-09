"""
Servicios de predicción y lógica de negocio
"""
import numpy as np
import logging
from pathlib import Path
from typing import List, Tuple
from src.models.train import ModelTrainer
from src.data.load_data import load_scaler
from src.schemas import IrisPredictionRequest, PredictionResponse, SpeciesEnum

logger = logging.getLogger(__name__)


class PredictionService:
    """
    Servicio centralizado de predicciones
    Maneja la lógica de carga de modelos y escalers
    """
    
    def __init__(self, model_path: str = 'models/iris_model.joblib', 
                 scaler_path: str = 'models/iris_scaler.joblib'):
        """
        Inicializa el servicio de predicción
        
        Args:
            model_path (str): Ruta al modelo entrenado
            scaler_path (str): Ruta al scaler
        """
        self.model_path = model_path
        self.scaler_path = scaler_path
        self.trainer = None
        self.scaler = None
        self.target_names = ['setosa', 'versicolor', 'virginica']
        
        logger.info(f"Inicializando PredictionService")
        logger.info(f"  - Model path: {model_path}")
        logger.info(f"  - Scaler path: {scaler_path}")
    
    def load_model(self) -> bool:
        """
        Carga el modelo y el scaler
        
        Returns:
            bool: True si se cargó exitosamente
        """
        try:
            logger.info("Cargando modelo...")
            if not Path(self.model_path).exists():
                logger.error(f"Modelo no encontrado: {self.model_path}")
                return False
            
            self.trainer = ModelTrainer()
            self.trainer.load_model(self.model_path)
            
            logger.info("Cargando scaler...")
            if not Path(self.scaler_path).exists():
                logger.warning(f"Scaler no encontrado: {self.scaler_path}")
                return False
            
            self.scaler = load_scaler(self.scaler_path)
            
            logger.info("Modelo y scaler cargados exitosamente")
            return True
        
        except Exception as e:
            logger.error(f"Error al cargar modelo: {str(e)}")
            return False
    
    def predict_single(self, request: IrisPredictionRequest) -> PredictionResponse:
        """
        Realiza una predicción individual
        
        Args:
            request (IrisPredictionRequest): Datos de entrada
            
        Returns:
            PredictionResponse: Predicción con confianza y probabilidades
            
        Raises:
            RuntimeError: Si el modelo no está cargado
        """
        if self.trainer is None or self.scaler is None:
            raise RuntimeError("Modelo no está cargado. Llama a load_model() primero")
        
        # Convertir a array
        X = np.array(request.to_array()).reshape(1, -1)
        
        # Normalizar
        X_scaled = self.scaler.transform(X)
        
        # Predicción
        prediction_id = self.trainer.predict(X_scaled)[0]
        probabilities = self.trainer.predict_proba(X_scaled)[0]
        
        # Confianza
        confidence = float(probabilities[prediction_id])
        
        # Crear respuesta
        prob_dict = {
            name: float(prob)
            for name, prob in zip(self.target_names, probabilities)
        }
        
        logger.info(f"Predicción: {self.target_names[prediction_id]}, "
                   f"Confianza: {confidence:.2%}")
        
        return PredictionResponse(
            prediction=SpeciesEnum(self.target_names[prediction_id]),
            prediction_id=int(prediction_id),
            confidence=confidence,
            probabilities=prob_dict
        )
    
    def predict_batch(self, samples: List[List[float]]) -> List[PredictionResponse]:
        """
        Realiza predicciones en batch
        
        Args:
            samples (List[List[float]]): Lista de características
            
        Returns:
            List[PredictionResponse]: Lista de predicciones
            
        Raises:
            RuntimeError: Si el modelo no está cargado
            ValueError: Si los datos no tienen la forma correcta
        """
        if self.trainer is None or self.scaler is None:
            raise RuntimeError("Modelo no está cargado")
        
        if not samples:
            raise ValueError("samples no puede estar vacío")
        
        samples = np.array(samples)
        
        if samples.ndim != 2 or samples.shape[1] != 4:
            raise ValueError("Cada muestra debe tener 4 características")
        
        # Normalizar
        X_scaled = self.scaler.transform(samples)
        
        # Predicciones
        predictions_ids = self.trainer.predict(X_scaled)
        probabilities = self.trainer.predict_proba(X_scaled)
        
        # Crear respuestas
        responses = []
        for i, (pred_id, probs) in enumerate(zip(predictions_ids, probabilities)):
            confidence = float(probs[pred_id])
            prob_dict = {
                name: float(prob)
                for name, prob in zip(self.target_names, probs)
            }
            
            response = PredictionResponse(
                prediction=SpeciesEnum(self.target_names[pred_id]),
                prediction_id=int(pred_id),
                confidence=confidence,
                probabilities=prob_dict
            )
            responses.append(response)
        
        logger.info(f"Predicciones en batch: {len(responses)} muestras procesadas")
        return responses
    
    def get_model_info(self) -> dict:
        """
        Retorna información del modelo
        
        Returns:
            dict: Información del modelo cargado
        """
        if self.trainer is None:
            return {'status': 'no_loaded'}
        
        return {
            'algorithm': 'RandomForestClassifier',
            'hyperparameters': self.trainer.hyperparameters,
            'is_trained': self.trainer.is_trained,
            'classes': self.target_names,
            'metrics': self.trainer.metrics if self.trainer.metrics else None
        }
    
    def is_healthy(self) -> bool:
        """
        Verifica si el servicio está sano (modelo y scaler cargados)
        
        Returns:
            bool: True si está listo para predicciones
        """
        return self.trainer is not None and self.scaler is not None
