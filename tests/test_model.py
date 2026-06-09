"""
Tests unitarios para el modelo y servicios

Ejecución:
    pytest tests/
    pytest tests/test_model.py -v
    pytest tests/test_model.py::test_model_accuracy -v
"""

import pytest
import numpy as np
from pathlib import Path

from src.data.load_data import load_iris_data, split_data, scale_data
from src.models.train import ModelTrainer
from src.services import PredictionService
from src.schemas import IrisPredictionRequest


# ============================================================================
# TESTS DE CARGA DE DATOS
# ============================================================================

class TestLoadData:
    """Tests para carga de datos"""
    
    def test_load_iris_data_shape(self):
        """Verifica que el dataset tenga la forma correcta"""
        X, y, feature_names, target_names = load_iris_data()
        
        assert X.shape == (150, 4), "X debe tener shape (150, 4)"
        assert y.shape == (150,), "y debe tener shape (150,)"
        assert len(feature_names) == 4, "Debe haber 4 features"
        assert len(target_names) == 3, "Debe haber 3 clases"
    
    def test_load_iris_data_values(self):
        """Verifica que los valores sean razonables"""
        X, y, _, _ = load_iris_data()
        
        assert X.min() >= 0, "No debe haber valores negativos"
        assert y.min() == 0, "Clases deben empezar en 0"
        assert y.max() == 2, "Máxima clase debe ser 2"
        assert np.all(np.isin(y, [0, 1, 2])), "Solo debe haber clases 0, 1, 2"
    
    def test_split_data_sizes(self):
        """Verifica que el split sea correcto"""
        X, y, _, _ = load_iris_data()
        X_train, X_test, y_train, y_test = split_data(X, y, test_size=0.2)
        
        assert X_train.shape[0] == 120, "Train debe tener 120 muestras"
        assert X_test.shape[0] == 30, "Test debe tener 30 muestras"
        assert y_train.shape[0] == 120
        assert y_test.shape[0] == 30
    
    def test_split_data_stratification(self):
        """Verifica que el split mantenga la distribución"""
        X, y, _, _ = load_iris_data()
        X_train, X_test, y_train, y_test = split_data(X, y, test_size=0.2)
        
        # Verificar que hay muestras de todas las clases
        assert len(np.unique(y_train)) == 3, "Train debe tener todas las clases"
        assert len(np.unique(y_test)) == 3, "Test debe tener todas las clases"
    
    def test_scale_data_normalization(self):
        """Verifica que el scaling normalice correctamente"""
        X, y, _, _ = load_iris_data()
        X_train, X_test, y_train, y_test = split_data(X, y)
        X_train_scaled, X_test_scaled, _ = scale_data(X_train, X_test)
        
        # Media debe ser ~0, std debe ser ~1
        assert np.allclose(X_train_scaled.mean(axis=0), 0, atol=0.01)
        assert np.allclose(X_train_scaled.std(axis=0), 1, atol=0.01)
    
    def test_split_data_invalid_test_size(self):
        """Verifica que test_size inválido genere error"""
        X, y, _, _ = load_iris_data()
        
        with pytest.raises(ValueError):
            split_data(X, y, test_size=1.5)
        
        with pytest.raises(ValueError):
            split_data(X, y, test_size=0)


# ============================================================================
# TESTS DEL MODELO
# ============================================================================

