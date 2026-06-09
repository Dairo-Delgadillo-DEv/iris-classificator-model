# Usa una imagen base oficial de Python ligera
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema requeridas (opcional pero recomendado)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar el archivo de dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del proyecto
COPY src/ /app/src/
COPY deployment/ /app/deployment/
COPY config/ /app/config/

# Si los modelos ya están generados, se pueden copiar
# COPY models/ /app/models/

# Exponer el puerto de la API
EXPOSE 5000

# Variables de entorno
ENV PYTHONPATH=/app
ENV PORT=5000

# Comando para ejecutar FastAPI usando uvicorn
CMD ["uvicorn", "deployment.api.app:app", "--host", "0.0.0.0", "--port", "5000"]
