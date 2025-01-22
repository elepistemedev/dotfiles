import logging
import subprocess

# Configurar logging básico (puedes personalizar según sea necesario)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def install_packages(
    commands,
    start_message="Instalando paquetes...",
    success_message="Paquetes instalados correctamente",
    error_message="Se instalaron los paquetes con algunos errores",
):
    """
    Instala una lista de paquetes usando comandos de terminal.

    Args:
        commands (list of tuples): Lista de comandos y descripciones [(cmd, description), ...].
        start_message (str): Mensaje inicial antes de comenzar la instalación.
        success_message (str): Mensaje al completar la instalación sin errores.
        error_message (str): Mensaje al completar la instalación con errores.

    Returns:
        bool: True si todos los paquetes se instalaron correctamente, False en caso de errores.
    """
    success = True
    logging.info(start_message)

    for cmd, description in commands:
        try:
            subprocess.run(cmd, shell=True, check=True)
            logging.info(f"✓ Instalado {description}")
        except Exception as e:
            logging.error(f"✗ Error al instalar {description}: {str(e)}")
            success = False
            continue

    if success:
        logging.info(success_message)
    else:
        logging.warning(error_message)

    return success
