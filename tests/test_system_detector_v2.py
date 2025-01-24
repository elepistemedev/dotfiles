import subprocess
from unittest.mock import mock_open, patch

from src.core.system_detector import SystemInfo


class TestSystemInfo:
    @patch("builtins.open", new_callable=mock_open, read_data="ID=ubuntu\nVERSION_ID=20.04")
    def test_detect_linux_distribution_from_os_release(self, mock_file):
        """Prueba la detección de distribución usando /etc/os-release."""
        system_info = SystemInfo()
        system_info._detect_linux_distribution()

        assert system_info.distribution == "ubuntu"
        assert system_info.version == "20.04"

    @patch("subprocess.check_output", side_effect=["ubuntu\n", "20.04\n"])
    def test_detect_linux_distribution_with_lsb_release(self, mock_subprocess):
        """Prueba la detección usando lsb_release cuando falla os-release."""
        system_info = SystemInfo()

        with patch("builtins.open", side_effect=FileNotFoundError):
            system_info._detect_linux_distribution()

        assert system_info.distribution == "ubuntu"
        assert system_info.version == "20.04"

    @patch(
        "subprocess.check_output",
        side_effect=subprocess.CalledProcessError(1, "lsb_release"),
    )
    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_detect_linux_distribution_failure(self, mock_subprocess, mock_open):
        """Prueba el fallo completo de detección de distribución."""
        system_info = SystemInfo()
        system_info._detect_linux_distribution()

        assert system_info.distribution is None
        assert system_info.version is None

    def test_set_package_manager_ubuntu(self):
        """Prueba la configuración correcta para Ubuntu."""
        system_info = SystemInfo()
        system_info.distribution = "ubuntu"
        system_info._set_package_manager()

        assert system_info.package_manager == "apt"
        assert system_info.update_command == ["sudo", "apt-get", "update"]
        assert system_info.install_command == ["sudo", "apt-get", "install", "-y"]

    def test_set_package_manager_fedora(self):
        """Prueba la configuración correcta para Fedora."""
        system_info = SystemInfo()
        system_info.distribution = "fedora"
        system_info.version = "41"
        system_info._set_package_manager()

        assert system_info.package_manager == "dnf"
        assert system_info.update_command == ["sudo", "dnf", "update", "-y"]
        assert "git" in system_info.dependencies_core
        assert "neovim" in system_info.dependencies_extended
