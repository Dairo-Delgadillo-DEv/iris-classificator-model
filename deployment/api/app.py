"""
API REST con FastAPI para el modelo Iris

Ejecución local:
    uvicorn deployment.api.app:app --reload --host 0.0.0.0 --port 5000

En producción con Gunicorn:
    gunicorn deployment.api.wsgi:app --bind 0.0.0.0:5000 --workers 4

Documentación interactiva:
    http://localhost:5000/docs (Swagger UI)
    http://localhost:5000/redoc (ReDoc)
"""

import logging
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from src.services import PredictionService
from src.schemas import (
    IrisPredictionRequest, BatchPredictionRequest,
    PredictionResponse, BatchPredictionResponse,
    ModelInfo, HealthResponse, ErrorResponse
)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Instancia global del servicio
prediction_service: PredictionService = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manejador de lifecycle de la aplicación
    Se ejecuta al iniciar y detener
    """
    # Startup
    logger.info("Iniciando aplicación...")
    global prediction_service
    prediction_service = PredictionService()
    
    if prediction_service.load_model():
        logger.info("✓ Modelo cargado exitosamente")
    else:
        logger.warning("⚠ No se pudo cargar el modelo")
    
    yield
    
    # Shutdown
    logger.info("Cerrando aplicación...")


# Crear aplicación FastAPI
app = FastAPI(
    title="Iris Flower Classification API",
    description="API para predicción de especies de flores Iris usando Random Forest",
    version="1.0.0",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción especificar dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# ENDPOINTS
# ============================================================================

@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["Health"],
    summary="Health Check",
    description="Verifica que la API esté activa y el modelo cargado"
)
async def health_check():
    """
    Endpoint para verificar el estado de la API
    
    Returns:
        HealthResponse: Estado de la API
    """
    try:
        is_healthy = prediction_service.is_healthy()
        
        return HealthResponse(
            status="healthy" if is_healthy else "degraded",
            model_loaded=is_healthy,
            version="1.0.0"
        )
    except Exception as e:
        logger.error(f"Error en health check: {str(e)}")
        return HealthResponse(
            status="unhealthy",
            model_loaded=False,
            version="1.0.0"
        )


@app.post(
    "/predict",
    response_model=PredictionResponse,
    tags=["Predictions"],
    summary="Predicción Individual",
    description="Realiza una predicción para una flor individual"
)
async def predict(request: IrisPredictionRequest):
    """
    Realiza una predicción individual
    
    Args:
        request (IrisPredictionRequest): Características de la flor
        
    Returns:
        PredictionResponse: Predicción con confianza y probabilidades
        
    Example:
        ```json
        {
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2
        }
        ```
    """
    try:
        if not prediction_service.is_healthy():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Modelo no está cargado"
            )
        
        response = prediction_service.predict_single(request)
        
        logger.info(f"Predicción: {response.prediction}, "
                   f"Confianza: {response.confidence:.2%}")
        
        return response
    
    except ValidationError as e:
        logger.error(f"Error de validación: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Datos de entrada inválidos"
        )
    except Exception as e:
        logger.error(f"Error en predicción: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en predicción: {str(e)}"
        )


@app.post(
    "/predict/batch",
    response_model=BatchPredictionResponse,
    tags=["Predictions"],
    summary="Predicciones en Batch",
    description="Realiza predicciones para múltiples flores"
)
async def predict_batch(request: BatchPredictionRequest):
    """
    Realiza predicciones en batch
    
    Args:
        request (BatchPredictionRequest): Lista de características
        
    Returns:
        BatchPredictionResponse: Lista de predicciones
        
    Example:
        ```json
        {
            "samples": [
                [5.1, 3.5, 1.4, 0.2],
                [7.0, 3.2, 4.7, 1.4],
                [6.3, 3.3, 6.0, 2.5]
            ]
        }
        ```
    """
    try:
        if not prediction_service.is_healthy():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Modelo no está cargado"
            )
        
        if not request.samples:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="samples no puede estar vacío"
            )
        
        if len(request.samples) > 1000:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Máximo 1000 muestras por request"
            )
        
        responses = prediction_service.predict_batch(request.samples)
        
        logger.info(f"Predicción en batch: {len(responses)} muestras")
        
        return BatchPredictionResponse(
            predictions=responses,
            count=len(responses)
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en predicción en batch: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en predicción: {str(e)}"
        )


@app.get(
    "/model/info",
    tags=["Model"],
    summary="Información del Modelo",
    description="Retorna información sobre el modelo cargado"
)
async def model_info():
    """
    Retorna información del modelo
    
    Returns:
        dict: Información del modelo
    """
    try:
        if not prediction_service.is_healthy():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Modelo no está cargado"
            )
        
        info = prediction_service.get_model_info()
        
        return {
            "name": "Iris Flower Classifier",
            "version": "1.0.0",
            "algorithm": info['algorithm'],
            "accuracy": info['metrics']['accuracy'] if info['metrics'] else None,
            "n_features": 4,
            "classes": info['classes'],
            "hyperparameters": info['hyperparameters']
        }
    
    except Exception as e:
        logger.error(f"Error al obtener info del modelo: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener información del modelo"
        )


@app.get(
    "/version",
    tags=["Info"],
    summary="Versión de la API",
    description="Retorna la versión de la API"
)
async def get_version():
    """Retorna la versión de la API"""
    return {
        "api_version": "1.0.0",
        "model_version": "1.0.0"
    }


# ============================================================================
# MANEJO DE ERRORES
# ============================================================================

@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    """Maneja errores de validación"""
    logger.error(f"Error de validación: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "detail": str(exc),
            "status_code": 422
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Maneja excepciones generales"""
    logger.error(f"Error no manejado: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "detail": "Ocurrió un error interno",
            "status_code": 500
        }
    )


# ============================================================================
# ENDPOINT ROOT
# ============================================================================

@app.get(
    "/",
    tags=["Info"],
    summary="Root",
    description="Información sobre la API"
)
async def root():
    """
    Root endpoint
    Redirige a documentación
    """
    return {
        "name": "Iris Flower Classification API",
        "version": "1.0.0",
        "description": "API para predicción de flores Iris",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "predict_batch": "/predict/batch",
            "model_info": "/model/info"
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Iniciando servidor FastAPI...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=5000,
        log_level="info"
    )
