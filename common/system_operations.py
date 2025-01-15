import subprocess
from .logger_utils import setup_logger
import os
from pathlib import Path
import urllib.request
from urllib.error import URLError
import sys
from common.install_packages import install_packages
import zipfile

logging = setup_logger()


# 2. Actualizar sistema
def update_system(system_info, use_repo=False):
    """Actualiza el sistema usando el gestor de paquetes correspondiente"""
    if not system_info.update_command:
        logging.error("No se pudo determinar el comando de actualización")
        return False

    try:
        if use_repo:
            if not system_info.repositories:
                logging.info("No hay repositorios para configurar.")
            else:
                for repo_name, repo_command in system_info.repositories.items():
                    logging.warning(
                        f"Añadiendo repositorio {repo_name}:\n{' '.join(repo_command)}"
                    )
                    try:
                        result = subprocess.run(
                            repo_command,
                            capture_output=True,
                            text=True,
                            input="y\n",
                            check=True,
                        )
                        # DNF puede retornar 100 cuando no hay actualizaciones disponibles
                        if result.returncode == 0 or (
                            system_info.package_manager in ["dnf", "yum"]
                            and result.returncode == 100
                        ):
                            logging.info(
                                f"Repositorio {repo_name} configurado correctamente"
                            )
                        else:
                            logging.error(
                                f"Error configurando repositorio {repo_name}: {result.stderr}"
                            )
                            return False
                    except subprocess.CalledProcessError as e:
                        logging.error(
                            f"Error ejecutando comando para repositorio {repo_name}: {e.stderr}"
                        )
                        return False

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


# 3 Instalar dependencias básicas
def install_dependencies(system_info, use_extended=False):
    """
    Instala las dependencias necesarias del sistema

    Args:
        system_info: Objeto con la información del sistema
        use_extended: Bool que indica si usar dependencies_extended en lugar de dependencies_core

    Returns:
        bool: True si la instalación fue exitosa, False en caso contrario
    """
    if not system_info.install_command:
        logging.error("No se pudo determinar el comando de instalación")
        return False

    # Seleccionar qué conjunto de dependencias usar
    dependencies = (
        system_info.dependencies_extended
        if use_extended
        else system_info.dependencies_core
    )

    if not dependencies:
        logging.warning("No hay dependencias definidas para instalar")
        return True

    success = True
    try:
        for package in dependencies:
            logging.info(f"Instalando {package}...")
            cmd = system_info.install_command + [package]
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode != 0:
                logging.error(f"Error instalando {package}: {result.stderr}")
                success = False
                continue  # Continúa con el siguiente paquete aunque este haya fallado

        if success:
            dependency_type = "extendidas" if use_extended else "core"
            logging.info(
                f"Todas las dependencias {dependency_type} fueron instaladas correctamente"
            )
        else:
            logging.warning("Algunas dependencias no pudieron ser instaladas")

        return success

    except Exception as e:
        logging.error(f"Error instalando dependencias: {str(e)}")
        return False


