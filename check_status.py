#!/usr/bin/env python
"""
Iris MLOps Project - STATUS CHECK
Ejecuta este script para ver el estado del proyecto
"""

import os
from pathlib import Path

def check_project_status():
    """Verifica el estado del proyecto"""
    
    base_path = Path(__file__).parent
    
    print("\n" + "="*60)
    print("  🌸 IRIS MLOPS PROJECT - STATUS CHECK")
    print("="*60 + "\n")
    
    # Archivos que deberían existir
    required_files = {
        "✅ COMPLETADOS": [
            "main.py",
            "predict_example.py",
            "requirements.txt",
            "setup.py",
            ".gitignore",
            "config/config.yaml",
            "src/data/load_data.py",
            "src/models/train.py",
            "src/utils/logger.py",
            "README.md",
            "MLOPS_GUIDE.md",
            "QUICKSTART.md",
            "RESPUESTAS.md",
            "ESTRUCTURA_COMPLETA.md",
            "DIAGRAMAS.md",
            "RESUMEN_EJECUTIVO.md",
            "ÍNDICE_DOCUMENTACIÓN.md",
        ],
        "🔧 POR COMPLETAR": [
            "deployment/api/app.py",
            "deployment/api/wsgi.py",
            "deployment/docker/Dockerfile",
            "deployment/docker/docker-compose.yml",
            "deployment/kubernetes/deployment.yaml",
            "deployment/kubernetes/service.yaml",
            "deployment/kubernetes/configmap.yaml",
            "tests/test_model.py",
            "notebooks/01_eda.ipynb",
            "notebooks/02_training.ipynb",
        ]
    }
    
    # Chequear completados
    print("✅ ARCHIVOS COMPLETADOS:\n")
    completed_count = 0
    for file in required_files["✅ COMPLETADOS"]:
        file_path = base_path / file
        exists = file_path.exists()
        status = "✅" if exists else "❌"
        print(f"  {status} {file}")
        if exists:
            completed_count += 1
    
    # Chequear por completar
    print("\n🔧 ARCHIVOS POR COMPLETAR (TODO):\n")
    todo_count = 0
    for file in required_files["🔧 POR COMPLETAR"]:
        file_path = base_path / file
        exists = file_path.exists()
        size = file_path.stat().st_size if exists else 0
        
        if exists and size < 200:
            status = "📝"
            print(f"  {status} {file} (plantilla lista)")
            todo_count += 1
        elif not exists:
            status = "❌"
            print(f"  {status} {file}")
    
    # Resumen
    print("\n" + "="*60)
    print(f"  ✅ COMPLETADOS: {completed_count}/{len(required_files['✅ COMPLETADOS'])}")
    print(f"  🔧 POR HACER: {len(required_files['🔧 POR COMPLETAR'])} tareas")
    print("="*60 + "\n")
    
    # Instrucciones
    print("📚 PRÓXIMOS PASOS:\n")
    print("  1. Abre: QUICKSTART.md")
    print("  2. Ejecuta: python main.py")
    print("  3. Lee: MLOPS_GUIDE.md")
    print("  4. Implementa: deployment/api/app.py")
    print("  5. Crea: deployment/docker/Dockerfile")
    print("  6. Configura: deployment/kubernetes/")
    print("  7. Sube a GitHub: git push\n")
    
    print("📖 DOCUMENTACIÓN DISPONIBLE:\n")
    print("  - QUICKSTART.md ................ Inicio rápido (5 min)")
    print("  - README.md ................... Descripción (15 min)")
    print("  - MLOPS_GUIDE.md .............. Guía completa (45 min) ⭐")
    print("  - RESPUESTAS.md ............... Tus preguntas (20 min)")
    print("  - ESTRUCTURA_COMPLETA.md ...... Mapa proyecto (20 min)")
    print("  - DIAGRAMAS.md ................ Visuales (15 min)")
    print("  - RESUMEN_EJECUTIVO.md ........ Resumen (10 min)")
    print("  - ÍNDICE_DOCUMENTACIÓN.md ..... Índice de docs\n")
    
    print("🎯 ENTRENAMIENTO DEL MODELO:\n")
    print("  Accuracy Esperada: 96.7%")
    print("  Dataset: Iris Flowers (150 muestras)")
    print("  Algoritmo: Random Forest (100 árboles)")
    print("  Características: 4 numéricas")
    print("  Clases: 3 especies\n")
    
    print("=" * 60)
    print("  ¡Tu proyecto está listo para empezar!")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    check_project_status()
