# BUG: Eliminar este archivo
import os
import sys
import subprocess
import logging
import platform
from pathlib import Path
import urllib.request


# INFO: Listo en logger_utils.py
def setup_logger():
    logger = logging.getLogger("Bootstrap")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s: %(message)s", datefmt="%H:%M:%S"
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


logger = setup_logger()


# INFO: Listo en system_info.py
class SystemInfo:
    def __init__(self):
        self.system = platform.system().lower()
        self.distribution = None
        self.version = None
        self.package_manager = None
        self.update_command = None
        self.install_command = None

        if self.system == "linux":
            self._detect_linux_distribution()
            self._set_package_manager()

    def _detect_linux_distribution(self):
        """Detecta la distribución Linux y su versión"""
        try:
            with open("/etc/os-release") as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith("ID="):
                        self.distribution = (
                            line.split("=")[1].strip().strip('"').lower()
                        )
                    elif line.startswith("VERSION_ID="):
                        self.version = line.split("=")[1].strip().strip('"')
        except FileNotFoundError:
            try:
                self.distribution = (
                    subprocess.check_output(
                        ["lsb_release", "-si"], universal_newlines=True
                    )
                    .strip()
                    .lower()
                )
                self.version = subprocess.check_output(
                    ["lsb_release", "-sr"], universal_newlines=True
                ).strip()
            except (subprocess.CalledProcessError, FileNotFoundError):
                logger.error("No se pudo detectar la distribución Linux")

    def _set_package_manager(self):
        """Configura el gestor de paquetes y sus comandos"""
        package_managers = {
            "debian": {
                "manager": "apt",
                "update": ["sudo", "apt-get", "update"],
                "install": ["sudo", "apt-get", "install", "-y"],
            },
            "ubuntu": {
                "manager": "apt",
                "update": ["sudo", "apt-get", "update"],
                "install": ["sudo", "apt-get", "install", "-y"],
            },
            "fedora": {
                "manager": "dnf",
                "update": ["sudo", "dnf", "check-update"],
                "install": ["sudo", "dnf", "install", "-y"],
            },
            "centos": {
                "manager": "yum",
                "update": ["sudo", "yum", "check-update"],
                "install": ["sudo", "yum", "install", "-y"],
            },
            "arch": {
                "manager": "pacman",
                "update": ["sudo", "pacman", "-Sy"],
                "install": ["sudo", "pacman", "-S", "--noconfirm"],
            },
            "manjaro": {
                "manager": "pacman",
                "update": ["sudo", "pacman", "-Sy"],
                "install": ["sudo", "pacman", "-S", "--noconfirm"],
            },
        }

        if self.distribution in package_managers:
            pm_info = package_managers[self.distribution]
            self.package_manager = pm_info["manager"]
            self.update_command = pm_info["update"]
            self.install_command = pm_info["install"]


# INFO: Listo en system_operations.py
def update_system(system_info):
    """Actualiza el sistema usando el gestor de paquetes correspondiente"""
    if not system_info.update_command:
        logger.error("No se pudo determinar el comando de actualización")
        return False

    try:
        logger.info(f"Actualizando el sistema usando {system_info.package_manager}...")
        result = subprocess.run(
            system_info.update_command, capture_output=True, text=True
        )

        # Manejar códigos de retorno especiales
        if result.returncode == 0 or (
            system_info.package_manager in ["dnf", "yum"] and result.returncode == 100
        ):
            logger.info("Sistema actualizado correctamente")
            return True
        else:
            logger.error(f"Error actualizando el sistema: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"Error durante la actualización: {str(e)}")
        return False


def clone_repo():
    """Clona el repositorio desde github en la carpeta home del usuario"""
    repo_url = "https://github.com/elepistemedev/dotfiles.git"
    home_dir = str(Path.home())
    repo_path = os.path.join(home_dir, "dotfiles")

    try:
        logger.info(f"Clonando repositorio dotfiles en {home_dir}...")
        subprocess.run(["git", "clone", repo_url, repo_path], check=True)
        logger.info("Repositorio clonado correctamente")
        return True
    except Exception as e:
        logger.error(f"Error clonando repositorio desde github: {str(e)}")
        return False


# INFO: Listo en system_operations.py
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
    ]  # apt-getgar más dependencias según necesites

    if not system_info.install_command:
        logger.error("No se pudo determinar el comando de instalación")
        return False

    try:
        for dep in dependencies:
            logger.info(f"Instalando {dep}...")
            cmd = system_info.install_command + [dep]
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode != 0:
                logger.error(f"Error instalando {dep}: {result.stderr}")
                return False

        logger.info("Todas las dependencias fueron instaladas correctamente")
        return True
    except Exception as e:
        logger.error(f"Error instalando dependencias: {str(e)}")
        return False


