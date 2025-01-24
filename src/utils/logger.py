import logging
import logging.handlers
from pathlib import Path


def setup_logging(log_level: str = "INFO", logs_dir: str = "logs", app_name: str = "nombre_proyecto") -> None:
    """Configura el sistema de logging.

    Args:
        log_level: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        logs_dir: Directorio donde se guardarán los logs
        app_name: Nombre de la aplicación para el archivo de log
    """
    # Crear directorio de logs si no existe
    log_dir = Path(logs_dir)
    log_dir.mkdir(exist_ok=True)

    # Configurar el formato de los logs
    log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Configurar el manejador de archivos con rotación
    file_handler = logging.handlers.RotatingFileHandler(
        filename=log_dir / f"{app_name}.log",
        maxBytes=10485760,  # 10MB
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(log_format)

    # Configurar el manejador de consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)

    # Configurar el logger root
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)


# Ejemplo de uso en __init__.py o en el punto de entrada de la aplicación
if __name__ == "__main__":
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Aplicación iniciada")
