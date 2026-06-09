"""
Configuración de la aplicación FastAPI

Variables de entorno:
    FLASK_ENV: development, staging, production
    MODEL_PATH: Ruta al modelo entrenado
    SCALER_PATH: Ruta al scaler
    LOG_LEVEL: DEBUG, INFO, WARNING, ERROR
    MAX_BATCH_SIZE: Máximo tamaño de batch
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Rutas
BASE_DIR = Path(__file__).parent.parent.parent
MODELS_DIR = BASE_DIR / 'models'

# Configuración de la API
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
DEBUG = FLASK_ENV == 'development'
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Modelo
MODEL_PATH = os.getenv('MODEL_PATH', str(MODELS_DIR / 'iris_model.joblib'))
SCALER_PATH = os.getenv('SCALER_PATH', str(MODELS_DIR / 'iris_scaler.joblib'))

# API
API_HOST = os.getenv('API_HOST', '0.0.0.0')
API_PORT = int(os.getenv('API_PORT', 5000))
MAX_BATCH_SIZE = int(os.getenv('MAX_BATCH_SIZE', 1000))

# CORS
CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')

# Logging
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': LOG_LEVEL,
            'formatter': 'default'
        }
    },
    'root': {
        'level': LOG_LEVEL,
        'handlers': ['console']
    }
}

# Settings
class Settings:
    """Configuración de la aplicación"""
    
    app_name: str = "Iris Flower Classification API"
    app_version: str = "1.0.0"
    debug: bool = DEBUG
    
    # Model
    model_path: str = MODEL_PATH
    scaler_path: str = SCALER_PATH
    
    # API
    api_host: str = API_HOST
    api_port: int = API_PORT
    max_batch_size: int = MAX_BATCH_SIZE
    
    # Logging
    log_level: str = LOG_LEVEL
    
    # Validation
    sepal_length_min: float = 4.0
    sepal_length_max: float = 8.0
    sepal_width_min: float = 2.0
    sepal_width_max: float = 4.5
    petal_length_min: float = 1.0
    petal_length_max: float = 7.0
    petal_width_min: float = 0.1
    petal_width_max: float = 2.5


settings = Settings()

# Verificar que el modelo existe
if not Path(settings.model_path).exists():
    print(f"⚠ WARNING: Modelo no encontrado en {settings.model_path}")
    print(f"  Asegúrate de ejecutar main.py primero")
