"""
Configuración WSGI para ejecutar FastAPI en producción con Gunicorn

Uso:
    gunicorn deployment.api.wsgi:app --bind 0.0.0.0:5000 --workers 4 --worker-class uvicorn.workers.UvicornWorker
    
Configuración recomendada para producción:
    gunicorn deployment.api.wsgi:app \
        --bind 0.0.0.0:5000 \
        --workers 4 \
        --worker-class uvicorn.workers.UvicornWorker \
        --max-requests 1000 \
        --max-requests-jitter 100 \
        --timeout 60 \
        --access-logfile - \
        --error-logfile -
"""

import logging
from deployment.api.app import app

# Configurar logging para producción
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.info("WSGI app importada para Gunicorn")

# La aplicación FastAPI se expondrá como 'app'
# Gunicorn la encontrará automáticamente en este módulo
