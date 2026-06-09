"""
Modelos Pydantic para validación de datos en la API
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class SpeciesEnum(str, Enum):
    """Enum de especies de flores Iris"""
    SETOSA = "setosa"
    VERSICOLOR = "versicolor"
    VIRGINICA = "virginica"


class IrisPredictionRequest(BaseModel):
    """
    Modelo de entrada para predicción
    
    Ejemplo:
    {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }
    """
    sepal_length: float = Field(..., ge=0, le=10, description="Largo del sépalo en cm")
    sepal_width: float = Field(..., ge=0, le=10, description="Ancho del sépalo en cm")
    petal_length: float = Field(..., ge=0, le=10, description="Largo del pétalo en cm")
    petal_width: float = Field(..., ge=0, le=10, description="Ancho del pétalo en cm")
    
    class Config:
        schema_extra = {
            "example": {
                "sepal_length": 5.1,
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2
            }
        }
    
    def to_array(self) -> List[float]:
        """Convierte a array para el modelo"""
        return [
            self.sepal_length,
            self.sepal_width,
            self.petal_length,
            self.petal_width
        ]


class BatchPredictionRequest(BaseModel):
    """
    Modelo para predicciones en batch
    
    Ejemplo:
    {
        "samples": [
            [5.1, 3.5, 1.4, 0.2],
            [7.0, 3.2, 4.7, 1.4]
        ]
    }
    """
    samples: List[List[float]] = Field(..., description="Lista de características")


class PredictionResponse(BaseModel):
    """
    Modelo de respuesta de predicción individual
    
    Ejemplo:
    {
        "prediction": "setosa",
        "prediction_id": 0,
        "confidence": 0.95,
        "probabilities": {
            "setosa": 0.95,
            "versicolor": 0.04,
            "virginica": 0.01
        }
    }
    """
    prediction: SpeciesEnum = Field(..., description="Especie predicha")
    prediction_id: int = Field(..., description="ID numérico de la predicción")
    confidence: float = Field(..., ge=0, le=1, description="Confianza de la predicción")
    probabilities: dict = Field(..., description="Probabilidades por clase")


class BatchPredictionResponse(BaseModel):
    """
    Modelo de respuesta de predicciones en batch
    """
    predictions: List[PredictionResponse] = Field(..., description="Lista de predicciones")
    count: int = Field(..., description="Número de predicciones")


class ModelInfo(BaseModel):
    """
    Información del modelo
    """
    name: str = Field(..., description="Nombre del modelo")
    version: str = Field(..., description="Versión del modelo")
    algorithm: str = Field(..., description="Algoritmo usado")
    accuracy: float = Field(..., description="Accuracy en test set")
    n_features: int = Field(..., description="Número de features")
    classes: List[str] = Field(..., description="Clases del modelo")
    hyperparameters: dict = Field(..., description="Hiperparámetros")


class HealthResponse(BaseModel):
    """Respuesta de health check"""
    status: str = Field(..., description="Estado de la API")
    model_loaded: bool = Field(..., description="¿Modelo cargado?")
    version: str = Field(..., description="Versión de la API")


class ErrorResponse(BaseModel):
    """Modelo de respuesta de error"""
    error: str = Field(..., description="Mensaje de error")
    detail: Optional[str] = Field(None, description="Detalles adicionales")
    status_code: int = Field(..., description="Código HTTP de error")
