import subprocess
from unittest.mock import mock_open, patch

from src.core.system_detector import SystemInfo


class TestSystemInfo:
    @patch("builtins.open", new_callable=mock_open, read_data="ID=ubuntu\nVERSION_ID=20.04")
    def test_detect_linux_distribution_from_os_release(self):
        """Prueba la detección de distribución usando /etc/os-release."""
        system_info = SystemInfo()
        system_info._detect_linux_distribution()

        assert system_info.distribution == "ubuntu"
        assert system_info.version == "20.04"

    @patch("subprocess.check_output", side_effect=["ubuntu\n", "20.04\n"])
    def test_detect_linux_distribution_with_lsb_release(self):
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
    def test_detect_linux_distribution_failure(self):
        """Prueba el fallo completo de detección de distribución."""
        system_info = SystemInfo()
        system_info._detect_linux_distribution()

        assert system_info.distribution is None
        assert system_info.version is None

    @patch("src.core.package_config_loader.PackageManagerConfigLoader.get_config")
    def test_set_package_manager_ubuntu(self, mock_get_config):
        """Prueba la configuración correcta para Ubuntu."""
        # Configuración mockeada para Ubuntu
        mock_config = {
            "manager": "apt",
            "update_command": ["sudo", "apt-get", "update"],
            "install_command": ["sudo", "apt-get", "install", "-y"],
            "repositories": {},
            "dependencies": {"core": [], "extended": []},
        }
        mock_get_config.return_value = mock_config

        # Evitar detección automática del sistema
        with patch.object(SystemInfo, "_detect_linux_distribution", autospec=True):
            system_info = SystemInfo()
            system_info.system = "linux"  # Forzar entorno Linux
            system_info.distribution = "ubuntu"  # Distribución mockeada
            system_info._set_package_manager()

        assert system_info.package_manager == "apt"
        assert system_info.update_command == ["sudo", "apt-get", "update"]
        assert system_info.install_command == ["sudo", "apt-get", "install", "-y"]

    @patch("src.core.package_config_loader.PackageManagerConfigLoader.get_config")
    def test_set_package_manager_fedora(self, mock_get_config):
        """Prueba la configuración correcta para Fedora."""
        # Configuración mockeada para Fedora
        mock_config = {
            "manager": "dnf",
            "update_command": ["sudo", "dnf", "update", "-y"],
            "install_command": ["sudo", "dnf", "install", "-y"],
            "repositories": {},
            "dependencies": {
                "core": ["git", "python3-devel"],
                "extended": ["neovim", "htop"],
            },
        }
        mock_get_config.return_value = mock_config

        # Evitar detección automática del sistema
        with patch.object(SystemInfo, "_detect_linux_distribution", autospec=True):
            system_info = SystemInfo()
            system_info.system = "linux"
            system_info.distribution = "fedora"
            system_info.version = "41"
            system_info._set_package_manager()

        assert system_info.package_manager == "dnf"
        assert system_info.update_command == ["sudo", "dnf", "update", "-y"]
        assert "git" in system_info.dependencies_core
        assert "neovim" in system_info.dependencies_extended
