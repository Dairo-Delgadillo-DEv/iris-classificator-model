"""
Ejemplo de predicción con el modelo entrenado
Muestra cómo usar el modelo para hacer predicciones

Ejecución:
    python predict_example.py
"""

import logging
import numpy as np
from src.utils.logger import setup_logging
from src.services import PredictionService
from src.data.load_data import load_iris_data, split_data, scale_data
from src.schemas import IrisPredictionRequest


def example_single_prediction():
    """
    Ejemplo 1: Predicción individual
    """
    logger = logging.getLogger(__name__)
    logger.info("\n" + "="*60)
    logger.info("EJEMPLO 1: PREDICCIÓN INDIVIDUAL")
    logger.info("="*60)
    
    # Cargar servicio
    service = PredictionService()
    if not service.load_model():
        logger.error("No se pudo cargar el modelo")
        return
    
    # Crear una predicción
    request = IrisPredictionRequest(
        sepal_length=5.1,
        sepal_width=3.5,
        petal_length=1.4,
        petal_width=0.2
    )
    
    logger.info(f"Entrada: {request}")
    
    # Realizar predicción
    response = service.predict_single(request)
    
    logger.info(f"\n✓ Predicción realizada:")
    logger.info(f"  - Especie: {response.prediction}")
    logger.info(f"  - ID: {response.prediction_id}")
    logger.info(f"  - Confianza: {response.confidence:.2%}")
    logger.info(f"  - Probabilidades:")
    for species, prob in response.probabilities.items():
        logger.info(f"    • {species}: {prob:.2%}")


def example_batch_prediction():
    """
    Ejemplo 2: Predicción en batch
    """
    logger = logging.getLogger(__name__)
    logger.info("\n" + "="*60)
    logger.info("EJEMPLO 2: PREDICCIÓN EN BATCH")
    logger.info("="*60)
    
    # Cargar servicio
    service = PredictionService()
    if not service.load_model():
        logger.error("No se pudo cargar el modelo")
        return
    
    # Múltiples predicciones
    samples = [
        [5.1, 3.5, 1.4, 0.2],  # Setosa
        [7.0, 3.2, 4.7, 1.4],  # Versicolor
        [6.3, 3.3, 6.0, 2.5],  # Virginica
    ]
    
    logger.info(f"Realizando predicciones para {len(samples)} muestras...")
    
    responses = service.predict_batch(samples)
    
    for i, response in enumerate(responses):
        logger.info(f"\n  Muestra {i+1}:")
        logger.info(f"    - Predicción: {response.prediction}")
        logger.info(f"    - Confianza: {response.confidence:.2%}")


def example_test_set_predictions():
    """
    Ejemplo 3: Predicciones en test set
    Compara predicciones con valores reales
    """
    logger = logging.getLogger(__name__)
    logger.info("\n" + "="*60)
    logger.info("EJEMPLO 3: PREDICCIONES EN TEST SET")
    logger.info("="*60)
    
    # Cargar datos
    X, y, feature_names, target_names = load_iris_data()
    X_train, X_test, y_train, y_test = split_data(X, y)
    X_train_scaled, X_test_scaled, scaler = scale_data(X_train, X_test)
    
    # Cargar servicio
    service = PredictionService()
    if not service.load_model():
        logger.error("No se pudo cargar el modelo")
        return
    
    # Predicciones en primeras 5 muestras
    logger.info(f"\nPredicciones en primeras 5 muestras del test set:")
    
    correct = 0
    for i in range(min(5, len(X_test_scaled))):
        # Predicción
        response = service.predict_batch([X_test_scaled[i].tolist()])[0]
        real = target_names[y_test[i]]
        predicted = str(response.prediction)
        is_correct = (predicted == real)
        
        if is_correct:
            correct += 1
        
        status = "✓" if is_correct else "✗"
        logger.info(f"\n  {status} Muestra {i+1}:")
        logger.info(f"    - Real: {real}")
        logger.info(f"    - Predicción: {predicted}")
        logger.info(f"    - Confianza: {response.confidence:.2%}")
    
    logger.info(f"\nAciertos: {correct}/5 ({correct*100//5}%)")


def example_model_info():
    """
    Ejemplo 4: Información del modelo
    """
    logger = logging.getLogger(__name__)
    logger.info("\n" + "="*60)
    logger.info("EJEMPLO 4: INFORMACIÓN DEL MODELO")
    logger.info("="*60)
    
    # Cargar servicio
    service = PredictionService()
    if not service.load_model():
        logger.error("No se pudo cargar el modelo")
        return
    
    info = service.get_model_info()
    
    logger.info(f"\n✓ Información del modelo:")
    logger.info(f"  - Algoritmo: {info['algorithm']}")
    logger.info(f"  - Clases: {', '.join(info['classes'])}")
    logger.info(f"  - Hiperparámetros:")
    for key, value in info['hyperparameters'].items():
        logger.info(f"    • {key}: {value}")
    
    if info['metrics']:
        logger.info(f"  - Métricas:")
        logger.info(f"    • Accuracy: {info['metrics']['accuracy']:.4f}")
        logger.info(f"    • Precision: {info['metrics']['precision']:.4f}")
        logger.info(f"    • Recall: {info['metrics']['recall']:.4f}")
        logger.info(f"    • F1-Score: {info['metrics']['f1_score']:.4f}")


def main():
    """
    Ejecuta todos los ejemplos de predicción
    """
    logger = setup_logging()
    
    logger.info("\n" + "="*60)
    logger.info("EJEMPLOS DE PREDICCIÓN CON EL MODELO IRIS")
    logger.info("="*60)
    
    try:
        # Ejecutar ejemplos
        example_single_prediction()
        example_batch_prediction()
        example_test_set_predictions()
        example_model_info()
        
        logger.info("\n" + "="*60)
        logger.info("✓ TODOS LOS EJEMPLOS COMPLETADOS")
        logger.info("="*60 + "\n")
    
    except Exception as e:
        logger.error(f"Error en ejemplos: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
