import sys
import urllib.request
import zipfile
import tempfile
import shutil
from subprocess import run
from pathlib import Path

# URL del repositorio en formato ZIP
REPO_URL = "https://github.com/elepistemedev/dotfiles/archive/refs/heads/dev.zip"


def download_and_extract(repo_url, temp_dir):
    """Descarga y extrae el repositorio en un directorio temporal."""
    zip_path = temp_dir / "repo.zip"
    try:
        print("Descargando repositorio...")
        urllib.request.urlretrieve(repo_url, zip_path)
        print("Repositorio descargado correctamente.")

        print("Extrayendo archivos...")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(temp_dir)
        extracted_path = temp_dir / "dev"
        return extracted_path
    except Exception as e:
        print(f"Error al descargar o extraer el repositorio: {e}")
        sys.exit(1)


def execute_phase1(temp_dir):
    """Ejecuta el script de la primera fase desde el directorio temporal."""
    main_script = temp_dir / "src" / "phase1" / "main.py"
    if main_script.exists():
        print("Ejecutando Fase 1 desde el directorio temporal...")
        try:
            run([sys.executable, str(main_script)], check=True)
        except Exception as e:
            print(f"Error al ejecutar Fase 1: {e}")
            sys.exit(1)
    else:
        print("El archivo main.py no existe en el directorio temporal.")
        sys.exit(1)


def main():
    print("Iniciando instalación y configuración...")
    temp_dir = Path(tempfile.mkdtemp(prefix="bootstrap_phase1_"))
    print(f"Directorio temporal creado: {temp_dir}")

    try:
        # Paso 1: Descargar y extraer el repositorio
        extracted_path = download_and_extract(REPO_URL, temp_dir)

        # Paso 2: Ejecutar la primera fase
        execute_phase1(extracted_path)

    finally:
        # Limpieza del directorio temporal
        print(f"Limpiando el directorio temporal: {temp_dir}")
        # shutil.rmtree(temp_dir, ignore_errors=True)
        print("Directorio temporal eliminado. Proceso completado.")


if __name__ == "__main__":
    main()
