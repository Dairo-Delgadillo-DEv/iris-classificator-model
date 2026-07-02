# 🛡️ DevSecOps: Seguridad en el Proyecto MLOps

## ¿Qué es DevSecOps?

**DevSecOps** (Development, Security, and Operations) significa pensar en la seguridad de nuestra aplicación y de nuestro modelo de Machine Learning desde el inicio, y no como un paso final. 

En proyectos tradicionales de ML, los modelos o las APIs se exponen a riesgos como: dependencias de librerías con fallos conocidos (que los atacantes pueden aprovechar), secretos (como contraseñas o tokens) subidos por error al repositorio, o imágenes Docker mal configuradas. Con DevSecOps prevenimos todo eso de forma automatizada.

---

## 🔒 Flujo de Seguridad Implementado

Nuestro flujo de seguridad cubre **todo el ciclo de vida** del desarrollo:

1. **Local (En el computador del desarrollador):**
   Antes de que un desarrollador pueda hacer un `commit` (guardar sus cambios en Git), se ejecutan validaciones rápidas para asegurar que no haya contraseñas "quemadas" (hardcoded) en el código.
   *Herramienta:* `pre-commit` con `detect-secrets`.

2. **Integración Continua (En GitHub):**
   Cada vez que subimos código a GitHub (Push o Pull Request), se lanzan escaneos automáticos de forma paralela al entrenamiento y empaquetado del modelo:
   - **SAST (Pruebas de Seguridad Estáticas):** Revisa el código Python (ej. `app.py`, `train.py`) buscando patrones inseguros, inyecciones o vulnerabilidades clásicas. 
     *Herramienta:* `Bandit`.
   - **SCA (Análisis de Composición de Software):** Revisa el archivo `requirements.txt` buscando librerías de Python desactualizadas que tengan vulnerabilidades públicas.
     *Herramienta:* `Safety`.
   - **Container Security (Seguridad de la Infraestructura):** Una vez que Docker construye la imagen del modelo, esta se escanea para asegurar que no use un sistema base con fallos.
     *Herramienta:* `Trivy`.

---

## 🛠️ Herramientas Utilizadas y Cómo Funcionan

### 1. Bandit (SAST)
Bandit analiza los archivos `.py` para encontrar problemas comunes en Python, como el uso de librerías inseguras (ej. el módulo `pickle` inseguro de Python sin validaciones), uso de funciones deprecadas de criptografía, etc.

### 2. Safety (SCA)
Safety compara nuestras dependencias (en `requirements.txt`) contra una base de datos global de vulnerabilidades de Python (CVEs) y nos avisa si estamos usando una versión que puede ser "hackeada".

### 3. Trivy (Escaneo de Contenedores)
Trivy escanéa el `Dockerfile` y la imagen generada, alertándonos de vulnerabilidades del sistema operativo (por ejemplo, si usamos una versión muy antigua de Debian/Ubuntu base).

---

## 🚀 Cómo Ejecutar la Seguridad de Forma Local

Para que los desarrolladores validen su código antes de subirlo, hemos habilitado un script amigable.

### Paso 1: Instalar herramientas de seguridad
Asegúrate de tener instaladas las librerías de seguridad (ya están en el `requirements.txt` global).
```bash
pip install -r requirements.txt
# O manualmente: pip install bandit safety pre-commit
```

### Paso 2: Activar pre-commit
Esto configura Git para que rechace commits que contengan secretos (tokens, passwords).
```bash
pre-commit install
```

### Paso 3: Ejecutar Escaneo General
Puedes ejecutar nuestro script automatizado para correr `Bandit` y `Safety` con un solo comando:

```bash
# Ejecutar desde la raíz del proyecto
python scripts/security/run_security_scans.py
```
> [!NOTE]
> Este script te dará un resumen rápido si tu código y tus librerías pasan las pruebas de seguridad, ahorrándote tiempo antes de esperar al CI/CD de GitHub.

---

## 📝 Resumen para Perfiles No Técnicos (Management/Product)

**¿Qué significa esto para el negocio?**
- **Confianza:** Podemos garantizar a nuestros clientes o usuarios que nuestra API de predicción de Machine Learning cumple con estándares de seguridad.
- **Ahorro:** Encontramos los errores de seguridad en la etapa de desarrollo ("shift-left"), lo que es 100 veces más barato de arreglar que si lo encontramos cuando el modelo ya está en producción.
- **Automatización:** Los desarrolladores no pierden tiempo revisando vulnerabilidades a mano; el sistema de GitHub Actions lo hace por ellos automáticamente en cada cambio.