# 4. Instalar y configurar zsh
def install_and_configure_zsh():
    """Configurando zsh como shell por defecto"""

    try:
        # Cambiar shell por defecto a zsh
        logging.info("Configurando zsh como shell por defecto...")
        user_name = os.getenv("USER")
        result = subprocess.run(
            ["sudo", "chsh", "-s", "/bin/zsh", str(user_name)],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise Exception(
                f"Error configurando zsh como shell por defecto: {result.stderr}"
            )

        logging.info("zsh instalado y configurado correctamente")
        return True
    except Exception as e:
        logging.error(f"Error instalando/configurando zsh: {str(e)}")
        return False


# 5. Clonar repositorio desde github
def clone_repo():
    """Clona el repositorio desde github en la carpeta home del usuario"""
    repo_url = "https://github.com/elepistemedev/dotfiles.git"
    home_dir = str(Path.home())
    repo_path = os.path.join(home_dir, "dotfiles")

    try:
        logging.info(f"Clonando repositorio dotfiles en {home_dir}...")
        subprocess.run(["git", "clone", "-b", "dev", repo_url, repo_path], check=True)
        logging.info("Repositorio clonado correctamente")
        return True
    except Exception as e:
        logging.error(f"Error clonando repositorio desde github: {str(e)}")
        return False


# 6. Instalar Anaconda
def setup_anaconda():
    """Descarga e instala Anaconda"""
    anaconda_url = (
        "https://repo.anaconda.com/archive/Anaconda3-2024.10-1-Linux-x86_64.sh"
    )
    installer_path = Path.home() / "anaconda_installer.sh"
    anaconda_path = Path.home() / "anaconda3"

    if anaconda_path.exists():
        logging.info("Anaconda ya está instalado")
        return True

    try:
        # Descargar Anaconda
        logging.info("Descargando Anaconda...")
        with urllib.request.urlopen(anaconda_url) as response:
            total_size = int(response.headers.get("Content-Length", 0))
            block_size = 8192
            downloaded = 0

            with open(installer_path, "wb") as file:
                while True:
                    buffer = response.read(block_size)
                    if not buffer:
                        break

                    downloaded += len(buffer)
                    file.write(buffer)

                    if total_size:
                        progress = int(50 * downloaded / total_size)
                        sys.stdout.write(
                            f"\rDescargando: [{'=' * progress}{' ' * (50 - progress)}] {downloaded}/{total_size} bytes"
                        )
                        sys.stdout.flush()

        print()  # Nueva línea después de la barra de progreso

        # Instalar Anaconda
        logging.info("Instalando Anaconda...")
        os.chmod(installer_path, 0o755)
        result = subprocess.run(
            ["bash", str(installer_path), "-b", "-p", str(anaconda_path)],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise Exception(result.stderr)

        # Limpiar instalador
        installer_path.unlink()

        # Configurar PATH en .zshrc en lugar de .bashrc
        zshrc_path = Path.home() / ".zshrc"
        with open(zshrc_path, "a") as zshrc:
            zshrc.write("\n# Anaconda3 PATH\n")
            zshrc.write(f'export PATH="{anaconda_path}/bin:$PATH"\n')

        logging.info("Anaconda instalado correctamente")
        return True

    except Exception as e:
        logging.error(f"Error instalando Anaconda: {str(e)}")
        if installer_path.exists():
            installer_path.unlink()
        return False


# 7. Instalar paquetes Python necesarios
def install_python_packages():
    """Instala los paquetes Python necesarios para la fase 2"""
    packages = ["rich", "InquirerPy", "typer", "tqdm", "gitlint", "textual"]
    anaconda_pip = str(Path.home() / "anaconda3" / "bin" / "pip")

    try:
        # Actualizar pip
        logging.info("Actualizando pip...")
        subprocess.run([anaconda_pip, "install", "--upgrade", "pip"], check=True)

        # Instalar paquetes
        for package in packages:
            logging.info(f"Instalando {package}...")
            result = subprocess.run(
                [anaconda_pip, "install", package], capture_output=True, text=True
            )
            if result.returncode != 0:
                raise Exception(f"Error instalando {package}: {result.stderr}")

        logging.info("Todos los paquetes Python han sido instalados")
        return True
    except Exception as e:
        logging.error(f"Error instalando paquetes Python: {str(e)}")
        return False


# 8. Instalar prompt Starship
def install_prompt():
    """Instala el prompt starship"""
    anaconda_pip = str(Path.home() / "anaconda3" / "bin" / "conda")
    try:
        logging.info("Instalando el prompt Starship...")
        subprocess.run(
            [anaconda_pip, "install", "-c", "conda-forge", "starship"], check=True
        )

        # Configurar PATH en .zshrc
        zshrc_path = Path.home() / ".zshrc"
        with open(zshrc_path, "a") as zshrc:
            zshrc.write("\n# Starship Prompt\n")
            zshrc.write('eval "$(starship init zsh)"\n')

        logging.info("Prompt Startship instalado correctamente")
        return True
    except Exception as e:
        logging.error(f"Error instalando el prompt Starship: {str(e)}")
        return False


# WARNING: De alguna forma ya se instala Node
def install_fnm():
    """Instala Fast Node Manager (fnm)"""
    repo_url = "https://fnm.vercel.app/install"
    try:
        logging.info("Instalando Fast Node Manager...")
        # Obtener el contenido del script
        curl_process = subprocess.run(
            ["curl", "-sS", repo_url], capture_output=True, text=True, check=True
        )
        # Ejecutar el script con sh
        subprocess.run(["sh"], input=curl_process.stdout, text=True, check=True)

        # Configurar PATH en .zshrc
        zshrc_path = Path.home() / ".zshrc"
        with open(zshrc_path, "a") as zshrc:
            zshrc.write("\n# Starship Prompt\n")
            zshrc.write('eval "$(fnm env --use-on-cd --shell zsh)"\n')

        logging.info("Prompt Startship instalado correctamente")
        return True
    except Exception as e:
        logging.error(f"Error instalando el prompt Starship: {str(e)}")
        return False


# TODO: Fase 2
def install_lazyvim():
    """Instalando Lazyvim"""
    repo_url = "https://github.com/LazyVim/starter"
    home_dir = str(Path.home())
    repo_path = os.path.join(home_dir, ".config/nvim")

    # Función helper para hacer backup de directorios si existen
    def backup_if_exists(path):
        if os.path.exists(path):
            subprocess.run(f"mv {path}{{,.bak}}", shell=True, check=True)

    try:
        # Hacer backup de los directorios si existen
        backup_if_exists(os.path.join(home_dir, ".config/nvim"))
        backup_if_exists(os.path.join(home_dir, ".local/share/nvim"))
        backup_if_exists(os.path.join(home_dir, ".local/state/nvim"))
        backup_if_exists(os.path.join(home_dir, ".cache/nvim"))

        logging.info("Instalando Lazyvim...")
        subprocess.run(["git", "clone", repo_url, repo_path], check=True)
        logging.info("Lazyvim instalado correctamente")
        return True
    except Exception as e:
        logging.error(f"Error instalando Lazyvim: {str(e)}")
        return False


# TODO: Fase 2
def configurar_docker():
    """Configurando Docker"""
    user_name = os.getenv("USER")

    commands = [
        ("sudo groupadd docker", "Creando grupo docker"),
        (f"sudo usermod -aG docker {user_name}", "Agregando usuario al grupo docker"),
        ("sudo systemctl enable docker.service", "Habilitando servicio docker"),
        ("sudo systemctl enable containerd.service", "Habilitando servicio containerd"),
        ("sudo systemctl start docker", "Iniciando servicio docker"),
    ]

    return install_packages(
        commands,
        start_message="Configurando Docker...",
        success_message="Docker configurado correctamente",
        error_message="Docker configurado con algunos errores",
    )


# TODO: Fase 2
def install_luapack():
    """Instalando luacheck y stylua con la función generalizada de instalación."""

    # Definir los comandos y descripciones para la instalación
    commands = [
        ("sudo luarocks install luacheck", "luacheck"),
        ("cargo install stylua", "stylua"),
    ]

    # Llamar a la función del módulo para instalar los paquetes
    return install_packages(
        commands,
        start_message="Instalando Paquetes para Lua...",
        success_message="Paquetes Lua instalados correctamente.",
        error_message="Se instalaron los paquetes Lua con algunos errores",
    )


# 9. instalar fuentes
def install_fonts():
    """
    Instala las fuentes Meslo y JetBrains Mono Nerd Fonts en el sistema.
    Requiere permisos de sudo para la instalación de fontconfig.
    """
    logger = setup_logger()

    try:
        # Instalar fontconfig
        logger.info("Instalando fontconfig...")
        subprocess.run(["sudo", "dnf", "-y", "install", "fontconfig"], check=True)

        # Definir URLs y rutas
        home_dir = str(Path.home())
        fonts_dir = os.path.join(home_dir, ".local", "share", "fonts")
        urls = {
            "Meslo.zip": "https://github.com/ryanoasis/nerd-fonts/releases/download/v3.3.0/Meslo.zip",
            "JetBrainsMono.zip": "https://github.com/ryanoasis/nerd-fonts/releases/download/v3.3.0/JetBrainsMono.zip",
        }

        # Crear directorio de fuentes si no existe
        os.makedirs(fonts_dir, exist_ok=True)
        logger.info(f"Directorio de fuentes creado/verificado: {fonts_dir}")

        # Descargar e instalar cada fuente
        for filename, url in urls.items():
            zip_path = os.path.join(home_dir, filename)

            # Descargar archivo
            logger.info(f"Descargando {filename}...")
            urllib.request.urlretrieve(url, zip_path)

            # Descomprimir archivo
            logger.info(f"Descomprimiendo {filename}...")
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(fonts_dir)

            # Eliminar archivo zip
            os.remove(zip_path)
            logger.info(f"Archivo {filename} eliminado")

        # Eliminar archivos de Windows
        logger.info("Eliminando archivos de Windows...")
        for file in os.listdir(fonts_dir):
            if "Windows" in file:
                os.remove(os.path.join(fonts_dir, file))
                logger.info(f"Archivo eliminado: {file}")

        # Actualizar cache de fuentes
        logger.info("Actualizando cache de fuentes...")
        subprocess.run(["fc-cache", "-fv"], check=True)

        logger.info("Instalación completada exitosamente!")
        return True

    except subprocess.CalledProcessError as e:
        logger.error(f"Error ejecutando comando: {e}")
        return False
    # except urllib.error.URLError as e:
    except URLError as e:
        logger.error(f"Error descargando archivos: {e}")
        return False
    except Exception as e:
        logger.error(f"Error inesperado: {e}")
        return False


# FIXME: cambiar un modulo independiente
def install_lazygit():
    """Instala Lazygit"""
    anaconda_pip = str(Path.home() / "anaconda3" / "bin" / "conda")
    try:
        logging.info("Instalando el prompt Starship...")
        subprocess.run(
            [anaconda_pip, "install", "Lazygit instalado correctamente")
        return True
    except Exception as e:
        logging.error(f"Error instalando Lazygit: {str(e)}")
        return False


# TODO: Fase 2
def install_post_install():
    """Post instalación"""

    commands = [
        ("curl -s https://ohmyposh.dev/install.sh | bash -s -- -d ~/bin","Instalando Oh My Posh")
        ("go install oss.terrastruct.com/d2@latest", "Instalando d2 diagram"),
        ("curl -fsS https://dl.brave.com/install.sh | sh", "Instalando Brave"),
        (
            "git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm",
            "Configurando tmux",
        ),
        ("tmux source ~/.tmux.conf", "activando tmux"),
        ("gem install tmuxinator", "instalando tmuxinator"),
        ("flatpak install flathub md.obsidian.Obsidian", "Instalando Obsidian"),
        ("flatpak install flathub org.freedownloadmanager.Manager",
        "Instalando FDM"),
    ]

    return install_packages(
        commands,
        start_message="Ejecutando post-instalación...",
        success_message="Post-instalación ejecutada correctamente",
        error_message="La post-instalación se ejecutó con algunos errores",
    )
