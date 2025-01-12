import subprocess
from common.logger_utils import setup_logger
import os
from pathlib import Path
import urllib.request
import sys

logging = setup_logger()


def update_system(system_info):
    """Actualiza el sistema usando el gestor de paquetes correspondiente"""
    if not system_info.update_command:
        logging.error("No se pudo determinar el comando de actualización")
        return False

    try:
        logging.info(f"Actualizando el sistema usando {system_info.package_manager}...")
        result = subprocess.run(
            system_info.update_command, capture_output=True, text=True
        )

        if result.returncode == 0 or (
            system_info.package_manager in ["dnf", "yum"] and result.returncode == 100
        ):
            logging.info("Sistema actualizado correctamente")
            return True
        else:
            logging.error(f"Error actualizando el sistema: {result.stderr}")
            return False
    except Exception as e:
        logging.error(f"Error durante la actualización: {str(e)}")
        return False


def install_dependencies(system_info):
    """Instala las dependencias necesarias"""
    dependencies = [
        "git",
        "curl",
        "wget",
        "gcc",
        "make",
        "git",
        "ripgrep",
        "fd-find",
        "unzip",
        "neovim",
        "zsh",
        "fastfetch",
    ]

    if not system_info.install_command:
        logging.error("No se pudo determinar el comando de instalación")
        return False

    try:
        for dep in dependencies:
            logging.info(f"Instalando {dep}...")
            cmd = system_info.install_command + [dep]
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode != 0:
                logging.error(f"Error instalando {dep}: {result.stderr}")
                return False

        logging.info("Todas las dependencias fueron instaladas correctamente")
        return True
    except Exception as e:
        logging.error(f"Error instalando dependencias: {str(e)}")
        return False


def install_and_configure_zsh():
    """Configurando zsh como shell por defecto"""

    try:
        # Cambiar shell por defecto a zsh
        logging.info("Configurando zsh como shell por defecto...")
        user_name = os.getenv("USER")
        result = subprocess.run(
            ["sudo", "chsh", "-s", "/bin/zsh", str(user_name)],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise Exception(
                f"Error configurando zsh como shell por defecto: {result.stderr}"
            )

        logging.info("zsh instalado y configurado correctamente")
        return True
    except Exception as e:
        logging.error(f"Error instalando/configurando zsh: {str(e)}")
        return False


def clone_repo():
    """Clona el repositorio desde github en la carpeta home del usuario"""
    repo_url = "https://github.com/elepistemedev/dotfiles.git"
    home_dir = str(Path.home())
    repo_path = os.path.join(home_dir, "dotfiles")

    try:
        logging.info(f"Clonando repositorio dotfiles en {home_dir}...")
        subprocess.run(["git", "clone", "-b", "dev", repo_url, repo_path], check=True)
        logging.info("Repositorio clonado correctamente")
        return True
    except Exception as e:
        logging.error(f"Error clonando repositorio desde github: {str(e)}")
        return False


def setup_anaconda():
    """Descarga e instala Anaconda"""
    anaconda_url = (
        "https://repo.anaconda.com/archive/Anaconda3-2024.10-1-Linux-x86_64.sh"
    )
    installer_path = Path.home() / "anaconda_installer.sh"
    anaconda_path = Path.home() / "anaconda3"

    if anaconda_path.exists():
        logging.info("Anaconda ya está instalado")
        return True

    try:
        # Descargar Anaconda
        logging.info("Descargando Anaconda...")
        with urllib.request.urlopen(anaconda_url) as response:
            total_size = int(response.headers.get("Content-Length", 0))
            block_size = 8192
            downloaded = 0

            with open(installer_path, "wb") as file:
                while True:
                    buffer = response.read(block_size)
                    if not buffer:
                        break

                    downloaded += len(buffer)
                    file.write(buffer)

                    if total_size:
                        progress = int(50 * downloaded / total_size)
                        sys.stdout.write(
                            f"\rDescargando: [{'=' * progress}{' ' * (50 - progress)}] {downloaded}/{total_size} bytes"
                        )
                        sys.stdout.flush()

        print()  # Nueva línea después de la barra de progreso

        # Instalar Anaconda
        logging.info("Instalando Anaconda...")
        os.chmod(installer_path, 0o755)
        result = subprocess.run(
            ["bash", str(installer_path), "-b", "-p", str(anaconda_path)],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise Exception(result.stderr)

        # Limpiar instalador
        installer_path.unlink()

        # Configurar PATH en .zshrc en lugar de .bashrc
        zshrc_path = Path.home() / ".zshrc"
        with open(zshrc_path, "a") as zshrc:
            zshrc.write("\n# Anaconda3 PATH\n")
            zshrc.write(f'export PATH="{anaconda_path}/bin:$PATH"\n')

        logging.info("Anaconda instalado correctamente")
        return True

    except Exception as e:
        logging.error(f"Error instalando Anaconda: {str(e)}")
        if installer_path.exists():
            installer_path.unlink()
        return False


def install_python_packages():
    """Instala los paquetes Python necesarios para la fase 2"""
    packages = ["rich", "questionary", "typer", "tqdm"]
    anaconda_pip = str(Path.home() / "anaconda3" / "bin" / "pip")

    try:
        # Actualizar pip
        logging.info("Actualizando pip...")
        subprocess.run([anaconda_pip, "install", "--upgrade", "pip"], check=True)

        # Instalar paquetes
        for package in packages:
            logging.info(f"Instalando {package}...")
            result = subprocess.run(
                [anaconda_pip, "install", package], capture_output=True, text=True
            )
            if result.returncode != 0:
                raise Exception(f"Error instalando {package}: {result.stderr}")

        logging.info("Todos los paquetes Python han sido instalados")
        return True
    except Exception as e:
        logging.error(f"Error instalando paquetes Python: {str(e)}")
        return False


def install_prompt():
    """Instala el prompt starship"""
    anaconda_pip = str(Path.home() / "anaconda3" / "bin" / "conda")
    try:
        logging.info("Instalando el prompt Starship...")
        subprocess.run(
            [anaconda_pip, "install", "-c", "conda-forge", "starship"], check=True
        )

        # Configurar PATH en .zshrc
        zshrc_path = Path.home() / ".zshrc"
        with open(zshrc_path, "a") as zshrc:
            zshrc.write("\n# Starship Prompt\n")
            zshrc.write('eval "$(starship init zsh)"\n')

        logging.info("Prompt Startship instalado correctamente")
        return True
    except Exception as e:
        logging.error(f"Error instalando el prompt Starship: {str(e)}")
        return False
