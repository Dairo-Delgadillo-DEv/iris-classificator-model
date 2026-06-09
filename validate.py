"""
Script para validar que todo funcione correctamente

Uso:
    python validate.py
"""

import logging
from pathlib import Path
from src.utils.logger import setup_logging
from src.data.load_data import load_iris_data, load_scaler
from src.models.train import ModelTrainer
from src.services import PredictionService
from src.schemas import IrisPredictionRequest

logger = setup_logging()


def validate_all():
    """Valida todos los componentes del proyecto"""
    
    logger.info("\n" + "="*70)
    logger.info("VALIDACIÓN DEL PROYECTO")
    logger.info("="*70)
    
    checks_passed = 0
    checks_total = 0
    
    # 1. Datos
    logger.info("\n[CHECK 1] Datos Iris")
    checks_total += 1
    try:
        X, y, feature_names, target_names = load_iris_data()
        assert X.shape == (150, 4)
        assert y.shape == (150,)
        logger.info("✓ Dataset Iris correcto")
        checks_passed += 1
    except Exception as e:
        logger.error(f"✗ Error en datos: {str(e)}")
    
    # 2. Modelo archivo
    logger.info("\n[CHECK 2] Archivo del modelo")
    checks_total += 1
    try:
        model_path = Path('models/iris_model.joblib')
        if model_path.exists():
            logger.info(f"✓ Modelo encontrado ({model_path.stat().st_size} bytes)")
            checks_passed += 1
        else:
            logger.warning(f"⚠ Modelo no encontrado en {model_path}")
            logger.info("  Ejecuta primero: python main.py o python train_once.py")
    except Exception as e:
        logger.error(f"✗ Error: {str(e)}")
    
    # 3. Scaler archivo
    logger.info("\n[CHECK 3] Archivo del scaler")
    checks_total += 1
    try:
        scaler_path = Path('models/iris_scaler.joblib')
        if scaler_path.exists():
            logger.info(f"✓ Scaler encontrado ({scaler_path.stat().st_size} bytes)")
            checks_passed += 1
        else:
            logger.warning(f"⚠ Scaler no encontrado")
            logger.info("  Ejecuta primero: python main.py o python train_once.py")
    except Exception as e:
        logger.error(f"✗ Error: {str(e)}")
    
    # 4. Cargar modelo
    logger.info("\n[CHECK 4] Cargar modelo")
    checks_total += 1
    try:
        trainer = ModelTrainer()
        if Path('models/iris_model.joblib').exists():
            trainer.load_model('models/iris_model.joblib')
            logger.info("✓ Modelo cargado correctamente")
            checks_passed += 1
        else:
            logger.warning("⚠ Saltar check - modelo no existe")
    except Exception as e:
        logger.error(f"✗ Error: {str(e)}")
    
    # 5. Cargar scaler
    logger.info("\n[CHECK 5] Cargar scaler")
    checks_total += 1
    try:
        if Path('models/iris_scaler.joblib').exists():
            scaler = load_scaler('models/iris_scaler.joblib')
            logger.info("✓ Scaler cargado correctamente")
            checks_passed += 1
        else:
            logger.warning("⚠ Saltar check - scaler no existe")
    except Exception as e:
        logger.error(f"✗ Error: {str(e)}")
    
    # 6. Servicio de predicción
    logger.info("\n[CHECK 6] Servicio de predicción")
    checks_total += 1
    try:
        service = PredictionService()
        if service.load_model():
            logger.info("✓ Servicio cargado correctamente")
            checks_passed += 1
        else:
            logger.warning("⚠ Servicio no pudo cargar modelo")
    except Exception as e:
        logger.error(f"✗ Error: {str(e)}")
    
    # 7. Hacer predicción
    logger.info("\n[CHECK 7] Predicción de prueba")
    checks_total += 1
    try:
        service = PredictionService()
        if service.load_model():
            request = IrisPredictionRequest(
                sepal_length=5.1,
                sepal_width=3.5,
                petal_length=1.4,
                petal_width=0.2
            )
            response = service.predict_single(request)
            logger.info(f"✓ Predicción exitosa: {response.prediction}")
            checks_passed += 1
        else:
            logger.warning("⚠ Saltar check - modelo no cargado")
    except Exception as e:
        logger.error(f"✗ Error: {str(e)}")
    
    # 8. Esquemas Pydantic
    logger.info("\n[CHECK 8] Esquemas Pydantic")
    checks_total += 1
    try:
        req = IrisPredictionRequest(
            sepal_length=5.1,
            sepal_width=3.5,
            petal_length=1.4,
            petal_width=0.2
        )
        assert len(req.to_array()) == 4
        logger.info("✓ Esquemas validados")
        checks_passed += 1
    except Exception as e:
        logger.error(f"✗ Error: {str(e)}")
    
    # Resumen
    logger.info("\n" + "="*70)
    logger.info(f"RESULTADO: {checks_passed}/{checks_total} checks pasados")
    logger.info("="*70)
    
    if checks_passed == checks_total:
        logger.info("\n✓ ¡TODO FUNCIONA CORRECTAMENTE!")
        logger.info("\nPróximos pasos:")
        logger.info("1. Ejecutar la API:")
        logger.info("   uvicorn deployment.api.app:app --reload")
        logger.info("\n2. En otra terminal, probar la API:")
        logger.info("   python test_api.py")
    else:
        logger.warning(f"\n⚠ Algunos checks fallaron")
        logger.info("\nPasos para completar setup:")
        logger.info("1. python main.py (o python train_once.py)")
        logger.info("2. python validate.py")
        logger.info("3. python test_api.py")
    
    logger.info("\n")
    return checks_passed == checks_total


if __name__ == "__main__":
    success = validate_all()
    exit(0 if success else 1)
