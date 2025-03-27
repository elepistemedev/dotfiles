import logging
from pathlib import Path
import shutil
import subprocess
from subprocess import CalledProcessError, run
import sys
import tempfile
from urllib.error import URLError
import urllib.request
import zipfile

# Configuración básica del logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# URL del repositorio a descargar
DEFAULT_REPO_URL = "https://github.com/elepistemedev/dotfiles/archive/refs/heads/feature/better_man.zip"

# Nombre del directorio final donde se ubicarán los dotfiles
FINAL_FOLDER_NAME = "dotfiles"

# Ejecutable de Rye
RYE_EXECUTABLE = "rye"


def is_rye_installed() -> bool:
    """Verifica si Rye está instalado en el sistema."""
    try:
        run([RYE_EXECUTABLE, "--version"], check=True, capture_output=True)
        return True
    except (FileNotFoundError, CalledProcessError):
        return False


def install_rye() -> None:
    """Instala Rye en el sistema usando el método recomendado."""
    logging.info("Rye no está instalado. Procediendo con la instalación...")
    try:
        install_command = "curl -sSf https://rye.astral.sh/get | bash"
        logging.info(f"Ejecutando comando para instalar Rye: {install_command}")
        run(install_command, shell=True, check=True)
        logging.info("Instalación de Rye completada. Asegúrate de que esté en tu PATH.")
        logging.info(
            "Es posible que necesites cerrar y volver a abrir tu terminal para que Rye esté disponible en tu PATH."
        )
        # Source Rye's environment
        source_command = f'source "$HOME/.rye/env"'
        logging.info(
            f"\033[1m\033[92mEjecutando comando para agregar Rye al PATH:\033[0m \033[3m{source_command}\033[0m"
        )
        run(source_command, shell=True, check=True, executable="/bin/bash")
    except CalledProcessError as e:
        logging.error(f"Error al ejecutar el comando de instalación de Rye: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Error inesperado al instalar Rye: {e}")
        sys.exit(1)


def download_and_extract(repo_url: str, extract_path: Path) -> Path:
    """Descarga y extrae el repositorio en la ruta especificada."""
    zip_path = extract_path / "repo.zip"
    try:
        logging.info(f"Descargando el repositorio desde {repo_url}...")
        urllib.request.urlretrieve(repo_url, zip_path)
        logging.info(f"Repositorio descargado correctamente en: {zip_path}")

        logging.info("Extrayendo archivos...")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_path)
        logging.info(f"Archivos extraídos en: {extract_path}")

        # Identificar el directorio raíz extraído
        extracted_dirs = [d for d in extract_path.iterdir() if d.is_dir()]
        if len(extracted_dirs) == 1:
            return extracted_dirs[0]
        else:
            logging.error("No se pudo identificar un único directorio raíz en el archivo ZIP extraído.")
            sys.exit(1)

    except URLError as e:
        logging.error(f"Error al descargar el repositorio desde {repo_url}: {e}")
        sys.exit(1)
    except zipfile.BadZipFile:
        logging.error("El archivo descargado no es un archivo ZIP válido.")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Error inesperado durante la descarga o extracción del repositorio: {e}")
        sys.exit(1)


def move_contents(source: Path, destination: Path) -> None:
    """Mueve el contenido del directorio fuente al directorio destino."""
    try:
        if not destination.exists():
            destination.mkdir(parents=True)
        for item in source.iterdir():
            target = destination / item.name
            if item.is_dir():
                if target.exists():
                    shutil.rmtree(target)
                shutil.move(str(item), str(target))
            else:
                if target.exists():
                    target.unlink()
                shutil.move(str(item), str(target))
        logging.info(f"Contenido movido de {source} a {destination}")
    except Exception as e:
        logging.error(f"Error al mover contenido: {e}")
        sys.exit(1)


def execute_phase1(dotfiles_path: Path) -> None:
    """Ejecuta el script de la primera fase desde el directorio de dotfiles."""
    home_path = Path.home()
    final_folder_name = FINAL_FOLDER_NAME
    dotfiles_path = home_path / final_folder_name
    if dotfiles_path.exists():
        for item in dotfiles_path.iterdir():
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
    else:
        dotfiles_path.mkdir(parents=True, exist_ok=True)

    main_script = dotfiles_path / "phase1" / "main.py"
    project_root = dotfiles_path
    if not main_script.exists():
        logging.error(f"El archivo main.py no existe en: {main_script}")
        sys.exit(1)

    logging.info("Ejecutando Fase 1 desde el directorio de dotfiles...")
    try:
        env = dict(PYTHONPATH=str(project_root), **os.environ)
        command = [RYE_EXECUTABLE, "run", "python", str(main_script)]
        run(command, check=True, env=env)
        logging.info("Fase 1 ejecutada correctamente.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error durante la ejecución de Fase 1: {e}")
        sys.exit(1)


if __name__ == "__main__":
    logging.info("Iniciando instalación de Fase 1 desde curl...")

    # Verificar e instalar Rye si es necesario
    if not is_rye_installed():
        install_rye()
    else:
        logging.info("Rye ya está instalado.")

    repo_url = DEFAULT_REPO_URL
    logging.info(f"Usando URL del repositorio: {repo_url}")

    home_path = Path.home()
    dotfiles_path = home_path / FINAL_FOLDER_NAME

    # Crear un directorio temporal para la descarga y extracción
    with tempfile.TemporaryDirectory(prefix="direct_install_") as temp_dir:
        temp_path = Path(temp_dir)
        extracted_path = download_and_extract(repo_url, temp_path)

        # Mover el contenido extraído al directorio final de dotfiles
        move_contents(extracted_path, dotfiles_path)

    # Ejecutar la Fase 1
    execute_phase1(dotfiles_path)
    logging.info("Proceso completado.")
