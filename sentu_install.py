import logging
import os
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

# URL por defecto en caso de que no se encuentre en .env (ahora hardcodeada para simplicidad)
DEFAULT_REPO_URL = "https://github.com/elepistemedev/dotfiles/archive/refs/heads/feature/better_man.zip"

RYE_EXECUTABLE = "rye"
REPO_NAME = "dotfiles-feature-better_man"
FINAL_FOLDER_NAME = "dotfiles"


def is_rye_installed() -> bool:
    """Verifica si Rye está instalado en el sistema."""
    try:
        run([RYE_EXECUTABLE, "--version"], check=True, capture_output=True)
        return True
    except FileNotFoundError:
        return False
    except CalledProcessError:
        return False


def install_rye() -> None:
    """Instala Rye en el sistema usando el método recomendado."""
    print("\033[1m\033[94mRye no está instalado. Procediendo con la instalación...\033[0m")
    try:
        install_command = f"curl -sSf https://rye.astral.sh/get | bash"
        print(f"\033[1m\033[92mEjecutando comando para instalar Rye:\033[0m \033[3m{install_command}\033[0m")
        run(install_command, shell=True, check=True)
        print("\033[1m\033[92mInstalación de Rye completada.\033[0m Asegúrate de que esté en tu PATH.")
        print("\n\033[1m\033[91m********************************************************************\033[0m")
        print("\033[1m\033[91m¡Importante! Es posible que necesites cerrar y volver a abrir tu terminal\033[0m")
        print("\033[1m\033[91mpara que Rye esté disponible en tu PATH.\033[0m")
        print("\033[1m\033[91m********************************************************************\033[0m\n")
    except CalledProcessError as e:
        print(f"\033[1m\033[91mError al ejecutar el comando de instalación de Rye:\033[0m \033[1m{e}\033[0m")
        sys.exit(1)
    except Exception as e:
        print("\033[1m\033[91mError inesperado al instalar Rye:\033[0m")
        print(e)
        sys.exit(1)


def download_and_extract(repo_url: str, extract_path: Path) -> Path:
    """Descarga y extrae el repositorio directamente en la ruta especificada."""
    zip_path = extract_path / "repo.zip"
    try:
        print("\033[1m\033[94mDescargando repositorio...\033[0m")
        urllib.request.urlretrieve(repo_url, zip_path)
        print(f"\033[1m\033[92mRepositorio descargado correctamente en:\033[0m \033[3m{zip_path}\033[0m")

        print("\033[1m\033[94mExtrayendo archivos...\033[0m")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_path)
        extracted_path = extract_path
        print(f"\033[1m\033[92mArchivos extraídos correctamente en:\033[0m \033[3m{extracted_path}\033[0m")

        # Verificar si hay un único directorio raíz
        extracted_content = list(extracted_path.iterdir())
        if len(extracted_content) == 1 and extracted_content[0].is_dir():
            return extracted_content[0]  # Retornar el directorio raíz
        else:
            return extracted_path  # Retornar la ruta de extracción si no hay un único directorio raíz
    except URLError as e:
        print(
            f"\033[1m\033[91mError al descargar el repositorio desde\033[0m \033[3m{repo_url}\033[0m: \033[1m{e}\033[0m",
        )
        sys.exit(1)
    except zipfile.BadZipFile:
        print(
            "\033[1m\033[91mEl archivo descargado no es un archivo ZIP válido:\033[0m \033[1m{e}\033[0m",
        )
        sys.exit(1)
    except Exception as e:
        print(
            "\033[1m\033[91mError inesperado al descargar o extraer el repositorio:\033[0m",
        )
        print(e)
        sys.exit(1)

def execute_phase1() -> None:
    """Ejecuta el script de la primera fase desde el directorio de dotfiles."""
    home_path = Path.home()
    final_folder_name = FINAL_FOLDER_NAME
    dotfiles_path = home_path / final_folder_name

    # Verificar si la carpeta dotfiles existe y tiene archivos
    if dotfiles_path.exists():
        # Eliminar archivos dentro de la carpeta si existen
        if dotfiles_path.is_dir():
            for item in dotfiles_path.iterdir():
                if item.is_file():
                    item.unlink()  # Eliminar el archivo
                elif item.is_dir():
                    shutil.rmtree(item)
    else:
        # Si no existe, crearla
        dotfiles_path.mkdir(parents=True, exist_ok=True)

    main_script = dotfiles_path / "phase1" / "main.py"
    project_root = dotfiles_path
    
    if not (main_script).exists():
        print(f"\033[1m\033[91mEl archivo main.py no existe en:\033[0m \033[3m{main_script}\033[0m")
        sys.exit(1)

    print("\033[1m\033[94mEjecutando Fase 1 desde el directorio de dotfiles...\033[0m")
    try:
        # Agregar el directorio raíz del proyecto al PYTHONPATH y ejecutar Fase 1
        env = dict(PYTHONPATH=str(project_root), **os.environ)
        run([sys.executable, str(main_script)], check=True, env=env)
        print("\033[1m\033[92mFase 1 ejecutada correctamente.\033[0m")

    except FileNotFoundError:
        print("\033[1m\033[91mEl ejecutable de Python no se encontró.\033[0m")
        sys.exit(1)
    except CalledProcessError as e:
        print(
            "\033[1m\033[91mError durante la ejecución de Fase 1:\033[0m",
        )
        print(e)
        sys.exit(1)
    except Exception as e:
        print(
            "\033[1m\033[91mError inesperado al ejecutar Fase 1:\033[0m",
        )
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    print("\033[1m\033[94mEjecutando instalación de Fase 1 desde curl...\033[0m")

    # Verificar e instalar Rye si es necesario
    if not is_rye_installed():
        install_rye()
    else:
        print("\033[1m\033[92mRye ya está instalado.\033[0m")

    repo_url_direct = DEFAULT_REPO_URL
    print(f"\033[1m\033[94mUsando URL del repositorio:\033[0m \033[3m{repo_url_direct}\033[0m")

    home_path = Path.home()
    final_folder_name = FINAL_FOLDER_NAME
    temp_dir_direct = Path(tempfile.mkdtemp(prefix="direct_install_"))
    print(f"\033[1m\033[92mExtrayendo temporalmente a:\033[0m \033[3m{temp_dir_direct}\033[0m")
    extracted_path_temp = download_and_extract(repo_url_direct, temp_dir_direct)

    # Mover el contenido a $HOME/dotfiles/
    home_path = Path.home()
    final_folder_name = FINAL_FOLDER_NAME
    destination_path = home_path / final_folder_name

    # Mover el contenido a la carpeta destino
    for item in extracted_path_temp.iterdir():
        if destination_path.exists():
            if item.is_dir():
                shutil.move(str(item), str(destination_path))
            else:
                shutil.move(str(item),str(destination_path))
        else:
            if item.is_dir():
                shutil.move(str(item),str(home_path))
            else:
                shutil.move(str(item),str(home_path))
    os.rename(home_path / REPO_NAME, home_path/FINAL_FOLDER_NAME)
    shutil.rmtree(temp_dir_direct, ignore_errors=True)

    print("\033[1m\033[94mEjecutando Fase 1...\033[0m")
    execute_phase1()
    sys.exit(0)
