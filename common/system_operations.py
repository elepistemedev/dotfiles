import os
import subprocess

from common.system_info import SystemInfo
from common.install_packages import install_packages
from common.system_info import SystemInfo  # Asegúrate de que esta importación esté aquí
from .logger_utils import setup_logger

logging = setup_logger()


def run_step(step, system_info, config):
    """
    Ejecuta un paso específico de la instalación.
    """
    task = step.get("task")
    if task == "update_system":
        return update_system(system_info)
    elif task == "install_dependencies":
        group = step.get("group")
        return install_dependencies(system_info, group)
    elif task == "install_and_configure_zsh":
        return install_and_configure_zsh(system_info)
    elif task == "clone_repo":
        return clone_repo()
    elif task == "install_uv":
        return install_uv(config)
    elif task == "install_rye":
        #TODO: Implementar la funcion install_rye
        return install_rye(config)
    elif task == "install_python_packages":
        return install_python_packages(config, system_info)
        return True
    elif task == "install_fonts":
        return install_fonts(config)
    elif task == "configurar_docker":
        return configurar_docker(config)
    elif task == "install_post_install":
        return install_post_install(config)
    elif task == "install_dotfiles":
        return install_dotfiles()
    else:
        logging.error(f"Tarea desconocida: {task}")
        return False




def clone_repo():
    """Clona el repositorio git."""
    repo_url = "https://github.com/MatiasP-dev/sentu-install"
    repo_path = os.path.expanduser("~/Repos/sentu-install")
    
    if os.path.exists(repo_path):
        logging.info(f"El repositorio ya existe en {repo_path}")
        return True

    logging.info(f"Clonando repositorio: {repo_url} en {repo_path}")
    try:
        subprocess.run(["git", "clone", repo_url, repo_path], check=True)
        os.chdir(repo_path)  # Mover al directorio recién creado
        logging.info(f"Repositorio clonado correctamente en {repo_path}")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Error al clonar el repositorio: {e}")
        return False
    except Exception as e:
        logging.error(f"Error inesperado: {e}")
        return False





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
                    logging.warning(f"Añadiendo repositorio {repo_name}:\n{' '.join(repo_command)}")
                    try:
                        result = subprocess.run(repo_command, text=True, input="y\n", check=True, shell=True)
                        # DNF puede retornar 100 cuando no hay actualizaciones disponibles
                        if result.returncode == 0 or (
                            system_info.package_manager in ["dnf", "yum"] and result.returncode == 100
                        ):
                            logging.info(f"Repositorio {repo_name} configurado correctamente")
                        else:
                            logging.error(f"Error configurando repositorio {repo_name}: {result.stderr}")
                            return False
                    except subprocess.CalledProcessError as e:
                        logging.error(f"Error al ejecutar comando del repositorio {repo_name}: {e}")
                        return False
                    except FileNotFoundError:
                        logging.error(f"Comando no encontrado al configurar el repositorio {repo_name}")
                        return False
                    except Exception as e:
                        logging.error(f"Error inesperado al configurar el repositorio {repo_name}: {e}")
                        return False

        logging.info(f"Ejecutando actualización del sistema: {' '.join(system_info.update_command)}")
        result = subprocess.run(system_info.update_command, text=True, input="y\n", check=True, shell=True)
        # DNF puede retornar 100 cuando no hay actualizaciones disponibles
        if result.returncode == 0 or (system_info.package_manager in ["dnf", "yum"] and result.returncode == 100):
            logging.info("Sistema actualizado correctamente")
            return True
        else:
            logging.error(f"Error al actualizar el sistema: {result.stderr}")
            return False
    except subprocess.CalledProcessError as e:
        logging.error(f"Error al ejecutar el comando de actualización: {e}")
        return False
    except FileNotFoundError:
        logging.error("Comando de actualización no encontrado")
        return False
    except Exception as e:
        logging.error(f"Error inesperado al actualizar el sistema: {e}")
        return False


