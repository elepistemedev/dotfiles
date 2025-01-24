from pathlib import Path
import unittest
from unittest.mock import MagicMock, patch

from src.utils.logger import (
    setup_logging,
)  # Reemplaza 'src.utils.logger' por el nombre de tu archivo Python


class TestSetupLogging(unittest.TestCase):
    @patch("src.utils.logger.Path")
    @patch("src.utils.logger.logging")
    def test_crea_directorio_logs(self, mock_logging, mock_path):
        """Prueba que se crea el directorio de logs si no existe."""
        mock_dir = MagicMock()
        mock_path.return_value = mock_dir

        setup_logging()

        mock_dir.mkdir.assert_called_once_with(exist_ok=True)

    @patch("src.utils.logger.logging.handlers.RotatingFileHandler")
    @patch("src.utils.logger.logging.StreamHandler")
    @patch("src.utils.logger.logging.getLogger")
    def test_configuracion_manejadores(self, mock_get_logger, mock_stream_handler, mock_rotating_handler):
        """Prueba que los manejadores de archivo y consola están configurados correctamente."""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        setup_logging(log_level="DEBUG", logs_dir="test_logs", app_name="test_app")

        # Verificar que RotatingFileHandler se configuró correctamente
        mock_rotating_handler.assert_called_once_with(
            filename=Path("test_logs") / "test_app.log",
            maxBytes=10485760,
            backupCount=5,
            encoding="utf-8",
        )

        # Verificar que StreamHandler fue creado
        mock_stream_handler.assert_called_once()

        # Verificar que ambos manejadores se añaden al logger
        self.assertEqual(mock_logger.addHandler.call_count, 2)

    @patch("src.utils.logger.logging.getLogger")
    def test_configuracion_nivel_logging(self, mock_get_logger):
        """Prueba que el nivel de logging se configura correctamente."""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        setup_logging(log_level="ERROR")

        mock_logger.setLevel.assert_called_once_with("ERROR")

    @patch("src.utils.logger.logging.Formatter")
    @patch("src.utils.logger.logging.handlers.RotatingFileHandler")
    @patch("src.utils.logger.logging.StreamHandler")
    def test_configuracion_formato_logs(self, mock_stream_handler, mock_rotating_handler, mock_formatter):
        """Prueba que el formato de los logs se configura correctamente."""
        mock_formatter_instance = MagicMock()
        mock_formatter.return_value = mock_formatter_instance

        setup_logging()

        # Verificar que Formatter fue creado
        mock_formatter.assert_called_once_with("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        # Verificar que se aplica el formato a ambos manejadores
        mock_rotating_handler.return_value.setFormatter.assert_called_once_with(mock_formatter_instance)
        mock_stream_handler.return_value.setFormatter.assert_called_once_with(mock_formatter_instance)


if __name__ == "__main__":
    unittest.main()
