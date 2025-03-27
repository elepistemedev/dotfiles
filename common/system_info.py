import json
from pathlib import Path
import platform
import subprocess

from .logger_utils import setup_logger

logging = setup_logger()

COMMON_DIR = Path(__file__).parent


class SystemInfo:
    def __init__(self):
        self.system = platform.system().lower()
        self.distribution = None
        self.version = None
        self.package_manager = None
        self.update_command = None
        self.install_command = None
        self.repositories = None
        self.dependencies_core = None
        self.dependencies_extended = None

        self.config = self._load_config()

        if self.system == "linux":
            self._detect_linux_distribution()
            self._set_package_manager_from_config()

    def _load_config(self):
        """Carga la configuración desde el archivo JSON."""
        config_path = COMMON_DIR / "installer_config.json"
        try:
            with open(config_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            logging.error(f"No se encontró el archivo de configuración: {config_path}")
            return {}
        except json.JSONDecodeError:
            logging.error(f"Error al decodificar el archivo JSON: {config_path}")
            return {}

    def _detect_linux_distribution(self):
        """Detecta la distribución Linux y su versión"""
        try:
            with open("/etc/os-release") as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith("ID="):
                        self.distribution = line.split("=")[1].strip().strip('"').lower()
                    elif line.startswith("VERSION_ID="):
                        self.version = line.split("=")[1].strip().strip('"')
        except FileNotFoundError:
            try:
                self.distribution = (
                    subprocess.check_output(["lsb_release", "-si"], universal_newlines=True).strip().lower()
                )
                self.version = subprocess.check_output(["lsb_release", "-sr"], universal_newlines=True).strip()
            except (subprocess.CalledProcessError, FileNotFoundError):
                logging.warning("No se pudo detectar la distribución Linux completamente.")
                self.distribution = "unknown"

    def _set_package_manager_from_config(self):
        """Establece el gestor de paquetes y comandos desde la configuración."""
        if (
            self.config
            and "sentu_install" in self.config
            and "package_managers" in self.config["sentu_install"]
            and self.system in self.config["sentu_install"]["package_managers"]
        ):
            system_config = self.config["sentu_install"]["package_managers"][self.system]
            if self.distribution in system_config:
                distro_config = system_config[self.distribution]
                self.package_manager = distro_config.get("manager")
                self.update_command = distro_config.get("update")
                self.install_command = distro_config.get("install")
                self.dependencies_core = distro_config.get("dependencies", {}).get("core", [])
                self.dependencies_extended = distro_config.get("dependencies", {}).get("extended", [])
            else:
                logging.warning(f"No se encontró configuración para la distribución: {self.distribution}")
        else:
            logging.warning(f"No se encontró configuración para el sistema operativo: {self.system}")