# 3. Instalar dependencias básicas
def install_dependencies(system_info, group):
    """
    Instala las dependencias necesarias según el sistema operativo y el grupo especificado.
    """
    dependency_type = group
    if group not in ["core", "extended"]:
      logging.error(f"Grupo de dependencias desconocido: {group}")
      return False

    dependencies = system_info.dependencies_core  # Por defecto, usa las dependencias "core"
    if group == "extended":
      dependencies = system_info.dependencies_extended
    
    if not system_info.install_command:
        logging.error("No se pudo determinar el comando de instalación")
        return False
    
    if not dependencies:
        logging.info(f"No se encontraron dependencias {dependency_type} para instalar.")
        return True

    try:  
        install_command = system_info.install_command + dependencies
        logging.info(f"Instalando dependencias {dependency_type}: {' '.join(install_command)}")
        result = subprocess.run(install_command, text=True, input="y\n", check=True, shell=True)
        if result.returncode == 0:
            logging.info(f"Dependencias {dependency_type} instaladas correctamente")
            return True
        else:
            logging.error(f"Error al instalar dependencias {dependency_type}: {result.stderr}")
            return False
    except subprocess.CalledProcessError as e:
        logging.error(f"Error al ejecutar el comando de instalación de dependencias: {e}")
        return False
    except FileNotFoundError:
        logging.error("Comando de instalación no encontrado")
        return False
    except Exception as e:
        logging.error(f"Error inesperado al instalar dependencias: {e}")
        return False


# 4. Instalar y configurar zsh
def install_and_configure_zsh(system_info):
    """Instala zsh y lo establece como el shell predeterminado usando la configuración"""
    if not system_info.install_command:
        logging.error("No se pudo determinar el comando de instalación")
        return False

    zsh_dependency = "zsh"  # Asumimos que 'zsh' es el nombre del paquete
    try:
        # Verificar si zsh ya está instalado
        if subprocess.run(["which", "zsh"], capture_output=True, text=True).returncode != 0:
            logging.info("Instalando zsh...")
            install_command = system_info.install_command + [zsh_dependency]
            result = subprocess.run(install_command, capture_output=True, text=True, check=True, shell=True)
            logging.info(result.stdout)
            logging.info("zsh instalado correctamente")
        else:
            logging.info("zsh ya está instalado")

        # Verificar si zsh es el shell predeterminado
        current_shell = os.environ.get("SHELL")
        if "/zsh" not in current_shell:
            logging.warning(f"El shell predeterminado actual es: {current_shell}")
            change_shell = input("¿Deseas cambiar tu shell predeterminado a zsh? (y/N): ").lower()
            if change_shell == "y":
                user = os.environ.get("USER")
                subprocess.run(["chsh", "-s", "/bin/zsh", user], check=True)
                logging.info(f"Shell predeterminado cambiado a zsh para el usuario {user}. Reinicia tu terminal.")
            else:
                logging.info("No se cambió el shell predeterminado.")
        else:
            logging.info("zsh ya es el shell predeterminado")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Error al instalar o configurar zsh: {e}")
        return False
    except FileNotFoundError:
        logging.error("Comando no encontrado al instalar o configurar zsh")
        return False
    except Exception as e:
        logging.error(f"Error inesperado al instalar o configurar zsh: {e}")
        return False



def install_python_packages(config, system_info):
    """Instala paquetes Python usando rye."""
    dependencies_python = config.get("sentu_install", {}).get("package_managers", {}).get("linux",{}).get(system_info.distribution,{}).get("dependencies_python")

    if not dependencies_python:
        logging.info(f"No se encontraron dependencias Python para instalar.")
        return True
    
    try:
        if system_info.package_manager == "pacman":
            install_command = system_info.install_command + dependencies_python
            logging.info(f"Instalando dependencias Python con pacman: {' '.join(install_command)}")
            result = subprocess.run(install_command, text=True, input="y\n", check=True, shell=True)
        for dependency in dependencies_python:
          rye_add_command = ["rye", "add", dependency]
          logging.info(f"Instalando dependencias Python con rye: {rye_add_command}")
          result = subprocess.run(rye_add_command, text=True, input="y\n", check=True, shell=True)
          if result.returncode == 0:
              logging.info(f"Dependencia Python {dependency} instalada correctamente")
          else:
              logging.error(f"Error al instalar la dependencia Python {dependency}: {result.stderr}")
              return False
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Error al ejecutar el comando de instalación de dependencias Python: {e}")
        return False
    except Exception as e:
        logging.error(f"Error inesperado al instalar dependencias Python: {e}")
        return False