class TestModelTrainer:
    """Tests para el entrenador del modelo"""
    
    @pytest.fixture
    def trained_model(self):
        """Fixture para obtener un modelo entrenado"""
        X, y, _, _ = load_iris_data()
        X_train, X_test, y_train, y_test = split_data(X, y)
        X_train_scaled, X_test_scaled, _ = scale_data(X_train, X_test)
        
        trainer = ModelTrainer(n_estimators=10, max_depth=5)
        trainer.train(X_train_scaled, y_train)
        
        return trainer, X_test_scaled, y_test
    
    def test_model_initialization(self):
        """Verifica que el modelo se inicialice correctamente"""
        trainer = ModelTrainer()
        
        assert trainer.model is not None
        assert trainer.is_trained == False
        assert trainer.metrics == {}
    
    def test_model_train(self, trained_model):
        """Verifica que el modelo se entrene"""
        trainer, _, _ = trained_model
        
        assert trainer.is_trained == True
        assert trainer.model is not None
    
    def test_model_predict(self, trained_model):
        """Verifica que el modelo haga predicciones"""
        trainer, X_test, _ = trained_model
        
        predictions = trainer.predict(X_test)
        
        assert predictions.shape == (X_test.shape[0],)
        assert np.all(np.isin(predictions, [0, 1, 2]))
    
    def test_model_predict_proba(self, trained_model):
        """Verifica que las probabilidades sean válidas"""
        trainer, X_test, _ = trained_model
        
        proba = trainer.predict_proba(X_test)
        
        assert proba.shape == (X_test.shape[0], 3)
        assert np.allclose(proba.sum(axis=1), 1.0)
        assert np.all(proba >= 0) and np.all(proba <= 1)
    
    def test_model_accuracy(self, trained_model):
        """Verifica que el accuracy sea razonable"""
        trainer, X_test, y_test = trained_model
        
        metrics = trainer.evaluate(X_test, y_test)
        
        assert metrics['accuracy'] > 0.7, "Accuracy debe ser > 70%"
        assert metrics['accuracy'] <= 1.0
    
    def test_model_metrics_validity(self, trained_model):
        """Verifica que las métricas sean válidas"""
        trainer, X_test, y_test = trained_model
        
        metrics = trainer.evaluate(X_test, y_test)
        
        assert 0 <= metrics['accuracy'] <= 1
        assert 0 <= metrics['precision'] <= 1
        assert 0 <= metrics['recall'] <= 1
        assert 0 <= metrics['f1_score'] <= 1
    
    def test_model_save_load(self, trained_model, tmp_path):
        """Verifica que se pueda guardar y cargar el modelo"""
        trainer, X_test, y_test = trained_model
        
        # Guardar
        model_path = str(tmp_path / "test_model.joblib")
        trainer.save_model(model_path)
        assert Path(model_path).exists()
        
        # Cargar
        trainer2 = ModelTrainer()
        trainer2.load_model(model_path)
        
        # Comparar predicciones
        pred1 = trainer.predict(X_test)
        pred2 = trainer2.predict(X_test)
        
        assert np.array_equal(pred1, pred2)
    
    def test_model_train_without_training_raises_error(self):
        """Verifica que evaluar sin entrenar genere error"""
        trainer = ModelTrainer()
        X, _, _, _ = load_iris_data()
        
        with pytest.raises(RuntimeError):
            trainer.evaluate(X, np.zeros(X.shape[0]))
    
    def test_model_predict_without_training_raises_error(self):
        """Verifica que predecir sin entrenar genere error"""
        trainer = ModelTrainer()
        X, _, _, _ = load_iris_data()
        
        with pytest.raises(RuntimeError):
            trainer.predict(X)


# ============================================================================
# TESTS DEL SERVICIO
# ============================================================================

class TestPredictionService:
    """Tests para el servicio de predicción"""
    
    def test_service_initialization(self):
        """Verifica que el servicio se inicialice"""
        service = PredictionService()
        
        assert service.trainer is None
        assert service.scaler is None
        assert service.is_healthy() == False
    
    def test_prediction_request_creation(self):
        """Verifica que se cree correctamente la request"""
        request = IrisPredictionRequest(
            sepal_length=5.1,
            sepal_width=3.5,
            petal_length=1.4,
            petal_width=0.2
        )
        
        array = request.to_array()
        assert len(array) == 4
        assert array[0] == 5.1
    
    def test_prediction_request_validation(self):
        """Verifica que la validación funcione"""
        # Valores negativos no permitidos
        with pytest.raises(Exception):
            IrisPredictionRequest(
                sepal_length=-5.1,
                sepal_width=3.5,
                petal_length=1.4,
                petal_width=0.2
            )
        
        # Valores fuera de rango
        with pytest.raises(Exception):
            IrisPredictionRequest(
                sepal_length=50.0,  # Muy grande
                sepal_width=3.5,
                petal_length=1.4,
                petal_width=0.2
            )


# ============================================================================
# TESTS DE INTEGRACIÓN
# ============================================================================

class TestIntegration:
    """Tests de integración end-to-end"""
    
    def test_full_pipeline(self):
        """Test completo del pipeline"""
        # Cargar datos
        X, y, _, target_names = load_iris_data()
        X_train, X_test, y_train, y_test = split_data(X, y)
        X_train_scaled, X_test_scaled, scaler = scale_data(X_train, X_test)
        
        # Entrenar
        trainer = ModelTrainer(n_estimators=50)
        trainer.train(X_train_scaled, y_train)
        
        # Evaluar
        metrics = trainer.evaluate(X_test_scaled, y_test, target_names)
        
        # Verificaciones
        assert metrics['accuracy'] > 0.85
        assert 'confusion_matrix' in metrics
        assert 'classification_report' in metrics
    
    def test_model_reproducibility(self):
        """Verifica que el modelo sea reproducible con mismo seed"""
        X, y, _, _ = load_iris_data()
        X_train, X_test, y_train, y_test = split_data(X, y, random_state=42)
        X_train_scaled, X_test_scaled, _ = scale_data(X_train, X_test)
        
        # Primer entrenamiento
        trainer1 = ModelTrainer(random_state=42)
        trainer1.train(X_train_scaled, y_train)
        pred1 = trainer1.predict(X_test_scaled)
        
        # Segundo entrenamiento con mismo seed
        trainer2 = ModelTrainer(random_state=42)
        trainer2.train(X_train_scaled, y_train)
        pred2 = trainer2.predict(X_test_scaled)
        
        # Deben ser idénticos
        assert np.array_equal(pred1, pred2)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
