import subprocess
from typing import Optional

from common.logger_utils import setup_logger
from common.system_info import SystemInfo

logger = setup_logger()


class FlatpakInstaller:
    """Módulo para gestionar la instalación de Flatpak en diferentes distribuciones Linux."""

    def __init__(self, system_info: SystemInfo):
        self.system_info = system_info
        self.installation_commands = {
            "apt": ["apt", "install", "-y", "flatpak", "gnome-software-plugin-flatpak"],
            "dnf": ["dnf", "install", "-y", "flatpak"],
            "pacman": ["pacman", "-S", "--noconfirm", "flatpak"],
            "zypper": ["zypper", "install", "-y", "flatpak"],
            "emerge": ["emerge", "sys-apps/flatpak"],
        }

    def _run_command(self, command: list[str]) -> tuple[bool, Optional[str]]:
        """Ejecuta un comando y retorna el resultado y cualquier error."""
        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
            return True, None
        except subprocess.CalledProcessError as e:
            return False, str(e.stderr)

    def _add_flathub_repo(self) -> tuple[bool, Optional[str]]:
        """Añade el repositorio Flathub."""
        command = [
            "flatpak",
            "remote-add",
            "--if-not-exists",
            "flathub",
            "https://flathub.org/repo/flathub.flatpakrepo",
        ]
        return self._run_command(command)

    def is_flatpak_installed(self) -> bool:
        """Verifica si Flatpak ya está instalado."""
        try:
            subprocess.run(["flatpak", "--version"], check=True, capture_output=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def install(self) -> bool:
        """Instala Flatpak y configura el repositorio Flathub."""
        if self.is_flatpak_installed():
            logger.info("Flatpak ya está instalado en el sistema.")
            success, error = self._add_flathub_repo()
            if not success:
                logger.error(f"Error al añadir repositorio Flathub: {error}")
            return success

        package_manager = self.system_info.package_manager
        if package_manager not in self.installation_commands:
            logger.error(f"Gestor de paquetes '{package_manager}' no soportado para instalar Flatpak")
            return False

        # Instalar Flatpak
        logger.info(f"Instalando Flatpak usando {package_manager}...")
        success, error = self._run_command(self.installation_commands[package_manager])
        if not success:
            logger.error(f"Error instalando Flatpak: {error}")
            return False

        # Añadir repositorio Flathub
        logger.info("Añadiendo repositorio Flathub...")
        success, error = self._add_flathub_repo()
        if not success:
            logger.error(f"Error al añadir repositorio Flathub: {error}")
            return False

        logger.info("Flatpak instalado y configurado exitosamente")
        return True


# Ejemplo de uso
def install_flatpak(system_info: SystemInfo) -> bool:
    """Función auxiliar para instalar Flatpak usando el instalador."""
    installer = FlatpakInstaller(system_info)
    return installer.install()
