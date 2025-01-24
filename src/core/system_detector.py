import logging
import platform
import subprocess

from src.core.package_config_loader import PackageManagerConfigLoader

logging = logging.getLogger(__name__)


class SystemInfo:
    """
    Clase para recopilar información detallada del sistema operativo.

    Attributes:
        system (str): Nombre del sistema operativo en minúsculas.
        distribution (Optional[str]): Nombre de la distribución Linux.
        version (Optional[str]): Versión del sistema operativo.
        package_manager (Optional[str]): Gestor de paquetes detectado.
        update_command (Optional[List[str]]): Comando para actualizar paquetes.
        install_command (Optional[List[str]]): Comando para instalar paquetes.
        repositories (Optional[Dict[str, List[str]]]): Repositorios adicionales.
        dependencies_core (Optional[List[str]]): Dependencias esenciales.
        dependencies_extended (Optional[List[str]]): Dependencias extendidas.
    """

    def __init__(self):
        """
        Inicializa la información del sistema, detectando detalles específicos para Linux.
        """
        self.system = platform.system().lower()
        self.distribution = None
        self.version = None
        self.package_manager = None
        self.update_command = None
        self.install_command = None
        self.repositories = None
        self.dependencies_core = []
        self.dependencies_extended = []

        if self.system == "linux":
            self._detect_linux_distribution()
            self._set_package_manager()

    def _detect_linux_distribution(self):
        """
        Detecta la distribución Linux y su versión.

        Intenta obtener la información desde /etc/os-release.
        Si falla, utiliza el comando lsb_release como respaldo.
        Registra un error si no puede detectar la distribución.
        """
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
                logging.error("No se pudo detectar la distribución Linux")

    def _set_package_manager(self):
        """
        Configura el gestor de paquetes y sus comandos para la distribución Linux detectada.

        Establece atributos como package_manager, update_command, install_command,
        repositories, y dependencias basado en la distribución Linux.
        """
        config = PackageManagerConfigLoader.get_config(str(self.distribution))
        if config:
            self.package_manager = config.get("manager")
            self.update_command = config.get("update_command", [])

            self.install_command = config.get("install_command", [])
            self.repositories = config.get("repositories", {})
            self.dependencies_core = config.get("dependencies", {}).get("core", [])
            self.dependencies_extended = config.get("dependencies", {}).get("extended", [])


# if __name__ == "__main__":
#     print("\n=== Prueba de detección del sistema ===")
#     system_info = SystemInfo()
#
#     # Imprimir información recolectada
#     print(f"Sistema operativo: {system_info.system}")
#     print(f"Distribución Linux: {system_info.distribution}")
#     print(f"Versión: {system_info.version}")
#     print(f"Gestor de paquetes: {system_info.package_manager}")
#     print(f"Comando actualización: {system_info.update_command}")
#     print(f"Comando instalación: {system_info.install_command}")
#     print(f"Repositorios: {system_info.repositories}")
#     print(f"Dependencias base: {system_info.dependencies_core}")
#     print(f"Dependencias extendidas: {system_info.dependencies_extended}")
