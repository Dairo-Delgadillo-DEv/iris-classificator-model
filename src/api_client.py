"""
Cliente HTTP para la API REST
Permite probar la API sin usar curl o Postman

Uso:
    from src.api_client import APIClient
    
    client = APIClient("http://localhost:5000")
    response = client.predict(sepal_length=5.1, sepal_width=3.5, ...)
"""

import requests
import logging
from typing import Dict, List, Optional
from src.schemas import IrisPredictionRequest

logger = logging.getLogger(__name__)


class APIClient:
    """Cliente HTTP para comunicarse con la API FastAPI"""
    
    def __init__(self, base_url: str = "http://localhost:5000", timeout: int = 10):
        """
        Inicializa el cliente
        
        Args:
            base_url (str): URL base de la API
            timeout (int): Timeout en segundos
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        
        logger.info(f"Inicializando APIClient")
        logger.info(f"  - Base URL: {self.base_url}")
        logger.info(f"  - Timeout: {timeout}s")
    
    def health_check(self) -> Dict:
        """
        Realiza un health check
        
        Returns:
            dict: Respuesta del servidor
        """
        try:
            response = self.session.get(
                f"{self.base_url}/health",
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error en health check: {str(e)}")
            raise
    
    def predict(self, sepal_length: float, sepal_width: float,
                petal_length: float, petal_width: float) -> Dict:
        """
        Realiza una predicción individual
        
        Args:
            sepal_length (float): Largo del sépalo
            sepal_width (float): Ancho del sépalo
            petal_length (float): Largo del pétalo
            petal_width (float): Ancho del pétalo
            
        Returns:
            dict: Respuesta con predicción
        """
        payload = {
            "sepal_length": sepal_length,
            "sepal_width": sepal_width,
            "petal_length": petal_length,
            "petal_width": petal_width
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/predict",
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error en predicción: {str(e)}")
            raise
    
    def predict_batch(self, samples: List[List[float]]) -> Dict:
        """
        Realiza predicciones en batch
        
        Args:
            samples (List[List[float]]): Lista de características
            
        Returns:
            dict: Respuesta con predicciones
        """
        payload = {"samples": samples}
        
        try:
            response = self.session.post(
                f"{self.base_url}/predict/batch",
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error en predicción en batch: {str(e)}")
            raise
    
    def get_model_info(self) -> Dict:
        """
        Obtiene información del modelo
        
        Returns:
            dict: Información del modelo
        """
        try:
            response = self.session.get(
                f"{self.base_url}/model/info",
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al obtener info del modelo: {str(e)}")
            raise
    
    def get_version(self) -> Dict:
        """
        Obtiene versión de la API
        
        Returns:
            dict: Versión de la API
        """
        try:
            response = self.session.get(
                f"{self.base_url}/version",
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al obtener versión: {str(e)}")
            raise
    
    def close(self):
        """Cierra la sesión HTTP"""
        self.session.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
