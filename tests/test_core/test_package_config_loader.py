from pathlib import Path
import unittest
from unittest.mock import MagicMock, mock_open, patch

import yaml

from src.core.package_config_loader import (
    PackageManagerConfigLoader,
)  # Ajuste para importar correctamente


class TestPackageManagerConfigLoader(unittest.TestCase):
    @patch("src.core.package_config_loader.Path")
    @patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
    @patch("src.core.package_config_loader.yaml.safe_load", return_value={"key": "value"})
    def test_load_configs(self, mock_safe_load, mock_open_func, mock_path):
        """Prueba que los archivos YAML se cargan correctamente."""
        # Simular archivos YAML en el directorio
        mock_file = MagicMock()
        mock_file.stem = "test_distribution"
        mock_file.__str__.return_value = "fake_file.yaml"  # Necesario para que open funcione correctamente
        mock_path.return_value.glob.return_value = [mock_file]

        # Llamar al método
        PackageManagerConfigLoader.load_configs(config_dir="fake_dir")

        # Validar que se abrieron los archivos y se cargaron
        mock_open_func.assert_called_once_with("fake_file.yaml", encoding="utf-8")
        mock_safe_load.assert_called_once_with(mock_open_func())
        self.assertIn("test_distribution", PackageManagerConfigLoader._configs)
        self.assertEqual(PackageManagerConfigLoader._configs["test_distribution"], {"key": "value"})

    @patch("src.core.package_config_loader.PackageManagerConfigLoader.load_configs")
    def test_get_config_calls_load_configs(self, mock_load_configs):
        """Prueba que get_config llama a load_configs si las configuraciones no están cargadas."""
        # Asegurarse de que _configs esté vacío
        PackageManagerConfigLoader._configs = {}

        # Llamar al método
        result = PackageManagerConfigLoader.get_config("non_existent")

        # Validar que load_configs fue llamado
        mock_load_configs.assert_called_once()
        self.assertEqual(result, {})

    @patch("src.core.package_config_loader.PackageManagerConfigLoader.load_configs")
    def test_get_config_returns_correct_config(self, mock_load_configs):
        """Prueba que get_config devuelve la configuración correcta."""
        # Configurar datos simulados
        PackageManagerConfigLoader._configs = {"ubuntu": {"key": "value"}}

        # Llamar al método
        result = PackageManagerConfigLoader.get_config("ubuntu")

        # Validar el resultado
        mock_load_configs.assert_not_called()  # No debería cargar de nuevo
        self.assertEqual(result, {"key": "value"})

    @patch("pathlib.Path.glob")
    @patch("builtins.print")
    def test_load_configs_with_yaml_error(self, mock_print, mock_glob):
        """Prueba el manejo de errores en archivos YAML inválidos"""
        # Configurar mocks
        fake_yaml = Path("invalid.yaml")
        mock_glob.return_value = [fake_yaml]

        # Simular archivo existente pero con YAML inválido
        error_message = "Error de sintaxis YAML"
        with patch("builtins.open", mock_open(read_data="invalid: yaml")):
            with patch("yaml.safe_load", side_effect=yaml.YAMLError(error_message)):
                PackageManagerConfigLoader.load_configs()

        # Verificar mensaje de error
        mock_print.assert_called_with(f"Error cargando configuración invalid: {error_message}")

        # Verificar que no se cargó la configuración inválida
        assert "invalid" not in PackageManagerConfigLoader._configs

    @patch("pathlib.Path.glob")
    @patch("builtins.print")
    def test_load_configs_with_io_error(self, mock_print, mock_glob):
        """Prueba el manejo de errores de lectura de archivos"""
        # Configurar mocks
        fake_yaml = Path("unreadable.yaml")
        mock_glob.return_value = [fake_yaml]

        # Simular error de archivo
        error_message = "Permiso denegado"
        with patch("builtins.open", mock_open()) as mock_file:
            mock_file.side_effect = OSError(error_message)
            PackageManagerConfigLoader.load_configs()

        # Verificar mensaje de error
        mock_print.assert_called_with(f"Error cargando configuración unreadable: {error_message}")

        # Verificar que no se cargó la configuración inválida
        assert "unreadable" not in PackageManagerConfigLoader._configs


if __name__ == "__main__":
    unittest.main()
