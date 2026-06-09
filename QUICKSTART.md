# 🚀 Quick Start - MLOps Iris Classification

Guía rápida para empezar a usar el proyecto.

## ⚡ 30 segundos - Setup Básico

```bash
# 1. Navega al proyecto
cd c:\Users\WINDOWS\Documents\DAIRO\MLOps\new_project_MLOps

# 2. Activa el entorno virtual
venv\Scripts\activate

# 3. Instala dependencias (si no lo hiciste)
pip install -r requirements.txt

# 4. Entrena el modelo
python main.py

# 5. Inicia la API
uvicorn deployment.api.app:app --reload

# 6. ¡Abre en el navegador!
# http://localhost:5000/docs
```

---

## 📋 Pasos Detallados

### Paso 1: Preparación

```bash
cd c:\Users\WINDOWS\Documents\DAIRO\MLOps\new_project_MLOps
```

### Paso 2: Entorno Virtual

```bash
# Crear (primera vez)
python -m venv venv

# Activar
venv\Scripts\activate

# Desactivar (después)
deactivate
```

### Paso 3: Instalar Dependencias

```bash
# Instalar todo
pip install -r requirements.txt

# O solo lo esencial
pip install scikit-learn pandas numpy fastapi uvicorn pydantic
```

### Paso 4: Entrenar Modelo

#### Opción A: Pipeline Completo (Recomendado)
```bash
python main.py
```

**Output esperado:**
```
✓ Config cargada
✓ Datos cargados (150 muestras)
✓ Datos divididos (120 train, 30 test)
✓ Datos normalizados
✓ Modelo entrenado
✓ Accuracy: 0.9667
✓ Modelo guardado
✓ Scaler guardado
✓ Métricas guardadas
```

#### Opción B: Entrenamiento Rápido
```bash
python train_once.py
```

### Paso 5: Validar Setup

```bash
python validate.py
```

**Output esperado:**
```
[CHECK 1] Datos Iris ✓
[CHECK 2] Archivo del modelo ✓
[CHECK 3] Archivo del scaler ✓
[CHECK 4] Cargar modelo ✓
[CHECK 5] Cargar scaler ✓
[CHECK 6] Servicio de predicción ✓
[CHECK 7] Predicción de prueba ✓
[CHECK 8] Esquemas Pydantic ✓

RESULTADO: 8/8 checks pasados
✓ ¡TODO FUNCIONA CORRECTAMENTE!
```

---

## 🌐 Iniciar la API

### Terminal 1: Servidor API

```bash
# Desarrollo (con auto-reload)
uvicorn deployment.api.app:app --reload

# Producción (4 workers)
gunicorn deployment.api.wsgi:app --bind 0.0.0.0:5000 --workers 4
```

**Output esperado:**
```
INFO:     Uvicorn running on http://0.0.0.0:5000
INFO:     Application startup complete
```

### Terminal 2: Pruebas

```bash
# Tests de la API
python test_api.py

# O usar curl
curl http://localhost:5000/health

# O abrir en navegador
# http://localhost:5000/docs   (Swagger UI)
# http://localhost:5000/redoc  (ReDoc)
```

---

## 🧪 Pruebas

### Test del Modelo

```bash
python predict_example.py
```

**Output:**
```
[EJEMPLO 1] Predicción Individual
  Input: [5.1, 3.5, 1.4, 0.2]
  Predicción: setosa
  Confianza: 0.95

[EJEMPLO 2] Predicción en Batch
  3 predicciones realizadas
  ...
```

### Tests Unitarios

```bash
# Todos los tests
pytest tests/test_model.py -v

# Test específico
pytest tests/test_model.py::TestModelTrainer::test_model_accuracy -v

# Con cobertura
pytest tests/test_model.py --cov=src
```

### Test de la API

```bash
# Terminal 1: API corriendo
uvicorn deployment.api.app:app --reload

# Terminal 2: Tests
python test_api.py
```

---

## 🔍 Ejemplos de Uso

