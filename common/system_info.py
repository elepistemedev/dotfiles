import platform
import subprocess
from .logger_utils import setup_logger

logging = setup_logger()


class SystemInfo:
    def __init__(self):
        self.system = platform.system().lower()
        self.distribution = None
        self.version = None
        self.package_manager = None
        self.update_command = None
        self.install_command = None
        self.repositories = None

        if self.system == "linux":
            self._detect_linux_distribution()
            self._set_package_manager()

    def _detect_linux_distribution(self):
        """Detecta la distribución Linux y su versión"""
        try:
            with open("/etc/os-release") as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith("ID="):
                        self.distribution = (
                            line.split("=")[1].strip().strip('"').lower()
                        )
                    elif line.startswith("VERSION_ID="):
                        self.version = line.split("=")[1].strip().strip('"')
        except FileNotFoundError:
            try:
                self.distribution = (
                    subprocess.check_output(
                        ["lsb_release", "-si"], universal_newlines=True
                    )
                    .strip()
                    .lower()
                )
                self.version = subprocess.check_output(
                    ["lsb_release", "-sr"], universal_newlines=True
                ).strip()
            except (subprocess.CalledProcessError, FileNotFoundError):
                logging.error("No se pudo detectar la distribución Linux")

    def _set_package_manager(self):
        """Configura el gestor de paquetes y sus comandos"""
        package_managers = {
            "debian": {
                "manager": "apt",
                "update": ["sudo", "apt-get", "update"],
                "install": ["sudo", "apt-get", "install", "-y"],
            },
            "ubuntu": {
                "manager": "apt",
                "update": ["sudo", "apt-get", "update"],
                "install": ["sudo", "apt-get", "install", "-y"],
            },
            "fedora": {
                "manager": "dnf",
                "update": ["sudo", "dnf", "check-update"],
                "install": ["sudo", "dnf", "install", "-y"],
                "repo": {
                    "rpmfusion": [
                        "sudo",
                        "dnf",
                        "install",
                        f"https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-{self.version}.noarch.rpm",
                    ],
                    "docker": [
                        "sudo",
                        "dnf",
                        "config-manager",
                        "addrepo",
                        "--from-repofile=https://download.docker.com/linux/fedora/docker-ce.repo",
                    ],
                },
            },
            "centos": {
                "manager": "yum",
                "update": ["sudo", "yum", "check-update"],
                "install": ["sudo", "yum", "install", "-y"],
            },
            "arch": {
                "manager": "pacman",
                "update": ["sudo", "pacman", "-Sy"],
                "install": ["sudo", "pacman", "-S", "--noconfirm"],
            },
            "manjaro": {
                "manager": "pacman",
                "update": ["sudo", "pacman", "-Sy"],
                "install": ["sudo", "pacman", "-S", "--noconfirm"],
            },
        }

        if self.distribution in package_managers:
            pm_info = package_managers[self.distribution]
            self.package_manager = pm_info["manager"]
            self.update_command = pm_info["update"]
            self.install_command = pm_info["install"]
            self.repositories = pm_info.get("repo", {})
