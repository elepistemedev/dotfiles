import os
import shutil
from datetime import datetime
import subprocess
from InquirerPy import inquirer
from InquirerPy.utils import color_print
from pathlib import Path

# Colores para mensajes en terminal (para uso con color_print)


def get_xdg_update_path():
    """Obtiene la ruta del comando xdg-user-dirs-update."""
    possible_paths = [
        "/usr/bin/xdg-user-dirs-update",
        "/usr/local/bin/xdg-user-dirs-update",
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None


def setup_xdg_dirs():
    """Configura los directorios XDG si es necesario."""
    home = os.path.expanduser("~")
    xdg_config_path = os.path.join(home, ".config", "user-dirs.dirs")

    if not os.path.exists(xdg_config_path):
        xdg_command = get_xdg_update_path()

        if not xdg_command:
            color_print(
                [
                    (
                        "yellow",
                        "El comando xdg-user-dirs-update no está disponible en el sistema.\n",
                    ),
                    (
                        "cyan",
                        "Puede que necesite instalarlo con: sudo dnf install xdg-user-dirs\n",
                    ),
                ]
            )
            return False

        try:
            result = subprocess.run(
                [xdg_command],
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:
                color_print(
                    [
                        ("red", "Error al ejecutar xdg-user-dirs-update: "),
                        ("yellow", f"{result.stderr}\n"),
                    ]
                )
                return False

            return True

        except Exception as e:
            color_print(
                [
                    ("red", "Error al configurar directorios XDG: "),
                    ("yellow", f"{str(e)}\n"),
                ]
            )
            return False

    return True


def _get_config_folders():
    """
    Lee las carpetas presentes en ~/dotfiles/config y devuelve una lista con sus nombres.

    Returns:
        list: Lista de nombres de carpetas encontradas en el directorio
    """
    # Expandir el path ~ a la ruta completa del home del usuario
    config_path = os.path.expanduser("~/dotfiles/config")

    # Verificar si el directorio existe
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"El directorio {config_path} no existe")

    # Usar Path para manejar las rutas de manera más robusta
    path = Path(config_path)

    # Obtener solo los directorios (no archivos) y extraer sus nombres
    folders = [item.name for item in path.iterdir() if item.is_dir()]

    # Ordenar la lista alfabéticamente para mantener consistencia
    folders.sort()

    return folders


def install_dot(try_nvim=None):
    """
    Instala dotfiles y hace respaldo de las configuraciones existentes.

    Args:
        try_nvim (str, opcional): Si se debe instalar la configuración de nvim ('y' o 'n').
                                 Si es None, preguntará al usuario.
    """
    # Obtener fecha actual para carpetas de respaldo
    date = datetime.now().strftime("%Y%m%d-%H%M")

    # Configuración de rutas
    home = os.path.expanduser("~")
    backup_folder = os.path.join(home, ".SENTUBackup")

    # Asegurar que los directorios XDG estén configurados
    if not setup_xdg_dirs():
        return  # Detener si no se pueden configurar los directorios XDG

    # Preguntar por la configuración de nvim si no se proporcionó
    if try_nvim is None:
        color_print(
            [
                (
                    "yellow",
                    "Si ya tienes una configuración NEOVIM potente y súper Pro, escribe 'n' en la siguiente pregunta.\n",
                )
            ]
        )
        color_print(
            [
                (
                    "yellow",
                    "Si respondes 'Sí', tu configuración de neovim se moverá al directorio de respaldo.\n",
                )
            ]
        )

        try_nvim = inquirer.select(  # type: ignore
            message="¿Quieres probar mi configuración de nvim?",
            choices=["Sí", "No"],
        ).execute()
        try_nvim = "y" if try_nvim == "Sí" else "n"

    # Crear carpeta de respaldo si no existe
    os.makedirs(backup_folder, exist_ok=True)

    color_print(
        [
            (
                "cyan",
                f"Los archivos de respaldo se almacenarán en {backup_folder}\n",
            )
        ]
    )

    # El resto del código sigue igual...
    # (Mantendremos la lógica para respaldar y copiar archivos)

    # Carpetas para respaldar
    # config_folders = [
    #     "bspwm",
    #     "alacritty",
    #     "picom",
    #     "rofi",
    #     "eww",
    #     "sxhkd",
    #     "dunst",
    #     "kitty",
    #     "polybar",
    #     "ncmpcpp",
    #     "ranger",
    #     "tmux",
    #     "zsh",
    #     "mpd",
    #     "paru",
    #     "sentu",
    # ]
    config_folders = _get_config_folders()

    # Respaldar configuraciones existentes
    for folder in config_folders:
        folder_path = os.path.join(home, ".config", folder)
        if os.path.exists(folder_path):
            try:
                backup_path = os.path.join(backup_folder, f"{folder}_{date}")
                shutil.move(folder_path, backup_path)
                color_print(
                    [
                        ("yellow", f"{folder}"),
                        ("cyan", "carpeta respaldada exitosamente en "),
                        ("cyan", f"{backup_path}\n"),
                    ]
                )
            except Exception as e:
                color_print(
                    [
                        (
                            "red",
                            f"No se pudo respaldar la carpeta {folder}. Error: {str(e)}\n",
                        )
                    ]
                )
        else:
            color_print(
                [
                    ("yellow", f"{folder}"),
                    ("cyan", " carpeta no existe, no se necesita respaldo\n"),
                ]
            )

    # Manejar respaldo de nvim si se solicitó
    if try_nvim == "y":
        nvim_path = os.path.join(home, ".config", "nvim")
        if os.path.exists(nvim_path):
            try:
                backup_path = os.path.join(backup_folder, f"nvim_{date}")
                shutil.move(nvim_path, backup_path)
                color_print(
                    [
                        ("cyan", "Carpeta nvim respaldada exitosamente en "),
                        ("cyan", f"{backup_path}\n"),
                    ]
                )
            except Exception as e:
                color_print(
                    [
                        (
                            "red",
                            f"No se pudo respaldar la carpeta nvim. Error: {str(e)}\n",
                        )
                    ]
                )
        else:
            color_print([("cyan", "Carpeta nvim no existe, no se necesita respaldo\n")])

    # Respaldar .zshrc
    zshrc_path = os.path.join(home, ".zshrc")
    if os.path.exists(zshrc_path):
        try:
            backup_path = os.path.join(backup_folder, f".zshrc_{date}")
            shutil.move(zshrc_path, backup_path)
            color_print(
                [
                    ("cyan", "Archivo .zshrc respaldado exitosamente en "),
                    ("cyan", f"{backup_path}\n"),
                ]
            )
        except Exception as e:
            color_print(
                [
                    (
                        "red",
                        f"No se pudo respaldar el archivo .zshrc. Error: {str(e)}\n",
                    )
                ]
            )

    color_print([("cyan", "¡Respaldo Completado!\n")])

    # Crear directorios necesarios
    os.makedirs(os.path.join(home, ".config"), exist_ok=True)
    os.makedirs(os.path.join(home, ".local", "bin"), exist_ok=True)
    os.makedirs(os.path.join(home, ".local", "share"), exist_ok=True)

    # Copiar dotfiles
    dotfiles_path = os.path.join(home, "dotfiles")

    # Copiar archivos de configuración
    config_source = os.path.join(dotfiles_path, "config")
    for item in os.listdir(config_source):
        if item == "nvim" and try_nvim != "y":
            continue
        try:
            shutil.copytree(
                os.path.join(config_source, item),
                os.path.join(home, ".config", item),
                dirs_exist_ok=True,
            )
            color_print(
                [
                    ("yellow", f"{item}"),
                    ("cyan", " configuración instalada exitosamente\n"),
                ]
            )
        except Exception as e:
            color_print(
                [
                    (
                        "red",
                        f"No se pudo instalar la configuración de {item}. Error: {str(e)}\n",
                    )
                ]
            )

    # Copiar carpeta bin
    try:
        shutil.copytree(
            os.path.join(dotfiles_path, "misc", "bin"),
            os.path.join(home, ".local", "bin"),
            dirs_exist_ok=True,
        )
        color_print([("cyan", "Carpeta bin copiada exitosamente!\n")])
    except Exception as e:
        color_print([("red", f"No se pudo copiar la carpeta bin. Error: {str(e)}\n")])

    # Copiar zshrc
    try:
        shutil.copy2(
            os.path.join(dotfiles_path, "home", ".zshrc"), os.path.join(home, ".zshrc")
        )
    except Exception as e:
        color_print([("red", f"No se pudo copiar .zshrc. Error: {str(e)}\n")])

    # Actualizar cache de fuentes
    try:
        subprocess.run(["fc-cache", "-rv"], capture_output=True)
    except Exception as e:
        color_print(
            [
                (
                    "red",
                    f"No se pudo actualizar el cache de fuentes. Error: {str(e)}\n",
                )
            ]
        )

    color_print([("cyan", "\n¡Archivos copiados exitosamente!\n")])


if __name__ == "__main__":
    install_dot()