### Predicción Individual (Python)

```python
from src.services import PredictionService
from src.schemas import IrisPredictionRequest

# Cargar servicio
service = PredictionService()
service.load_model()

# Crear request
request = IrisPredictionRequest(
    sepal_length=5.1,
    sepal_width=3.5,
    petal_length=1.4,
    petal_width=0.2
)

# Predicción
response = service.predict_single(request)

# Resultados
print(f"Predicción: {response.prediction}")
print(f"Confianza: {response.confidence:.2%}")
print(f"Probabilidades: {response.probabilities}")
```

### Predicción con API (curl)

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
  }'
```

**Response:**
```json
{
  "prediction": "setosa",
  "confidence": 0.95,
  "probabilities": {
    "setosa": 0.95,
    "versicolor": 0.04,
    "virginica": 0.01
  }
}
```

### Cliente Python

```python
from src.api_client import APIClient

client = APIClient("http://localhost:5000")

# Health check
health = client.health_check()
print(f"Status: {health['status']}")

# Predicción
response = client.predict(5.1, 3.5, 1.4, 0.2)
print(f"Prediction: {response['prediction']}")

# Batch
samples = [[5.1, 3.5, 1.4, 0.2], [7.0, 3.2, 4.7, 1.4]]
batch = client.predict_batch(samples)
print(f"Predicciones: {batch['count']}")

client.close()
```

---

## 📁 Estructura de Directorios Clave

```
new_project_MLOps/
├── main.py                  ⭐ Ejecutar primero
├── predict_example.py       📌 Ejemplos de uso
├── test_api.py             📌 Probar API
├── validate.py             📌 Validar setup
│
├── src/
│   ├── schemas.py          ✓ Validación
│   ├── services.py         ✓ Lógica de negocio
│   ├── api_client.py       ✓ Cliente HTTP
│   ├── data/load_data.py   ✓ Datos
│   ├── models/train.py     ✓ Modelo
│   └── utils/logger.py     ✓ Logging
│
├── deployment/api/
│   ├── app.py              ✓ API FastAPI
│   ├── wsgi.py             ✓ Gunicorn
│   ├── config.py           ✓ Configuración
│   └── requirements.txt    ✓ Dependencias
│
├── tests/
│   └── test_model.py       ✓ Tests unitarios
│
├── models/                 (Generado por main.py)
│   ├── iris_model.joblib
│   ├── iris_scaler.joblib
│   └── metrics.json
│
└── config/
    └── config.yaml         ✓ Configuración YAML
```

---

## 🔧 Troubleshooting

### Error: "Model not found"

```bash
python main.py
# o
python train_once.py
```

### Error: "Port 5000 already in use"

```bash
# Usa otro puerto
uvicorn deployment.api.app:app --reload --port 8000

# O mata el proceso
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Error: "ModuleNotFoundError"

```bash
# Asegúrate de estar en el venv correcto
venv\Scripts\activate

# Reinstala dependencias
pip install -r requirements.txt --force-reinstall
```

### Error: "CORS"

La API tiene CORS habilitado por defecto. Si tienes problemas:

1. Edita `deployment/api/app.py`
2. Cambia `allow_origins=["*"]` a tu dominio específico

---

## 📚 Documentación

| Documento | Contenido |
|-----------|----------|
| [API_FASTAPI.md](API_FASTAPI.md) | Guía de la API REST |
| [CODIGO_PYTHON.md](CODIGO_PYTHON.md) | Índice de todo el código |
| [README.md](README.md) | Información del proyecto |
| [QUICKSTART.md](QUICKSTART.md) | Este archivo |

---

## 📊 Comandos Útiles

| Comando | Propósito |
|---------|-----------|
| `python main.py` | Entrenar modelo |
| `python train_once.py` | Entrenamiento rápido |
| `python predict_example.py` | Ejemplos |
| `python validate.py` | Validar setup |
| `python test_api.py` | Probar API |
| `pytest tests/ -v` | Tests unitarios |
| `uvicorn deployment.api.app:app --reload` | Iniciar API |
| `curl http://localhost:5000/docs` | Documentación |

