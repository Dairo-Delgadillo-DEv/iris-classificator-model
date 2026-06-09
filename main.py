"""
Pipeline principal de entrenamiento y evaluación del modelo MLOps
Dataset: Iris Flower Classification
Modelo: Random Forest Classifier

Ejecución:
    python main.py
"""

import logging
import yaml
from pathlib import Path
from src.utils.logger import setup_logging
from src.data.load_data import load_iris_data, split_data, scale_data, save_scaler
from src.models.train import ModelTrainer


def load_config(config_path='config/config.yaml'):
    """
    Carga la configuración desde el archivo YAML
    
    Args:
        config_path (str): Ruta al archivo de configuración
        
    Returns:
        dict: Configuración cargada
        
    Raises:
        FileNotFoundError: Si el archivo no existe
    """
    if not Path(config_path).exists():
        raise FileNotFoundError(f"Archivo de config no encontrado: {config_path}")
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config


def main():
    """
    Función principal del pipeline
    
    Pasos:
    1. Cargar datos
    2. Dividir en train/test
    3. Normalizar features
    4. Entrenar modelo
    5. Evaluar modelo
    6. Guardar modelo y scaler
    7. Mostrar resultados
    """
    
    # Configurar logging
    logger = setup_logging()
    logger.info("=" * 70)
    logger.info("INICIANDO PIPELINE MLOPS - IRIS CLASSIFICATION")
    logger.info("=" * 70)
    
    try:
        # Cargar configuración
        logger.info("\n[PASO 0] Cargando configuración...")
        config = load_config()
        logger.info(f"Proyecto: {config['project_name']}")
        logger.info(f"Versión: {config['model_version']}")
        
        # 1. CARGAR DATOS
        logger.info("\n[PASO 1] Cargando datos del dataset Iris...")
        X, y, feature_names, target_names = load_iris_data()
        logger.info(f"✓ Dataset cargado")
        logger.info(f"  - Total de muestras: {X.shape[0]}")
        logger.info(f"  - Features: {X.shape[1]}")
        logger.info(f"  - Clases: {len(target_names)} ({', '.join(target_names)})")
        
        # 2. DIVIDIR DATOS
        logger.info("\n[PASO 2] Dividiendo datos en train/test...")
        test_size = config['data']['test_size']
        X_train, X_test, y_train, y_test = split_data(X, y, test_size=test_size)
        logger.info(f"✓ Datos divididos")
        logger.info(f"  - Train set: {X_train.shape[0]} muestras ({(1-test_size)*100:.0f}%)")
        logger.info(f"  - Test set: {X_test.shape[0]} muestras ({test_size*100:.0f}%)")
        
        # 3. NORMALIZAR DATOS
        logger.info("\n[PASO 3] Normalizando features con StandardScaler...")
        X_train_scaled, X_test_scaled, scaler = scale_data(X_train, X_test)
        logger.info(f"✓ Features normalizadas")
        
        # 4. ENTRENAR MODELO
        logger.info("\n[PASO 4] Entrenando modelo Random Forest...")
        model_params = config['model']['hyperparameters']
        trainer = ModelTrainer(
            n_estimators=model_params['n_estimators'],
            max_depth=model_params['max_depth'],
            random_state=model_params['random_state']
        )
        trainer.train(X_train_scaled, y_train)
        logger.info(f"✓ Modelo entrenado exitosamente")
        
        # 5. EVALUAR MODELO
        logger.info("\n[PASO 5] Evaluando modelo en test set...")
        metrics = trainer.evaluate(X_test_scaled, y_test, target_names=target_names)
        logger.info(f"✓ Modelo evaluado")
        
        # 6. GUARDAR MODELO Y SCALER
        logger.info("\n[PASO 6] Guardando modelo y scaler...")
        Path('models').mkdir(exist_ok=True)
        model_path = 'models/iris_model.joblib'
        scaler_path = 'models/iris_scaler.joblib'
        
        trainer.save_model(model_path)
        save_scaler(scaler, scaler_path)
        
        # Guardar métricas
        metrics_path = 'models/metrics.json'
        trainer.save_metrics(metrics_path)
        logger.info(f"✓ Archivos guardados")
        logger.info(f"  - Modelo: {model_path}")
        logger.info(f"  - Scaler: {scaler_path}")
        logger.info(f"  - Métricas: {metrics_path}")
        
        # 7. RESUMEN FINAL
        logger.info("\n" + "=" * 70)
        logger.info("RESUMEN DEL ENTRENAMIENTO")
        logger.info("=" * 70)
        logger.info(f"Accuracy:  {metrics['accuracy']:.4f} ({metrics['accuracy']*100:.2f}%)")
        logger.info(f"Precision: {metrics['precision']:.4f}")
        logger.info(f"Recall:    {metrics['recall']:.4f}")
        logger.info(f"F1-Score:  {metrics['f1_score']:.4f}")
        logger.info("=" * 70)
        
        # Verificar si cumple el objetivo
        target_accuracy = config['model']['target_metrics']['accuracy']
        if metrics['accuracy'] >= target_accuracy:
            logger.info(f"\n✓ ÉXITO: Accuracy ({metrics['accuracy']:.4f}) >= "
                       f"Target ({target_accuracy:.4f})")
        else:
            logger.warning(f"\n⚠ ADVERTENCIA: Accuracy ({metrics['accuracy']:.4f}) < "
                          f"Target ({target_accuracy:.4f})")
        
        logger.info("\n" + "=" * 70)
        logger.info("PIPELINE COMPLETADO EXITOSAMENTE")
        logger.info("=" * 70 + "\n")
        
        return trainer, metrics, scaler
    
    except Exception as e:
        logger.error(f"ERROR en el pipeline: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    trainer, metrics, scaler = main()

