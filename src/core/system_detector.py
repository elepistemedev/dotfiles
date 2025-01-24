import logging
import platform
import subprocess

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
        self.dependencies_core = None
        self.dependencies_extended = None

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
            "mint": {
                "manager": "apt",
                "update": ["sudo", "apt-get", "update"],
                "install": ["sudo", "apt-get", "install", "-y"],
            },
            "fedora": {
                "manager": "dnf",
                "update": ["sudo", "dnf", "update", "-y"],
                "install": ["sudo", "dnf", "install", "-y", "--allowerasing"],
                "repo": {
                    "rpmfusion-nonfree": [
                        "sudo",
                        "dnf",
                        "install",
                        "-y",
                        f"https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-{self.version}.noarch.rpm",
                    ],
                    "rpmfusion-free": [
                        "sudo",
                        "dnf",
                        "install",
                        "-y",
                        f"https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-{self.version}.noarch.rpm",
                    ],
                    "docker": [
                        "sudo",
                        "dnf",
                        "config-manager",
                        "addrepo",
                        "--from-repofile=https://download.docker.com/linux/fedora/docker-ce.repo",
                    ],
                    "google-chrome": [
                        "sudo",
                        "dnf",
                        "install",
                        "-y",
                        "https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm",
                    ],
                    "lazygit": ["sudo", "dnf", "copr", "enable", "atim/lazygit", "-y"],
                },
                "dependencies": {
                    "core": [
                        "git",
                        "curl",
                        "wget",
                        "gcc",
                        "make",
                        "unzip",
                        "zsh",
                        "golang",
                        "cargo",
                        "g++",
                        "python3",
                        "ruby",
                        "unrar",
                        "p7zip",
                        "p7zip-plugins",
                        "xdg-user-dirs",
                        "lsd",
                        "java",
                        "dnf-utils",
                        "flatpak",
                        "kernel-devel",
                        "gcc",
                        "make",
                        "automake",
                        "perl",
                        "elfutils-libelf-devel",
                    ],
                    "extended": [
                        "lazygit",
                        "ripgrep",
                        "fd-find",
                        "neovim",
                        "fastfetch",
                        "util-linux-user",
                        "anacron",
                        "neovim",
                        "python3-neovim",
                        "kitty",
                        "lua-devel",
                        "luarocks",
                        "docker-ce",
                        "docker-ce-cli",
                        "containerd.io",
                        "docker-compose-plugin",
                        "bat",
                        "fzf",
                        "httpie",
                        "ripgrep",
                        "tmux",
                        "htop",
                        "proselint",
                        "lm_sensors",
                        "discord",
                        "alacritty",
                        "kde-connect",
                        "dnf-utils",
                        "kdenlive",
                        "openshot",
                        "vlc",
                        "mpv",
                        "gnome-mpv",
                        "soundconverter",
                        "audacity",
                        "muse",
                        "lmms",
                        "amarok",
                        "flowblade",
                        "dnf-plugins-core",
                        "xine-lib",
                        "xine-lib-extras",
                        "xine-lib-extras-freeworld",
                        "libdvdread",
                        "libdvdnav",
                        "lsdvd",
                        "libdvbpsi",
                        "ffmpeg",
                        "libmatroska",
                        "xvidcore",
                        "gimp",
                        "inkscape",
                        "libreoffice-writer",
                        "libreoffice-calc",
                        "libreoffice-impress",
                        "libreoffice-draw",
                        "libreoffice-langpack-es",
                        "gstreamer1-devel",
                        "gstreamer1-plugins-base-tools",
                        "gstreamer1-doc",
                        "gstreamer1-plugins-base-devel",
                        "gstreamer1-plugins-good",
                        "gstreamer1-plugins-good-extras",
                        "gstreamer1-plugins-bad-free",
                        "gstreamer1-plugins-bad-free-devel",
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
            self.dependencies_core = pm_info.get("dependencies", {}).get("core", [])
            self.dependencies_extended = pm_info.get("dependencies", {}).get("extended", [])