def configurar_docker(config):
    """Configura Docker desde la configuración."""
    logger = setup_logger()
    system_info = SystemInfo()
    docker_config = config.get("phase_2", {}).get("configurar_docker", {}).get(system_info.distribution)

    if not docker_config:
        logger.warning(f"No se encontró configuración de Docker para la distribución: {system_info.distribution}")
        return True

    commands_to_execute = []
    for item in docker_config:
        command = item.get("command")
        description = item.get("description")
        if command and description:
            commands_to_execute.append((command, description))

    return install_packages(
        commands_to_execute,
        start_message="Configurando Docker...",
        success_message="Docker configurado correctamente. Puede que necesites cerrar sesión y volver a entrar para que los cambios en el grupo docker surtan efecto.",
        error_message="Error al configurar Docker.",
    )


def install_from_config(config, section, key, start_message, success_message, error_message):
    """Instala paquetes o ejecuta comandos definidos en la configuración."""
    logger = setup_logger()
    commands_from_config = config.get(section, {}).get(key)

    if not commands_from_config:
        logger.info(f"No se encontraron comandos definidos para '{key}' en la sección '{section}'.")
        return True

    commands_to_execute = []
    if isinstance(commands_from_config, str):
        commands_to_execute.append((commands_from_config, key))  # Usar la clave como descripción si es un solo comando
    elif isinstance(commands_from_config, list):
        for item in commands_from_config:
            if isinstance(item, str):
                commands_to_execute.append((item, key))  # Usar la clave como descripción si es una lista de strings
            elif isinstance(item, dict):
                command = item.get("command")
                description = item.get("description", key)  # Usar la clave si no hay descripción
                if command:
                    commands_to_execute.append((command, description))

    return install_packages(
        commands_to_execute,
        start_message=start_message,
        success_message=success_message,
        error_message=error_message,
    )


def install_post_install(config):
    """Ejecuta los comandos de post-instalación definidos en la configuración."""
    return install_from_config(
        config,
        "phase_2",
        "install_post_install_commands",
        "Ejecutando post-instalaciones...",
        "Post-instalaciones completadas exitosamente",
        "Las post-instalaciones se completaron con algunos errores",
    )


def install_uv(config):
    """Instala uv usando el comando de configuración."""
    return install_from_config(
        config,
        "sentu_install",
        "uv_install_command",
        "Instalando uv...",
        "uv instalado correctamente.",
        "Error al instalar uv.",
    )


def install_fonts(config):
    """Instala las fuentes desde la configuración."""
    return install_from_config(
        config,
        "sentu_install",
        "install_fonts_commands",
        "Instalando fuentes...",
        "Fuentes instaladas correctamente. Puede que necesites reiniciar tu terminal.",
        "Error al instalar las fuentes.",
    )


def install_rye(config):
    """Instala rye usando el comando de configuración."""
    return install_from_config(
        config, "sentu_install", "rye", "Instalando rye...", "Rye instalado correctamente.", "Error al instalar rye."
    )



def install_dotfiles(config):
    """Instala las dotfiles desde la configuración."""
    logger = setup_logger()
    command = config.get("phase_2", {}).get("install_dotfiles", {}).get("command")
    description = config.get("phase_2", {}).get("install_dotfiles", {}).get("description")
    
    if not command or not description:
        logger.error("No se encontró comando o descripción para install_dotfiles en la configuración.")
        return False
    
    return install_packages(
        [(command, description)], "Instalando dotfiles...", "dotfiles instalados correctamente.", "Error al instalar dotfiles"
    )

