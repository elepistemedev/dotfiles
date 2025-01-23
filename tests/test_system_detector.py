import subprocess
import unittest
from unittest.mock import mock_open, patch

from src.core.system_detector import SystemInfo


class TestSystemInfo(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data="ID=ubuntu\nVERSION_ID=20.04")
    def test_detect_linux_distribution_from_os_release(self, mock_file):
        system_info = SystemInfo()
        system_info._detect_linux_distribution()

        self.assertEqual(system_info.distribution, "ubuntu")
        self.assertEqual(system_info.version, "20.04")

    @patch("subprocess.check_output", side_effect=["ubuntu\n", "20.04\n"])
    def test_detect_linux_distribution_with_lsb_release(self, mock_subprocess):
        system_info = SystemInfo()

        with patch("builtins.open", side_effect=FileNotFoundError):
            system_info._detect_linux_distribution()

        self.assertEqual(system_info.distribution, "ubuntu")
        self.assertEqual(system_info.version, "20.04")

    @patch(
        "subprocess.check_output",
        side_effect=subprocess.CalledProcessError(1, "lsb_release"),
    )
    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_detect_linux_distribution_failure(self, mock_open, mock_subprocess):
        # Inicializamos SystemInfo
        system_info = SystemInfo()

        # Forzamos la detección fallida
        system_info._detect_linux_distribution()

        # Verificamos que la distribución y versión sean None
        self.assertIsNone(system_info.distribution)
        self.assertIsNone(system_info.version)

    def test_set_package_manager_ubuntu(self):
        system_info = SystemInfo()
        system_info.distribution = "ubuntu"
        system_info._set_package_manager()

        self.assertEqual(system_info.package_manager, "apt")
        self.assertEqual(system_info.update_command, ["sudo", "apt-get", "update"])
        self.assertEqual(system_info.install_command, ["sudo", "apt-get", "install", "-y"])

    def test_set_package_manager_fedora(self):
        system_info = SystemInfo()
        system_info.distribution = "fedora"
        system_info.version = "41"
        system_info._set_package_manager()

        self.assertEqual(system_info.package_manager, "dnf")
        self.assertEqual(system_info.update_command, ["sudo", "dnf", "update", "-y"])
        self.assertIn("git", system_info.dependencies_core)
        self.assertIn("neovim", system_info.dependencies_extended)


if __name__ == "__main__":
    unittest.main()
