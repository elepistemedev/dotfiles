import subprocess
from logger_utils import setup_logger

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