# BUG: Falta
def install_and_configure_zsh():
    """Configurando zsh como shell por defecto"""

    try:
        # Cambiar shell por defecto a zsh
        logger.info("Configurando zsh como shell por defecto...")
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

        logger.info("zsh instalado y configurado correctamente")
        return True
    except Exception as e:
        logger.error(f"Error instalando/configurando zsh: {str(e)}")
        return False


# BUG: Falta
def setup_anaconda():
    """Descarga e instala Anaconda"""
    anaconda_url = (
        "https://repo.anaconda.com/archive/Anaconda3-2023.09-0-Linux-x86_64.sh"
    )
    installer_path = Path.home() / "anaconda_installer.sh"
    anaconda_path = Path.home() / "anaconda3"

    if anaconda_path.exists():
        logger.info("Anaconda ya está instalado")
        return True

    try:
        # Descargar Anaconda
        logger.info("Descargando Anaconda...")
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
        logger.info("Instalando Anaconda...")
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

        logger.info("Anaconda instalado correctamente")
        return True

    except Exception as e:
        logger.error(f"Error instalando Anaconda: {str(e)}")
        if installer_path.exists():
            installer_path.unlink()
        return False


# BUG: Falta
def install_python_packages():
    """Instala los paquetes Python necesarios para la fase 2"""
    packages = ["rich", "questionary", "typer", "tqdm"]
    anaconda_pip = str(Path.home() / "anaconda3" / "bin" / "pip")

    try:
        # Actualizar pip
        logger.info("Actualizando pip...")
        subprocess.run([anaconda_pip, "install", "--upgrade", "pip"], check=True)

        # Instalar paquetes
        for package in packages:
            logger.info(f"Instalando {package}...")
            result = subprocess.run(
                [anaconda_pip, "install", package], capture_output=True, text=True
            )
            if result.returncode != 0:
                raise Exception(f"Error instalando {package}: {result.stderr}")

        logger.info("Todos los paquetes Python han sido instalados")
        return True
    except Exception as e:
        logger.error(f"Error instalando paquetes Python: {str(e)}")
        return False


def main():
    logger.info("Iniciando fase 1 (Bootstrap)...")

    # INFO: 1. Detectar sistema operativo
    system_info = SystemInfo()
    logger.info(f"Sistema detectado: {system_info.system}")
    if system_info.distribution:
        logger.info(f"Distribución: {system_info.distribution} {system_info.version}")
        logger.info(f"Gestor de paquetes: {system_info.package_manager}")

    # INFO: 2. Actualizar sistema
    if not update_system(system_info):
        logger.error("No se pudo actualizar el sistema")
        sys.exit(1)

    # INFO: 3. Instalar dependencias básicas
    if not install_dependencies(system_info):
        logger.error("No se pudieron instalar las dependencias")
        sys.exit(1)

    # BUG: 4. Instalar y configurar zsh
    if not install_and_configure_zsh():
        logger.error("No se pudo instalar/configurar zsh")
        sys.exit(1)

    # BUG: 5. Clonar repositorio desde github
    if not clone_repo():
        logger.error("No se pudo clonar el repositorio desde github")
        sys.exit(1)

    # BUG:: 6. Instalar Anaconda
    if not setup_anaconda():
        logger.error("No se pudo instalar Anaconda")
        sys.exit(1)

    # BUG: 7. Instalar paquetes Python necesarios
    if not install_python_packages():
        logger.error("No se pudieron instalar los paquetes Python")
        sys.exit(1)

    logger.info("\n=== Fase 1 completada exitosamente ===")
    logger.info("\nPara continuar con la fase 2:")
    logger.info("1. Cierra y vuelve a abrir la terminal")
    logger.info("2. Ejecuta:")
    logger.info("   cd ~/dotfiles")
    logger.info("   python scripts/phase2.py")


if __name__ == "__main__":
    main()
