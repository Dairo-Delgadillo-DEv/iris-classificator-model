import subprocess
import sys

# Forzar codificación UTF-8 para emojis en consola de Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def run_command(command, description):
    print(f"\n{'='*50}")
    print(f"Ejecutando: {description}")
    print(f"Comando: {' '.join(command)}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print(result.stdout)
        print("✅ PASS")
        return True
    except subprocess.CalledProcessError as e:
        print(e.stdout)
        print(e.stderr)
        print("❌ FAIL")
        return False
    except FileNotFoundError:
        print(f"❌ ERROR: No se encontró el comando '{command[0]}'.")
        print("Asegúrate de haber instalado las dependencias de seguridad (pip install bandit safety pre-commit)")
        return False

def main():
    print("🛡️ Iniciando escaneos de seguridad DevSecOps...")
    
    # 1. Bandit para SAST (Static Application Security Testing)
    # Analizamos el código fuente (src y deployment) excluyendo tests
    bandit_cmd = ["bandit", "-r", "src/", "deployment/api/", "-ll", "-ii"]
    bandit_success = run_command(bandit_cmd, "Bandit (Análisis Estático de Código Python)")
    
    # 2. Safety para SCA (Software Composition Analysis)
    # Analizamos las dependencias en busca de vulnerabilidades conocidas
    safety_cmd = ["safety", "check", "-r", "requirements.txt", "--full-report"]
    safety_success = run_command(safety_cmd, "Safety (Análisis de Dependencias)")
    
    print(f"\n{'='*50}")
    print("🎯 RESUMEN DE SEGURIDAD")
    print(f"{'='*50}")
    print(f"Bandit (Código):      {'✅ PASS' if bandit_success else '❌ FAIL'}")
    print(f"Safety (Dependencias):{'✅ PASS' if safety_success else '❌ FAIL'}")
    
    if not (bandit_success and safety_success):
        print("\n⚠️ Se encontraron problemas de seguridad. Por favor, revísalos antes de hacer commit.")
        sys.exit(1)
    else:
        print("\n✅ ¡Todo seguro! Listo para hacer commit.")
        sys.exit(0)

if __name__ == "__main__":
    main()
