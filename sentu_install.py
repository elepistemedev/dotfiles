import logging
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

DEFAULT_REPO_URL = "https://github.com/elepistemedev/dotfiles/archive/refs/heads/feature/better_man.zip"
RYE_EXECUTABLE = "rye"
FINAL_FOLDER_NAME = "dotfiles"


def is_rye_installed() -> bool:
    """Verifica si Rye está instalado en el sistema."""
    try:
        subprocess.run([RYE_EXECUTABLE, "--version"], check=True, capture_output=True)
        return True
    except FileNotFoundError:
        return False


def install_rye() -> None:
    """Instala Rye en el sistema de manera segura."""
    print("\033[1m\033[94mInstalando Rye...\033[0m")
    try:
        curl_proc = subprocess.run(
            ["curl", "-sSf", "https://rye.astral.sh/get"],
            check=True,
            stdout=subprocess.PIPE,
        )
        subprocess.run(["bash"], input=curl_proc.stdout, check=True)
        print("\033[1m\033[92mInstalación completada.\033[0m")
    except subprocess.CalledProcessError as e:
        print(f"\033[1m\033[91mError instalando Rye:\033[0m {e}")
        sys.exit(1)


def download_and_extract(repo_url: str, extract_path: Path) -> Path:
    """Descarga y extrae un repositorio en la ruta especificada."""
    zip_path = extract_path / "repo.zip"
    try:
        print("\033[1m\033[94mDescargando repositorio...\033[0m")
        urllib.request.urlretrieve(repo_url, zip_path)

        print("\033[1m\033[94mExtrayendo archivos...\033[0m")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_path)

        extracted_content = [item for item in extract_path.iterdir() if item.is_dir()]
        if len(extracted_content) == 1:
            return extracted_content[0]
        return extract_path
    finally:
        zip_path.unlink(missing_ok=True)


def execute_phase1() -> None:
    """Ejecuta la fase 1 del proceso."""
    home_path = Path.home()
    dotfiles_path = home_path / FINAL_FOLDER_NAME

    # Backup antes de eliminar
    backup_path = home_path / f"{FINAL_FOLDER_NAME}_backup"
    if dotfiles_path.exists():
        if backup_path.exists():
            shutil.rmtree(backup_path)
        shutil.copytree(dotfiles_path, backup_path)

        for item in dotfiles_path.iterdir():
            if item.is_file():
                item.unlink()
            else:
                shutil.rmtree(item)

    else:
        dotfiles_path.mkdir(parents=True, exist_ok=True)

    main_script = dotfiles_path / "phase1" / "main.py"
    if not main_script.exists():
        print(f"\033[1m\033[91mNo se encontró:\033[0m {main_script}")
        sys.exit(1)

    print("\033[1m\033[94mEjecutando Fase 1...\033[0m")
    try:
        subprocess.run(
            [sys.executable, str(main_script)], check=True, env={**os.environ, "PYTHONPATH": str(dotfiles_path)}
        )
        print("\033[1m\033[92mFase 1 ejecutada con éxito.\033[0m")
    except subprocess.CalledProcessError as e:
        print(f"\033[1m\033[91mError ejecutando Fase 1:\033[0m {e}")
        sys.exit(1)


if __name__ == "__main__":
    print("\033[1m\033[94mIniciando instalación...\033[0m")

    if not is_rye_installed():
        install_rye()

    temp_dir = Path(tempfile.mkdtemp(prefix="direct_install_"))
    extracted_path = download_and_extract(DEFAULT_REPO_URL, temp_dir)

    destination_path = Path.home() / FINAL_FOLDER_NAME
    for item in extracted_path.iterdir():
        if not (destination_path / item.name).exists():
            shutil.move(str(item), str(destination_path))

    shutil.rmtree(temp_dir, ignore_errors=True)
    execute_phase1()
