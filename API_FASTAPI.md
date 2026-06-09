# API REST con FastAPI

Documentación de la API REST para el modelo de clasificación de Iris.

## Quick Start

### 1. Entrenar el Modelo (Primera vez)

```bash
# Navega al proyecto
cd c:\Users\WINDOWS\Documents\DAIRO\MLOps\new_project_MLOps

# Activa venv
venv\Scripts\activate

# Instala dependencias
pip install -r requirements.txt

# Entrena el modelo
python main.py
# O si prefieres algo más rápido:
python train_once.py
```

### 2. Iniciar la API

```bash
# En una terminal
uvicorn deployment.api.app:app --reload --host 0.0.0.0 --port 5000
```

**Output esperado:**
```
INFO:     Uvicorn running on http://0.0.0.0:5000
INFO:     Application startup complete
```

### 3. Acceder a la Documentación

- **Swagger UI**: http://localhost:5000/docs
- **ReDoc**: http://localhost:5000/redoc

### 4. Probar la API

```bash
# En otra terminal
python test_api.py
```

## Endpoints

### GET `/health`
Health check de la API

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "version": "1.0.0"
}
```

---

### POST `/predict`
Realiza una predicción individual

**Request:**
```json
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
```

**Response:**
```json
{
  "prediction": "setosa",
  "prediction_id": 0,
  "confidence": 0.95,
  "probabilities": {
    "setosa": 0.95,
    "versicolor": 0.04,
    "virginica": 0.01
  }
}
```

---

### POST `/predict/batch`
Realiza predicciones en batch

**Request:**
```json
{
  "samples": [
    [5.1, 3.5, 1.4, 0.2],
    [7.0, 3.2, 4.7, 1.4],
    [6.3, 3.3, 6.0, 2.5]
  ]
}
```

**Response:**
```json
{
  "predictions": [
    {
      "prediction": "setosa",
      "prediction_id": 0,
      "confidence": 0.95,
      "probabilities": {...}
    },
    ...
  ],
  "count": 3
}
```

---

### GET `/model/info`
Información del modelo

**Response:**
```json
{
  "name": "Iris Flower Classifier",
  "version": "1.0.0",
  "algorithm": "RandomForestClassifier",
  "accuracy": 0.9667,
  "n_features": 4,
  "classes": ["setosa", "versicolor", "virginica"],
  "hyperparameters": {
    "n_estimators": 100,
    "max_depth": 10,
    "random_state": 42
  }
}
```

---

### GET `/version`
Versión de la API

**Response:**
```json
{
  "api_version": "1.0.0",
  "model_version": "1.0.0"
}
```

---

## Cliente Python

Usa el cliente Python para llamar a la API:

```python
from src.api_client import APIClient

# Inicializar cliente
client = APIClient("http://localhost:5000")

# Health check
health = client.health_check()
print(health)

# Predicción individual
response = client.predict(
    sepal_length=5.1,
    sepal_width=3.5,
    petal_length=1.4,
    petal_width=0.2
)
print(f"Predicción: {response['prediction']}")
print(f"Confianza: {response['confidence']:.2%}")

# Batch
samples = [
    [5.1, 3.5, 1.4, 0.2],
    [7.0, 3.2, 4.7, 1.4]
]
batch = client.predict_batch(samples)
print(f"Predicciones: {batch['count']}")

# Cerrar
client.close()
```

## Usando curl

```bash
# Health check
curl http://localhost:5000/health

# Predicción
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
  }'

# Batch
curl -X POST http://localhost:5000/predict/batch \
  -H "Content-Type: application/json" \
  -d '{
    "samples": [
      [5.1, 3.5, 1.4, 0.2],
      [7.0, 3.2, 4.7, 1.4]
    ]
  }'

# Model info
curl http://localhost:5000/model/info
```

## Producción con Gunicorn

```bash
# Con 4 workers
gunicorn deployment.api.wsgi:app \
  --bind 0.0.0.0:5000 \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --max-requests 1000 \
  --timeout 60
```

## Variables de Entorno

Crea `.env` para personalizar:

```env
FLASK_ENV=development
MODEL_PATH=models/iris_model.joblib
SCALER_PATH=models/iris_scaler.joblib
LOG_LEVEL=INFO
API_HOST=0.0.0.0
API_PORT=5000
MAX_BATCH_SIZE=1000
CORS_ORIGINS=*
```

## Estructura

```
deployment/api/
├── app.py                 # Aplicación FastAPI principal
├── wsgi.py               # Configuración WSGI para Gunicorn
├── config.py             # Configuración de la app
├── requirements.txt      # Dependencias
└── __init__.py          # Package init

Clientes:
├── src/api_client.py    # Cliente HTTP Python
├── test_api.py          # Tests de la API
└── validate.py          # Validación del setup
```

## Testing

```bash
# Validar setup
python validate.py

# Tests del modelo
pytest tests/test_model.py -v

# Tests de la API
python test_api.py
```

## Troubleshooting

### Modelo no encontrado
```
⚠ WARNING: Modelo no encontrado en models/iris_model.joblib
```

**Solución:**
```bash
python main.py
# o
python train_once.py
```

### Error de conexión
```
ConnectionError: Failed to connect to API
```

**Solución:**
- Asegúrate de que la API esté ejecutándose
- Verifica puerto 5000: `netstat -an | grep 5000`
- Cambia puerto en uvicorn: `--port 8000`

### Timeout
```
ReadTimeout: HTTPConnectionPool timed out
```

**Solución:**
- Aumenta timeout en cliente: `APIClient(..., timeout=30)`
- Verifica que el modelo no sea muy grande
- Usa batch más pequeños

## Métricas Esperadas

| Métrica | Valor |
|---------|-------|
| **Accuracy** | 96.7% |
| **Latencia** | <10ms |
| **Throughput** | >1000 req/s |

## Estructura de Request/Response

### Error Response

```json
{
  "error": "Validation Error",
  "detail": "Error details...",
  "status_code": 422
}
```

### Códigos HTTP

| Código | Significado |
|--------|------------|
| 200 | Éxito |
| 400 | Bad Request |
| 422 | Validation Error |
| 503 | Service Unavailable |
| 500 | Internal Server Error |

---

**API completa y lista para usar! 🚀**
