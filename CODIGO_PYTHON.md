# 📚 Índice Completo del Código Python

Este documento contiene el índice de todo el código Python creado para el proyecto MLOps de clasificación de Iris.

## 📁 Estructura del Proyecto

```
new_project_MLOps/
├── 🎯 SCRIPTS PRINCIPALES
│   ├── main.py                      ⭐ Pipeline de entrenamiento completo
│   ├── predict_example.py           ⭐ Ejemplos de predicción
│   ├── train_once.py                📌 Entrenamiento rápido
│   ├── validate.py                  📌 Validación del setup
│   └── test_api.py                  📌 Tests de la API
│
├── 📦 SRC (Código del Modelo)
│   ├── __init__.py
│   ├── schemas.py                   ⭐ Modelos Pydantic para validación
│   ├── services.py                  ⭐ Servicio de predicción
│   ├── api_client.py                📌 Cliente HTTP para la API
│   │
│   ├── data/
│   │   ├── __init__.py
│   │   └── load_data.py             ⭐ Carga, split, normalizacion de datos
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── train.py                 ⭐ Clase ModelTrainer para Random Forest
│   │
│   └── utils/
│       ├── __init__.py
│       └── logger.py                📌 Setup de logging centralizado
│
├── 🚀 DEPLOYMENT/API (API FastAPI)
│   ├── app.py                       ⭐ Aplicación FastAPI principal
│   ├── wsgi.py                      📌 Configuración WSGI para Gunicorn
│   ├── config.py                    📌 Configuración de la aplicación
│   ├── requirements.txt             📌 Dependencias de la API
│   └── __init__.py
│
├── ✅ TESTS
│   ├── __init__.py
│   └── test_model.py                ⭐ Tests unitarios completos
│
├── 📖 DOCUMENTACIÓN
│   ├── API_FASTAPI.md               📌 Guía de la API REST
│   ├── CODIGO_PYTHON.md             📌 Este archivo
│   └── requirements.txt             📌 Dependencias principales
│
└── 📊 DATOS Y MODELOS
    └── models/                      (Generado por main.py)
        ├── iris_model.joblib        Modelo entrenado
        ├── iris_scaler.joblib       Scaler de datos
        └── metrics.json             Métricas de entrenamiento
```

---

## 🎯 SCRIPTS PRINCIPALES

### main.py - Pipeline Completo ⭐

**Propósito:** Script principal que ejecuta el pipeline completo de MLOps

**Funciones clave:**
- `load_config()` - Carga configuración desde YAML
- `main()` - Ejecuta pipeline: cargar datos → split → escalar → entrenar → evaluar → guardar

**Flujo:**
```
1. Cargar config (config/config.yaml)
2. Cargar datos (150 flores Iris)
3. Split 80/20 train/test
4. Normalizar con StandardScaler
5. Entrenar Random Forest (100 árboles)
6. Evaluar y guardar métricas
7. Guardar modelo y scaler
```

**Uso:**
```bash
python main.py
```

**Output:**
```
Accuracy:  0.9667 (96.67%)
Precision: 0.9667
Recall:    0.9667
F1-Score:  0.9667
✓ PIPELINE COMPLETADO
```

---

### predict_example.py - Ejemplos de Predicción ⭐

**Propósito:** 4 ejemplos funcionales de cómo usar el modelo

**Ejemplos:**
1. `example_single_prediction()` - Predicción individual
2. `example_batch_prediction()` - Predicción en batch (3 flores)
3. `example_test_set_predictions()` - Predicciones en test set con comparación
4. `example_model_info()` - Información del modelo

**Uso:**
```bash
python predict_example.py
```

---

### train_once.py - Entrenamiento Rápido 📌

**Propósito:** Entrenar modelo una sola vez sin mucha salida

**Diferencia con main.py:**
- Más conciso
- Menos logging
- Directo al punto

**Uso:**
```bash
python train_once.py
```

---

### validate.py - Validación del Setup 📌

**Propósito:** Valida que todo esté configurado correctamente

**Checks:**
1. Dataset Iris cargable
2. Archivo del modelo existe
3. Archivo del scaler existe
4. Modelo se carga correctamente
5. Scaler se carga correctamente
6. Servicio de predicción funciona
7. Predicción de prueba funciona
8. Esquemas Pydantic válidos

**Uso:**
```bash
python validate.py
```

---

### test_api.py - Tests de la API REST 📌

**Propósito:** Prueba todos los endpoints de la API

**Tests:**
1. Health Check
2. Model Info
3. Single Prediction
4. Batch Prediction
5. API Version

**Uso:**
```bash
# Terminal 1
uvicorn deployment.api.app:app --reload

# Terminal 2
python test_api.py
```

---

## 📦 SRC - Código del Modelo

### schemas.py - Modelos Pydantic ⭐

**Propósito:** Validación de datos en la API con Pydantic

**Modelos:**
- `IrisPredictionRequest` - Request de predicción individual
- `BatchPredictionRequest` - Request de batch
- `PredictionResponse` - Response de predicción
- `BatchPredictionResponse` - Response de batch
- `ModelInfo` - Información del modelo
- `HealthResponse` - Respuesta de health check
- `ErrorResponse` - Respuesta de error

**Ejemplo:**
```python
from src.schemas import IrisPredictionRequest

request = IrisPredictionRequest(
    sepal_length=5.1,
    sepal_width=3.5,
    petal_length=1.4,
    petal_width=0.2
)
# Validación automática: valores entre 0-10
```

---

### services.py - Servicio de Predicción ⭐

**Propósito:** Capa de lógica de negocio para predicciones

**Clase `PredictionService`:**
- Carga modelo y scaler
- Realiza predicciones
- Gestiona el ciclo de vida del modelo

**Métodos:**
- `load_model()` - Carga modelo y scaler
- `predict_single(request)` - Predicción individual
- `predict_batch(samples)` - Predicción en batch
- `get_model_info()` - Info del modelo
- `is_healthy()` - Verifica si está listo

**Ejemplo:**
```python
from src.services import PredictionService
from src.schemas import IrisPredictionRequest

service = PredictionService()
service.load_model()

request = IrisPredictionRequest(...)
response = service.predict_single(request)

print(f"Predicción: {response.prediction}")
print(f"Confianza: {response.confidence:.2%}")
```

---

### api_client.py - Cliente HTTP 📌

**Propósito:** Cliente Python para comunicarse con la API

**Clase `APIClient`:**
- Método HTTP al servidor FastAPI
- Context manager para sesiones

**Métodos:**
- `health_check()`
- `predict(sepal_length, sepal_width, petal_length, petal_width)`
- `predict_batch(samples)`
- `get_model_info()`
- `get_version()`

**Ejemplo:**
```python
from src.api_client import APIClient

with APIClient("http://localhost:5000") as client:
    health = client.health_check()
    response = client.predict(5.1, 3.5, 1.4, 0.2)
    print(response['prediction'])
```

---

### data/load_data.py - Carga de Datos ⭐

**Propósito:** Funciones para cargar, dividir y normalizar datos

**Funciones:**
- `load_iris_data()` - Carga dataset Iris de sklearn
- `load_iris_dataframe()` - Carga como DataFrame de pandas
- `split_data(X, y, test_size=0.2)` - Split train/test con stratify
- `scale_data(X_train, X_test)` - Normaliza con StandardScaler
- `save_scaler(scaler, filepath)` - Guarda el scaler
- `load_scaler(filepath)` - Carga un scaler

**Características:**
- Validación de datos
- Logging detallado
- Stratification en split
- Normalización con media=0, std=1

**Ejemplo:**
```python
from src.data.load_data import load_iris_data, split_data, scale_data

X, y, feature_names, target_names = load_iris_data()
X_train, X_test, y_train, y_test = split_data(X, y)
X_train_s, X_test_s, scaler = scale_data(X_train, X_test)
```

---

### models/train.py - Entrenador de Modelo ⭐

**Propósito:** Clase para entrenar y evaluar Random Forest

**Clase `ModelTrainer`:**
- Encapsula toda la lógica del modelo
- Gestiona entrenamiento y evaluación
- Guarda/carga modelo

**Métodos:**
- `__init__()` - Inicializa Random Forest
- `train(X_train, y_train)` - Entrena el modelo
- `evaluate(X_test, y_test)` - Evalúa en test set
- `predict(X)` - Predicciones duras
- `predict_proba(X)` - Predicciones con probabilidad
- `save_model(filepath)` - Guarda con joblib
- `load_model(filepath)` - Carga modelo
- `save_metrics(filepath)` - Guarda métricas JSON
- `get_feature_importance()` - Importancia de features
- `get_model_info()` - Info del modelo

**Ejemplo:**
```python
from src.models.train import ModelTrainer

trainer = ModelTrainer(n_estimators=100, max_depth=10)
trainer.train(X_train_scaled, y_train)
metrics = trainer.evaluate(X_test_scaled, y_test)

print(f"Accuracy: {metrics['accuracy']:.4f}")

trainer.save_model('models/iris_model.joblib')
```

---

### utils/logger.py - Logging Centralizado 📌

**Propósito:** Configuración centralizada de logging

**Función:**
- `setup_logging(level='INFO')` - Configura logger global

**Características:**
- Formato estandarizado
- Output a consola
- Niveles configurables

**Uso:**
```python
from src.utils.logger import setup_logging

logger = setup_logging()
logger.info("Mensaje")
logger.error("Error")
```

---

## 🚀 DEPLOYMENT/API - API FastAPI

### app.py - Aplicación FastAPI ⭐

**Propósito:** Servidor FastAPI con todos los endpoints

**Características:**
- 6 endpoints principales
- CORS habilitado
- Manejo de errores
- Documentación automática
- Validación con Pydantic
- Lifecycle management (startup/shutdown)

**Endpoints:**
```
GET  /                    - Info de la API
GET  /health              - Health check
POST /predict             - Predicción individual
POST /predict/batch       - Predicción en batch
GET  /model/info          - Información del modelo
GET  /version             - Versión de la API
```

**Ejemplo:**
```bash
# Iniciar
uvicorn deployment.api.app:app --reload

# En el navegador
http://localhost:5000/docs  # Swagger UI
http://localhost:5000/redoc # ReDoc
```

---

### wsgi.py - Configuración WSGI 📌

**Propósito:** Wrapper para ejecutar con Gunicorn

**Uso:**
```bash
gunicorn deployment.api.wsgi:app \
  --bind 0.0.0.0:5000 \
  --workers 4
```

---

### config.py - Configuración 📌

**Propósito:** Centraliza todas las configuraciones

**Clase `Settings`:**
- Rutas de modelo y scaler
- Configuración de API
- Limites de validación
- Logging

**Uso:**
```python
from deployment.api.config import settings

print(settings.model_path)
print(settings.max_batch_size)
```

---

## ✅ TESTS

### test_model.py - Tests Unitarios ⭐

**Propósito:** Cobertura completa de tests

**Clases de Test:**
- `TestLoadData` - Tests de carga de datos (5 tests)
- `TestModelTrainer` - Tests del modelo (10 tests)
- `TestPredictionService` - Tests del servicio (3 tests)
- `TestIntegration` - Tests E2E (2 tests)

**Total: 20 tests**

**Tests clave:**
```python
# Datos
- test_load_iris_data_shape()
- test_split_data_stratification()
- test_scale_data_normalization()

# Modelo
- test_model_train()
- test_model_accuracy()
- test_model_save_load()

# Integración
- test_full_pipeline()
- test_model_reproducibility()
```

**Uso:**
```bash
pytest tests/test_model.py -v
pytest tests/test_model.py::TestModelTrainer::test_model_accuracy -v
```

---

## 📋 Resumen de Archivos

### Archivos Python Completos (24)

| Archivo | Líneas | Propósito |
|---------|--------|-----------|
| **main.py** | 120 | Pipeline completo |
| **predict_example.py** | 150 | Ejemplos de predicción |
| **train_once.py** | 60 | Entrenamiento rápido |
| **validate.py** | 200 | Validación del setup |
| **test_api.py** | 150 | Tests de API |
| **src/schemas.py** | 150 | Modelos Pydantic |
| **src/services.py** | 200 | Servicio de predicción |
| **src/api_client.py** | 150 | Cliente HTTP |
| **src/data/load_data.py** | 180 | Carga de datos |
| **src/models/train.py** | 250 | Entrenador del modelo |
| **src/utils/logger.py** | 40 | Logging |
| **deployment/api/app.py** | 300 | API FastAPI |
| **deployment/api/wsgi.py** | 20 | Config WSGI |
| **deployment/api/config.py** | 90 | Configuración |
| **tests/test_model.py** | 350 | Tests unitarios |
| **+ 9 archivos __init__.py** | - | Package init |

**Total: ~2100 líneas de código Python**

---

## 🔄 Flujos Principales

### Flujo de Entrenamiento
```
main.py
  ├─ load_config()
  ├─ load_iris_data()
  ├─ split_data()
  ├─ scale_data()
  ├─ ModelTrainer.train()
  ├─ ModelTrainer.evaluate()
  ├─ ModelTrainer.save_model()
  └─ save_scaler()
```

### Flujo de Predicción (Offline)
```
predict_example.py
  ├─ PredictionService.load_model()
  ├─ IrisPredictionRequest(...)
  ├─ PredictionService.predict_single()
  └─ print(response)
```

### Flujo de Predicción (API)
```
POST /predict
  ├─ Validar request (Pydantic)
  ├─ PredictionService.predict_single()
  ├─ Formatear response
  └─ Return JSON
```

---

## 📚 Dependencias Principales

```
numpy==1.24.3              # Operaciones numéricas
pandas==2.0.3              # DataFrames
scikit-learn==1.3.0        # Machine Learning
fastapi==0.104.1           # Web framework
uvicorn==0.24.0            # ASGI server
pydantic==2.5.0            # Validación de datos
joblib==1.3.1              # Serialización
pytest==7.4.0              # Testing
gunicorn==21.2.0           # Production server
requests==2.31.0           # HTTP client
```

---

## ✅ Checklist de Código

- ✅ Carga de datos completa y validada
- ✅ Entrenamiento del modelo funcionando
- ✅ Predicciones individual y batch
- ✅ API REST con FastAPI
- ✅ Cliente HTTP Python
- ✅ Tests unitarios (20 tests)
- ✅ Validación con Pydantic
- ✅ Servicio de predicción
- ✅ Logging centralizado
- ✅ Documentación de API
- ✅ Scripts de validación
- ✅ Ejemplos funcionales

---

## 🚀 Próximos Pasos

### Ahora que tienes todo el código Python:

1. **Ejecutar pipeline:**
   ```bash
   python main.py
   ```

2. **Iniciar API:**
   ```bash
   uvicorn deployment.api.app:app --reload
   ```

3. **Probar endpoints:**
   ```bash
   python test_api.py
   ```

4. **Ejecutar tests:**
   ```bash
   pytest tests/test_model.py -v
   ```

### Para deployment:

5. **Docker** (lo hacemos después)
6. **Kubernetes** (lo hacemos después)
7. **CI/CD** (lo hacemos después)

---

**¡ Código Python 100% completo y funcional! 🎉**
