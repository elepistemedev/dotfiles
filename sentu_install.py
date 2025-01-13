import sys
import urllib.request
import zipfile
import tempfile
import shutil
from subprocess import run
from pathlib import Path
import os

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
        extracted_path = temp_dir
        return extracted_path
    except Exception as e:
        print(f"Error al descargar o extraer el repositorio: {e}")
        sys.exit(1)


def execute_phase1(temp_dir):
    """Ejecuta el script de la primera fase desde el directorio temporal."""
    main_script = temp_dir / "dotfiles-dev" / "phase1" / "main.py"
    project_root = temp_dir / "dotfiles-dev"

    print(f"Archivo main.py está en: {str(main_script)}")
    if main_script.exists():
        print("Ejecutando Fase 1 desde el directorio temporal...")
        try:
            # Agregar el directorio raíz del proyecto al PYTHONPATH
            env = dict(PYTHONPATH=str(project_root), **os.environ)

            run([sys.executable, str(main_script)], check=True, env=env)
        except Exception as e:
            print(f"Error al ejecutar Fase 1: {e}")
            sys.exit(1)
    else:
        print("El archivo main.py no existe en el directorio temporal.")
        sys.exit(1)


def execute_phase2(temp_dir, conda_path, env_name):
    """
    Ejecuta el script de la segunda fase desde el directorio temporal usando Anaconda.

    Args:
        temp_dir (Path): Ruta al directorio temporal donde está el proyecto.
        conda_path (str): Ruta al directorio 'bin' o 'Scripts' de Anaconda.
        env_name (str): Nombre del entorno virtual de Anaconda a usar.
    """
    main_script = temp_dir / "dotfiles-dev" / "phase2" / "main.py"
    project_root = temp_dir / "dotfiles-dev"

    print(f"Archivo main.py está en: {str(main_script)}")
    if main_script.exists():
        print("Ejecutando Fase 2 desde el directorio temporal usando Anaconda...")
        try:
            # Comando para activar el entorno y ejecutar el script
            activation_cmd = (
                f"{os.path.join(conda_path, 'conda')} run -n {env_name} "
                f"{sys.executable} {str(main_script)}"
            )

            # Agregar el directorio raíz del proyecto al PYTHONPATH
            env = dict(PYTHONPATH=str(project_root), **os.environ)

            run(activation_cmd, shell=True, check=True, env=env)
        except Exception as e:
            print(f"Error al ejecutar Fase 2: {e}")
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

        # temp_dir = Path("/ruta/al/directorio/temporal")  # Cambia por tu ruta
        anaconda_path = Path.home() / "anaconda3"
        conda_path = (
            f"{str(anaconda_path)}/bin"  # Cambia según la instalación de Anaconda
        )
        env_name = "base"  # Nombre del entorno creado en la Fase 1

        # Ejecutar la Fase 2
        execute_phase2(temp_dir, conda_path, env_name)

    finally:
        # Limpieza del directorio temporal
        print(f"Limpiando el directorio temporal: {temp_dir}")
        shutil.rmtree(temp_dir, ignore_errors=True)
        print("Directorio temporal eliminado. Proceso completado.")


if __name__ == "__main__":
    main()
