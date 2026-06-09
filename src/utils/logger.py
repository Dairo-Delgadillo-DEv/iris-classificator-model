"""
Configuración del logging para el proyecto
"""
import logging
import os
from datetime import datetime


def setup_logging(log_level=logging.INFO, log_file="logs/training.log"):
    """
    Configura el logging del proyecto
    
    Args:
        log_level: Nivel de logging
        log_file: Ruta del archivo de log
    """
    # Crear directorio de logs si no existe
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    # Crear logger principal
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # Formato del log
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Handler para archivo
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    
    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    
    # Agregar handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger
