# 📊 DIAGRAMA VISUAL DEL PROYECTO

## Pipeline de Entrenamiento

```
┌─────────────────────────────────────────────────────────────────┐
│                    IRIS ML PIPELINE                             │
└─────────────────────────────────────────────────────────────────┘

1. CARGAR DATOS
   ┌──────────────────────┐
   │  sklearn.iris        │
   │  150 muestras        │
   │  4 features          │
   │  3 clases            │
   └──────────┬───────────┘
              │ load_data.py
              ▼

2. DIVIDIR DATOS
   ┌─────────────────────────────┐
   │  X_train: 120 × 4           │
   │  X_test: 30 × 4             │
   │  y_train: 120               │
   │  y_test: 30                 │
   └──────────┬────────────────────┘
              │ train_test_split()
              ▼

3. NORMALIZAR
   ┌──────────────────────┐
   │  StandardScaler      │
   │  Media: 0            │
   │  SD: 1               │
   └──────────┬───────────┘
              │ scale_data()
              ▼

4. ENTRENAR
   ┌──────────────────────┐
   │  RandomForest        │
   │  - 100 árboles       │
   │  - max_depth=10      │
   └──────────┬───────────┘
              │ train.py
              ▼

5. EVALUAR
   ┌──────────────────────┐
   │  Accuracy: 96.7%     │
   │  Precision: 96.7%    │
   │  Recall: 96.7%       │
   │  F1: 96.7%           │
   └──────────┬───────────┘
              │ evaluate()
              ▼

6. GUARDAR
   ┌──────────────────────┐
   │  iris_model.joblib   │
   │  ~50 KB              │
   │  Listo para usar     │
   └──────────────────────┘
```

---

## Estructura de Carpetas

```
new_project_MLOps/
│
├── 🎯 CORE (Código ejecutable)
│   ├── main.py ........................ Ejecuta el pipeline
│   ├── predict_example.py ............ Ejemplo de predicciones
│   └── requirements.txt .............. Dependencias
│
├── 📚 CONFIGURACIÓN
│   ├── config/config.yaml ............ Parámetros del modelo
│   ├── .env.example .................. Variables de entorno
│   ├── setup.py ...................... Setup de package
│   └── .gitignore .................... Archivos a ignorar
│
├── 💻 CÓDIGO FUENTE (src/)
│   ├── data/
│   │   └── load_data.py ............. Cargar y procesar datos
│   ├── models/
│   │   └── train.py ................. Entrenar el modelo
│   ├── features/
│   │   └── features.py .............. Feature engineering
│   └── utils/
│       └── logger.py ................ Logging
│
├── 📊 DATOS (data/)
│   ├── raw/ .......................... Datos sin procesar
│   └── processed/ .................... Datos procesados
│
├── 💾 MODELOS GUARDADOS (models/)
│   └── iris_model.joblib ............ Modelo entrenado
│
├── 📝 DOCUMENTACIÓN
│   ├── README.md .................... Descripción general
│   ├── MLOPS_GUIDE.md ............... Guía detallada
│   ├── QUICKSTART.md ................ Inicio rápido
│   ├── RESPUESTAS.md ................ Respuestas a tus preguntas
│   └── ESTRUCTURA_COMPLETA.md ....... Mapa del proyecto
│
├── 📓 NOTEBOOKS (notebooks/)
│   ├── 01_eda.ipynb ................. Análisis exploratorio
│   └── 02_training.ipynb ............ Documentación entrenamiento
│
├── ✅ TESTS (tests/)
│   └── test_model.py ................ Tests unitarios
│
├── 📋 DEPLOYMENT
│   ├── api/ .......................... API REST
│   │   ├── app.py ................... Aplicación Flask
│   │   ├── wsgi.py .................. Configuración WSGI
│   │   └── requirements.txt ......... Dependencias API
│   │
│   ├── docker/ ...................... Containerización
│   │   ├── Dockerfile ............... Imagen Docker
│   │   ├── docker-compose.yml ....... Orquestación local
│   │   └── .dockerignore ............ Archivos ignorados
│   │
│   └── kubernetes/ .................. Orquestación
│       ├── deployment.yaml .......... Deployment K8S
│       ├── service.yaml ............. Service K8S
│       └── configmap.yaml ........... ConfigMap K8S
│
├── 📝 LOGS (logs/)
│   └── training.log ................. Logs de ejecución
│
└── 🔧 OTROS
    └── .gitignore ................... Archivos a ignorar en Git
```

---

## Flujo de Entrenamiento en Código

```python
# main.py ejecución:

1. load_config()
   ↓ Lee config.yaml
   
2. load_iris_data()
   ↓ Retorna X (150×4), y (150), names
   
3. split_data(X, y, test_size=0.2)
   ↓ Retorna X_train(120×4), X_test(30×4), y_train, y_test
   
4. scale_data(X_train, X_test)
   ↓ Normaliza con StandardScaler
   ↓ Retorna X_train_scaled, X_test_scaled, scaler
   
5. ModelTrainer.train(X_train_scaled, y_train)
   ↓ Crea 100 árboles de decisión
   ↓ Guarda modelo en trainer.model
   
6. trainer.evaluate(X_test_scaled, y_test)
   ↓ Predice en test set
   ↓ Calcula: accuracy, precision, recall, f1
   ↓ Retorna metrics dict
   
7. trainer.save_model('models/iris_model.joblib')
   ↓ Guarda modelo entrenado
   ↓ Archivo listo para predicciones
   
8. Mostrar resultados en logs
```

---

## Stack Tecnológico

```
┌─────────────────────────────────────────────┐
│            IRIS MLOPS STACK                │
├─────────────────────────────────────────────┤
│                                             │
│  Language: Python 3.8+                     │
│  ├─ scikit-learn (ML algorithms)          │
│  ├─ pandas (Data manipulation)            │
│  ├─ numpy (Numerical computing)           │
│  └─ matplotlib/seaborn (Visualization)    │
│                                             │
│  MLOps: Logging, Config Management         │
│  ├─ pyyaml (Config files)                │
│  ├─ python-dotenv (Environment vars)     │
│  └─ joblib (Model serialization)         │
│                                             │
│  Deployment: Container + Orchestration     │
│  ├─ Flask (REST API)                      │
│  ├─ Docker (Containerization)             │
│  ├─ Kubernetes (Orchestration)            │
│  └─ Gunicorn (WSGI server)                │
│                                             │
│  Testing: Quality Assurance                │
│  └─ pytest (Unit testing)                 │
│                                             │
└─────────────────────────────────────────────┘
```

---

## Flujo de Deployment

```
┌──────────────────────────────────────┐
│  1. LOCAL DEVELOPMENT                │
│  ├─ python main.py                  │
│  ├─ python predict_example.py       │
│  └─ pytest tests/                   │
└──────────────┬───────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│  2. API REST                         │
│  ├─ Flask app.py                    │
│  ├─ Endpoints: /health, /predict    │
│  └─ Testing: curl http://localhost:5000
└──────────────┬───────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│  3. DOCKER                           │
│  ├─ docker build -t iris:1.0 .     │
│  ├─ docker run -p 5000:5000        │
│  └─ docker push username/iris:1.0  │
└──────────────┬───────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│  4. KUBERNETES                       │
│  ├─ kubectl apply -f deployment/    │
│  ├─ kubectl get pods                │
│  └─ kubectl logs <pod-name>         │
└──────────────┬───────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│  5. PRODUCCIÓN                       │
│  ├─ Múltiples réplicas              │
│  ├─ Load balancing automático       │
│  ├─ Auto-scaling según demanda      │
│  └─ Monitoreo y alertas             │
└──────────────────────────────────────┘
```

---

## Ciclo de Vida del Modelo

```
┌─────────────────────────────────────────────────────────┐
│           MODEL LIFECYCLE                               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  DEVELOPMENT ──────────────────────┐                  │
│  ├─ Explore data (EDA)            │                  │
│  ├─ Build pipeline                 │                  │
│  ├─ Train model                    │                  │
│  └─ Evaluate (96.7% acc)           │                  │
│                          ↓                             │
│  PRODUCTION ────────────────────────────────────────┐  │
│  ├─ Save model (.joblib)                           │  │
│  ├─ Containerize (Docker)                          │  │
│  ├─ Deploy (Kubernetes)                            │  │
│  └─ Monitor performance                            │  │
│                          ↓                          │  │
│  MAINTENANCE ──────────────────────────────────────┘  │
│  ├─ Track metrics                                     │
│  ├─ Detect data drift                                │
│  ├─ Retrain if needed                                │
│  └─ A/B testing of new models                        │
│                                                       │
└─────────────────────────────────────────────────────────┘
```

---

**Este diagrama te muestra la arquitectura completa del proyecto MLOps**
