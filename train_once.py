"""
Script para entrenar el modelo una sola vez
Útil para testing o demostración rápida

Uso:
    python train_once.py
"""

import logging
from pathlib import Path
from src.utils.logger import setup_logging
from src.data.load_data import load_iris_data, split_data, scale_data, save_scaler
from src.models.train import ModelTrainer


def train_once():
    """
    Entrena el modelo una vez con los hiperparámetros por defecto
    Guarda modelo y scaler
    """
    logger = setup_logging()
    
    logger.info("\n" + "="*70)
    logger.info("ENTRENAMIENTO RÁPIDO DEL MODELO")
    logger.info("="*70)
    
    try:
        # Cargar datos
        logger.info("\n1. Cargando datos...")
        X, y, feature_names, target_names = load_iris_data()
        logger.info(f"   ✓ {X.shape[0]} muestras, {X.shape[1]} features")
        
        # Dividir datos
        logger.info("\n2. Dividiendo datos...")
        X_train, X_test, y_train, y_test = split_data(X, y)
        logger.info(f"   ✓ Train: {X_train.shape[0]}, Test: {X_test.shape[0]}")
        
        # Normalizar
        logger.info("\n3. Normalizando datos...")
        X_train_scaled, X_test_scaled, scaler = scale_data(X_train, X_test)
        logger.info(f"   ✓ Datos normalizados")
        
        # Entrenar
        logger.info("\n4. Entrenando modelo...")
        trainer = ModelTrainer(n_estimators=100, max_depth=10)
        trainer.train(X_train_scaled, y_train)
        logger.info(f"   ✓ Modelo entrenado")
        
        # Evaluar
        logger.info("\n5. Evaluando modelo...")
        metrics = trainer.evaluate(X_test_scaled, y_test, target_names)
        logger.info(f"   ✓ Accuracy: {metrics['accuracy']:.4f}")
        
        # Guardar
        logger.info("\n6. Guardando archivos...")
        Path('models').mkdir(exist_ok=True)
        
        model_path = 'models/iris_model.joblib'
        scaler_path = 'models/iris_scaler.joblib'
        
        trainer.save_model(model_path)
        save_scaler(scaler, scaler_path)
        
        logger.info(f"   ✓ Modelo guardado en {model_path}")
        logger.info(f"   ✓ Scaler guardado en {scaler_path}")
        
        logger.info("\n" + "="*70)
        logger.info("✓ ENTRENAMIENTO COMPLETADO")
        logger.info("="*70)
        
        logger.info(f"\nAhora puedes ejecutar la API:")
        logger.info(f"  uvicorn deployment.api.app:app --reload")
        logger.info(f"\nOTRON terminal, prueba la API:")
        logger.info(f"  python test_api.py\n")
    
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    train_once()
