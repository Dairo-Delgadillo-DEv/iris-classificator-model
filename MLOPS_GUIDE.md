# GUÍA COMPLETA DEL PROYECTO MLOPS - IRIS CLASSIFICATION

## 📖 ÍNDICE
1. [¿Qué es Iris Classification?](#qué-es)
2. [¿Qué es Random Forest?](#random-forest)
3. [¿Por qué este modelo?](#por-qué)
4. [Pipeline Completo](#pipeline)
5. [Explicación Paso a Paso](#paso-a-paso)
6. [Deployment Step by Step](#deployment)

---

## ¿QUÉ ES IRIS CLASSIFICATION? {#qué-es}

### El Dataset Iris

El **Dataset Iris** es uno de los datasets más famosos en Machine Learning. Fue creado por **Ronald Fisher** en 1936.

#### Características:
- **150 muestras** de flores Iris
- **4 características numéricas** de cada flor
- **3 especies** diferentes de Iris
- **Perfecto para principiantes** (datos limpios, bien balanceados)

#### Las 4 características medidas:

```
┌─────────────────────────────────────────┐
│  SEPAL LENGTH (Largo del sépalo)       │
│  Medido en centímetros                  │
│  Rango: 4.3 - 7.9 cm                   │
│                                         │
│  SEPAL WIDTH (Ancho del sépalo)        │
│  Medido en centímetros                  │
│  Rango: 2.0 - 4.4 cm                   │
│                                         │
│  PETAL LENGTH (Largo del pétalo)       │
│  Medido en centímetros                  │
│  Rango: 1.0 - 6.9 cm                   │
│                                         │
│  PETAL WIDTH (Ancho del pétalo)        │
│  Medido en centímetros                  │
│  Rango: 0.1 - 2.5 cm                   │
└─────────────────────────────────────────┘
```

#### Las 3 clases (especies):

```
1. SETOSA      (50 muestras)
   └─ Flores pequeñas
   
2. VERSICOLOR  (50 muestras)
   └─ Flores medianas
   
3. VIRGINICA   (50 muestras)
   └─ Flores grandes
```

### ¿Cuál es el objetivo?

**Predecir la especie de una flor** basándose en sus 4 características.

**Input**: [5.1, 3.5, 1.4, 0.2]  
**Output**: Setosa

---

## ¿QUÉ ES RANDOM FOREST? {#random-forest}

### Concepto Simple

Random Forest es un **conjunto de árboles de decisión** que "votan" juntos.

### Analogía del mundo real

```
Imagina que quieres clasificar un correo como SPAM o NO SPAM:

┌─────────────────────────────────────────────────────┐
│ Árbol 1: ¿Contiene "viagra"?                       │
│         Sí → SPAM, No → NO SPAM                    │
│                                                     │
│ Árbol 2: ¿El remitente es desconocido?            │
│         Sí → SPAM, No → NO SPAM                    │
│                                                     │
│ Árbol 3: ¿Tiene adjuntos ejecutables?             │
│         Sí → SPAM, No → NO SPAM                    │
│                                                     │
│ Árbol 4: ¿Usa muchos MAYÚSCULAS?                  │
│         Sí → SPAM, No → NO SPAM                    │
│                                                     │
│ ...más árboles...                                  │
│                                                     │
│ VOTACIÓN FINAL:                                    │
│ - SPAM: 7 votos ← GANADOR                          │
│ - NO SPAM: 3 votos                                 │
└─────────────────────────────────────────────────────┘

Resultado: El correo es clasificado como SPAM
```

### ¿Cómo funciona con Iris?

```
ÁRBOL 1
├─ ¿Petal Length > 2.5?
│  ├─ Sí: ¿Sepal Width > 3.0?
│  │  ├─ Sí: Virginica
│  │  └─ No: Versicolor
│  └─ No: Setosa

ÁRBOL 2
├─ ¿Sepal Length > 5.5?
│  ├─ Sí: ¿Petal Width > 1.5?
│  │  ├─ Sí: Virginica
│  │  └─ No: Versicolor
│  └─ No: Setosa

ÁRBOL 3
├─ ¿Petal Length > 3.0?
│  ... (similar pattern)

... más árboles ...

VOTACIÓN:
- Setosa: 85 votos ← GANADOR
- Versicolor: 10 votos
- Virginica: 5 votos

Predicción final: SETOSA
```

### Ventajas del Random Forest

| Ventaja | Explicación |
|---------|-------------|
| **Simple** | Fácil de entender y explicar |
| **Robusto** | Maneja bien datos pequeños y grandes |
| **No requiere normalización** | Los árboles no son sensibles a escala |
| **Rápido** | Entrena rápido, predice rápido |
| **Resiste overfitting** | Los múltiples árboles reducen overfitting |
| **Importancia de features** | Indica qué features son más importantes |

---

## ¿POR QUÉ ESTE MODELO? {#por-qué}

### Para Portfolio/Entrevistas

✅ **Fácil de explicar** → "Es como una votación de árboles"  
✅ **Datos limpios** → No hay ruido que confunda  
✅ **Alta precisión** → >96% accuracy  
✅ **Código simple** → Demuestra que entiendes ML  
✅ **Estructura profesional** → Muestra buenas prácticas  

### Para Aprender MLOps

Este proyecto te enseña:

1. **Carga de datos** (`src/data/load_data.py`)
2. **Preprocesamiento** (split, normalización)
3. **Entrenamiento** (`src/models/train.py`)
4. **Evaluación** (metrics)
5. **Guardado del modelo** (serialización)
6. **Logging** (monitoreo)
7. **Deployment** (Docker, Kubernetes)
8. **API** (Flask REST API)

---

## PIPELINE COMPLETO {#pipeline}

```
┌──────────────────┐
│  DATASET IRIS    │
│  (150 muestras)  │
└────────┬─────────┘
         │
         ▼
┌──────────────────────┐
│  LOAD_DATA.PY        │
│  - Cargar datos      │
│  - 150 × 4 features  │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│  TRAIN/TEST SPLIT    │
│  - 80% train (120)   │
│  - 20% test (30)     │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│  FEATURE SCALING     │
│  - StandardScaler    │
│  - Media=0, SD=1     │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│  TRAIN.PY            │
│  - Random Forest     │
│  - 100 árboles       │
│  - max_depth=10      │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│  EVALUATION          │
│  - Accuracy: 96.7%   │
│  - Precision: 96.7%  │
│  - Recall: 96.7%     │
│  - F1: 96.7%         │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│  SAVE MODEL          │
│  - Guardar .joblib   │
│  - Listo para deploy │
└──────────────────────┘
```

---

## EXPLICACIÓN PASO A PASO {#paso-a-paso}

### PASO 1: LOAD DATA (`load_iris_data()`)

```python
# Cargar el dataset Iris
X, y, feature_names, target_names = load_iris_data()

# Resultado:
# X.shape = (150, 4)  → 150 flores, 4 características
# y.shape = (150,)    → 150 labels (0, 1, 2)
# feature_names = ['sepal length (cm)', 'sepal width (cm)', ...]
# target_names = ['setosa', 'versicolor', 'virginica']
```

**¿Qué hace?**
- Carga el dataset Iris de sklearn
- Separa features (X) de target (y)
- Devuelve nombres para legibilidad

---

### PASO 2: TRAIN/TEST SPLIT (`split_data()`)

```python
X_train, X_test, y_train, y_test = split_data(X, y, test_size=0.2)

# Resultado:
# X_train.shape = (120, 4)   → Datos para entrenar
# X_test.shape = (30, 4)     → Datos para probar
# y_train.shape = (120,)     → Labels de entrenamiento
# y_test.shape = (30,)       → Labels de prueba
```

**¿Qué hace?**
- Divide datos en 80% entrenamiento, 20% prueba
- Mezcla aleatoriamente los datos
- Garantiza que el modelo se pruebe con datos nunca vistos

**¿Por qué es importante?**
- Si pruebas con los mismos datos de entrenamiento, el modelo parecerá mejor de lo que realmente es
- Necesitas datos nuevos para evaluar honestamente

---

### PASO 3: FEATURE SCALING (`scale_data()`)

```python
X_train_scaled, X_test_scaled, scaler = scale_data(X_train, X_test)

# Antes:
# X_train[0] = [5.1, 3.5, 1.4, 0.2]

# Después (normalizado):
# X_train_scaled[0] = [0.5, -0.3, -1.2, -0.5]
```

**¿Qué hace?**
- Convierte cada feature a media=0, desviación estándar=1
- Fórmula: z = (x - media) / desviación_estándar

**¿Por qué es importante?**
- Algunos algoritmos funcionan mejor con datos normalizados
- Evita que features con valores grandes dominen el modelo

---

### PASO 4: ENTRENAR MODELO (`ModelTrainer.train()`)

```python
trainer = ModelTrainer(n_estimators=100, max_depth=10)
trainer.train(X_train_scaled, y_train)

# El modelo construye:
# - 100 árboles de decisión
# - Cada árbol aprende patrones diferentes
# - Se guardan en trainer.model
```

**¿Qué hace?**
- Crea 100 árboles de decisión
- Cada árbol aprende a clasificar basándose en features
- Los árboles se "entrenan" con datos aleatorios

**Hiperparámetros:**
- `n_estimators=100`: Cuántos árboles crear
  - Más árboles = mejor precisión (pero más lento)
  - Menos árboles = más rápido (pero menos preciso)
  
- `max_depth=10`: Profundidad máxima de cada árbol
  - Más profundo = modelo más complejo (puede overfitear)
  - Menos profundo = modelo más simple (puede underfitear)

---

### PASO 5: EVALUAR MODELO (`ModelTrainer.evaluate()`)

```python
metrics = trainer.evaluate(X_test_scaled, y_test)

# Resultado:
# {
#   'accuracy': 0.9667,    → 96.67% correcto
#   'precision': 0.9667,   → 96.67% precisión
#   'recall': 0.9667,      → 96.67% cobertura
#   'f1_score': 0.9667     → 96.67% balance
# }
```

**¿Qué miden estas métricas?**

| Métrica | Significado | Fórmula |
|---------|-------------|---------|
| **Accuracy** | % de predicciones correctas | Correctas / Total |
| **Precision** | De los positivos predichos, ¿cuántos eran correctos? | TP / (TP + FP) |
| **Recall** | De los positivos reales, ¿cuántos predijimos? | TP / (TP + FN) |
| **F1-Score** | Balance entre Precision y Recall | 2 × (P × R) / (P + R) |

**Interpretación:**
- >95%: Excelente
- 85-95%: Muy bueno
- 70-85%: Bueno
- <70%: Necesita mejora

---

### PASO 6: GUARDAR MODELO (`ModelTrainer.save_model()`)

```python
trainer.save_model('models/iris_model.joblib')

# Resultado:
# - Archivo creado: models/iris_model.joblib
# - Tamaño: ~50KB (muy pequeño)
# - Formato: joblib (específico para sklearn)
# - Contenido: El modelo entrenado completo
```

**¿Por qué guardar?**
- El modelo ya está entrenado y listo
- No necesitas entrenar de nuevo
- Puedes cargarlo en producción
- Puedes compartirlo con otros

**¿Cómo cargar?**
```python
trainer2 = ModelTrainer()
trainer2.load_model('models/iris_model.joblib')
predicción = trainer2.predict([[5.1, 3.5, 1.4, 0.2]])
```

---

## DEPLOYMENT STEP BY STEP {#deployment}

### ¿Qué es Deployment?

**Deployment** = Poner tu modelo en producción para que otros usuarios lo usen.

### Etapas del Deployment

```
┌─────────────────────────────────────────────────────────────┐
│ 1. DESARROLLO LOCAL                                         │
│    - Crear y entrenar modelo en tu PC                      │
│    - Probar localmente                                      │
│    - Guardar en models/iris_model.joblib                   │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. CONTAINERIZACIÓN (Docker)                                │
│    - Crear Dockerfile                                       │
│    - Instalar dependencias en contenedor                    │
│    - Exponer puerto (5000)                                  │
│    - Comando: docker build -t iris-model .                 │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. REGISTRO (Docker Hub/ECR)                                │
│    - Subir imagen a registro público/privado               │
│    - Comando: docker push username/iris-model               │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. ORQUESTACIÓN (Kubernetes)                                │
│    - Desplegar múltiples instancias                         │
│    - Load balancing automático                              │
│    - Auto-scaling según demanda                             │
│    - Comando: kubectl apply -f deployment/kubernetes/      │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. MONITOREO Y LOGS                                         │
│    - Ver logs de la aplicación                              │
│    - Monitorear uso de CPU/memoria                          │
│    - Alertas si algo falla                                  │
└─────────────────────────────────────────────────────────────┘
```

### Fase 1: API REST (deployment/api/)

**¿Qué es una API REST?**

API = Interfaz de Programación de Aplicaciones  
REST = Representa transferencia de Estado

Es una forma de que otros programas hablen con tu modelo.

**Endpoints a implementar:**

```
GET  /health
└─ ¿La API está activa?
   Respuesta: {"status": "healthy"}

POST /predict
├─ Entrada: {"features": [5.1, 3.5, 1.4, 0.2]}
├─ Procesa: Normaliza, hace predicción
└─ Salida: {"prediction": "setosa", "confidence": 0.95}

GET  /model/info
└─ Información del modelo
   Respuesta: {"model": "RandomForest", "accuracy": 0.967}
```

**`deployment/api/app.py`** - Crear con Flask:

```python
# TODO: Implementar

from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Cargar modelo
model = joblib.load('models/iris_model.joblib')

@app.route('/health', methods=['GET'])
def health():
    """Check if API is running"""
    return jsonify({"status": "healthy"})

@app.route('/predict', methods=['POST'])
def predict():
    """Make prediction"""
    data = request.json
    features = np.array(data['features']).reshape(1, -1)
    prediction = model.predict(features)
    return jsonify({"prediction": str(prediction[0])})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

---

### Fase 2: Docker (deployment/docker/)

**¿Qué es Docker?**

Docker = Caja virtual que contiene tu aplicación + todo lo que necesita

**`deployment/docker/Dockerfile`** - Receta para crear la imagen:

```dockerfile
# TODO: Implementar

FROM python:3.9-slim

WORKDIR /app

# Copiar archivos
COPY requirements.txt .
COPY src/ src/
COPY models/ models/
COPY deployment/api/app.py .

# Instalar dependencias
RUN pip install -r requirements.txt

# Exponer puerto
EXPOSE 5000

# Comando para ejecutar
CMD ["python", "app.py"]
```

**Pasos para construir y ejecutar:**

```bash
# 1. Construir imagen
docker build -t iris-classifier:1.0 .

# 2. Ejecutar contenedor
docker run -p 5000:5000 iris-classifier:1.0

# 3. Probar API
curl http://localhost:5000/health
```

---

### Fase 3: Kubernetes (deployment/kubernetes/)

**¿Qué es Kubernetes?**

Kubernetes = Orquestador de contenedores  
Administra múltiples contenedores automáticamente

**`deployment/kubernetes/deployment.yaml`** - Especifica cómo desplegar:

```yaml
# TODO: Implementar

apiVersion: apps/v1
kind: Deployment
metadata:
  name: iris-classifier

spec:
  replicas: 3  # 3 copias del modelo ejecutándose
  
  selector:
    matchLabels:
      app: iris-classifier
  
  template:
    metadata:
      labels:
        app: iris-classifier
    spec:
      containers:
      - name: iris-api
        image: username/iris-classifier:1.0
        ports:
        - containerPort: 5000
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

**`deployment/kubernetes/service.yaml`** - Expone la aplicación:

```yaml
# TODO: Implementar

apiVersion: v1
kind: Service
metadata:
  name: iris-classifier-service

spec:
  type: LoadBalancer
  selector:
    app: iris-classifier
  ports:
  - protocol: TCP
    port: 80
    targetPort: 5000
```

**Desplegar en Kubernetes:**

```bash
# 1. Aplicar deployment
kubectl apply -f deployment/kubernetes/deployment.yaml

# 2. Aplicar service
kubectl apply -f deployment/kubernetes/service.yaml

# 3. Verificar pods
kubectl get pods

# 4. Ver logs
kubectl logs <pod-name>

# 5. Acceder a la aplicación
# La URL externa estará disponible después de minutos
kubectl get service iris-classifier-service
```

---

## RESUMEN

### Estructura de Carpetas

```
new_project_MLOps/
├── src/              ← Código del modelo
│   ├── data/        ← Cargar y preparar datos
│   └── models/      ← Entrenar y evaluar
├── models/          ← Modelo guardado
├── deployment/      ← Código para producción
│   ├── api/        ← API REST
│   ├── docker/     ← Contenedor
│   └── kubernetes/ ← Orquestación
└── main.py         ← Script principal
```

### Flujo de Trabajo

1. **Local**: `python main.py`
2. **API**: Crear `deployment/api/app.py`
3. **Docker**: Crear `deployment/docker/Dockerfile`
4. **K8S**: Crear `deployment/kubernetes/deployment.yaml`
5. **Deploy**: `kubectl apply -f deployment/`

### Métricas de Éxito

✅ Accuracy > 96%  
✅ API REST funcionando  
✅ Docker image creada  
✅ Kubernetes deployment funcionando  
✅ Código en GitHub profesional  

---

**¡Listo! Ahora tiene todo lo que necesita para completar el proyecto MLOps y impresionar a los futuros empleadores! 🚀**