---

## ✅ Checklist de Setup

- [ ] Proyecto clonado/descargado
- [ ] Virtualenv creado: `python -m venv venv`
- [ ] Virtualenv activado: `venv\Scripts\activate`
- [ ] Dependencias instaladas: `pip install -r requirements.txt`
- [ ] Modelo entrenado: `python main.py`
- [ ] Setup validado: `python validate.py`
- [ ] API iniciada: `uvicorn deployment.api.app:app --reload`
- [ ] API probada: `python test_api.py`

---

## 🎯 Próximos Pasos

1. **Aprender el código:**
   - Lee `CODIGO_PYTHON.md`
   - Explora cada archivo Python

2. **Experimentar:**
   - Modifica valores en `config/config.yaml`
   - Entrena con diferentes hiperparámetros
   - Crea tus propias predicciones

3. **Deployment:**
   - Docker (lo hacemos juntos después)
   - Kubernetes (lo hacemos juntos después)
   - CI/CD (lo hacemos juntos después)

---

## 💬 Contacto / Ayuda

Si tienes preguntas sobre el código, revisa:
1. Los docstrings en cada función
2. Los comentarios en el código
3. Los ejemplos en `predict_example.py`
4. La documentación de la API en `/docs`

---

**¡Listo para empezar! 🚀**

Ejecuta esto para empezar de inmediato:

```bash
cd c:\Users\WINDOWS\Documents\DAIRO\MLOps\new_project_MLOps
venv\Scripts\activate
python main.py
uvicorn deployment.api.app:app --reload
```

Luego abre: http://localhost:5000/docs

[PASO 6] Guardando modelo...
Modelo guardado en: models/iris_model.joblib

==================================================
```

## Paso 5: Hacer predicciones
```bash
python predict_example.py
```

---

## 📚 Próximos Pasos (Tu Tarea)

### 1. Completa el deployment/api/app.py
- Crea una API REST con Flask
- Endpoints: /health, /predict, /model/info
- Ver MLOPS_GUIDE.md para detalles

### 2. Completa el deployment/docker/Dockerfile
- Dockerfile con imagen Python 3.9
- Instala dependencias
- Copia archivos
- Expone puerto 5000
- Ver MLOPS_GUIDE.md para detalles

### 3. Completa el deployment/kubernetes/
- deployment.yaml (3 réplicas)
- service.yaml (LoadBalancer)
- configmap.yaml (configuración)
- Ver MLOPS_GUIDE.md para detalles

### 4. Tests (tests/test_model.py)
- Tests para load_data()
- Tests para model training
- Tests para predicciones

---

## 📖 Documentación Completa
- **MLOPS_GUIDE.md** ← Lee esto para entender cada paso
- **README.md** ← Descripción general del proyecto
- **requirements.txt** ← Dependencias necesarias
- **config/config.yaml** ← Parámetros del modelo

---

## 🎯 Checklist para GitHub

- [ ] Código entrenado (python main.py exitoso)
- [ ] API REST implementada (deployment/api/)
- [ ] Dockerfile creado (deployment/docker/)
- [ ] Kubernetes manifiestos (deployment/kubernetes/)
- [ ] Tests escritos (tests/)
- [ ] README actualizado
- [ ] .gitignore configurado
- [ ] Commits con mensajes claros
- [ ] Push a GitHub

---

## 💡 Tips para Entrevistas

Cuando presentes este proyecto:

1. **Explica el modelo**: "Random Forest es 100 árboles votando"
2. **Muestra el pipeline**: "Cargamos datos → dividimos → normalizamos → entrenamos"
3. **Habla de las métricas**: "96.7% accuracy en test set"
4. **Menciona MLOps**: "Implementé logging, Docker y Kubernetes"
5. **Demuestra deployment**: "La API está lista en contenedor"

---

**¡Ahora te toca implementar los archivos TODO! 🔥**
