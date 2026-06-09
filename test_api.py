"""
Script para probar la API REST

Uso:
    # 1. Iniciar la API en otra terminal
    uvicorn deployment.api.app:app --reload --host 0.0.0.0 --port 5000
    
    # 2. En otra terminal, ejecutar este script
    python test_api.py
"""

import logging
import time
from src.utils.logger import setup_logging
from src.api_client import APIClient

logger = setup_logging()


def test_api():
    """Prueba los endpoints de la API"""
    
    logger.info("\n" + "="*70)
    logger.info("PRUEBAS DE API REST")
    logger.info("="*70)
    
    # Esperar a que la API esté lista
    logger.info("\nEsperando a que la API esté lista...")
    max_retries = 5
    retry_count = 0
    
    client = None
    while retry_count < max_retries:
        try:
            client = APIClient()
            health = client.health_check()
            if health['status'] == 'healthy':
                logger.info("✓ API está lista")
                break
            else:
                logger.warning(f"⚠ API no completamente sana: {health['status']}")
        except Exception as e:
            retry_count += 1
            if retry_count < max_retries:
                logger.info(f"Reintentando... ({retry_count}/{max_retries})")
                time.sleep(2)
            else:
                logger.error(f"No se pudo conectar a la API después de {max_retries} intentos")
                return
    
    if client is None:
        return
    
    try:
        # Test 1: Health check
        logger.info("\n[TEST 1] Health Check")
        logger.info("-" * 70)
        health = client.health_check()
        logger.info(f"✓ Status: {health['status']}")
        logger.info(f"✓ Model loaded: {health['model_loaded']}")
        logger.info(f"✓ API Version: {health['version']}")
        
        # Test 2: Model info
        logger.info("\n[TEST 2] Model Info")
        logger.info("-" * 70)
        info = client.get_model_info()
        logger.info(f"✓ Algorithm: {info['algorithm']}")
        logger.info(f"✓ Accuracy: {info['accuracy']:.4f}")
        logger.info(f"✓ Classes: {', '.join(info['classes'])}")
        logger.info(f"✓ Hyperparameters:")
        for key, val in info['hyperparameters'].items():
            logger.info(f"  - {key}: {val}")
        
        # Test 3: Single prediction
        logger.info("\n[TEST 3] Single Prediction")
        logger.info("-" * 70)
        pred = client.predict(
            sepal_length=5.1,
            sepal_width=3.5,
            petal_length=1.4,
            petal_width=0.2
        )
        logger.info(f"✓ Input: [5.1, 3.5, 1.4, 0.2]")
        logger.info(f"✓ Prediction: {pred['prediction']}")
        logger.info(f"✓ Confidence: {pred['confidence']:.2%}")
        logger.info(f"✓ Probabilities:")
        for species, prob in pred['probabilities'].items():
            logger.info(f"  - {species}: {prob:.2%}")
        
        # Test 4: Batch prediction
        logger.info("\n[TEST 4] Batch Prediction")
        logger.info("-" * 70)
        samples = [
            [5.1, 3.5, 1.4, 0.2],
            [7.0, 3.2, 4.7, 1.4],
            [6.3, 3.3, 6.0, 2.5],
        ]
        batch_pred = client.predict_batch(samples)
        logger.info(f"✓ Predictions made: {batch_pred['count']}")
        for i, pred in enumerate(batch_pred['predictions']):
            logger.info(f"  Sample {i+1}: {pred['prediction']} "
                       f"(confidence: {pred['confidence']:.2%})")
        
        # Test 5: Version
        logger.info("\n[TEST 5] API Version")
        logger.info("-" * 70)
        version = client.get_version()
        logger.info(f"✓ API Version: {version['api_version']}")
        logger.info(f"✓ Model Version: {version['model_version']}")
        
        logger.info("\n" + "="*70)
        logger.info("✓ TODOS LOS TESTS EXITOSOS")
        logger.info("="*70 + "\n")
    
    except Exception as e:
        logger.error(f"Error durante tests: {str(e)}", exc_info=True)
    
    finally:
        if client:
            client.close()


if __name__ == "__main__":
    test_api()
