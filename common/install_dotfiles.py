import os
import shutil
from datetime import datetime
import subprocess
import re
from InquirerPy import inquirer
from InquirerPy.utils import color_print


def install_dot(try_nvim=None):
    """
    Instala dotfiles y hace respaldo de las configuraciones existentes.

    Args:
        try_nvim (str, opcional): Si se debe instalar la configuración de nvim ('y' o 'n').
                                 Si es None, preguntará al usuario.
    """
    # Colores para mensajes en terminal (para uso con color_print)
    COLORS = {
        "verde": "#00FF00",
        "amarillo": "#FFFF00",
        "azul": "#0000FF",
        "rojo": "#FF0000",
    }

    # Obtener fecha actual para carpetas de respaldo
    date = datetime.now().strftime("%Y%m%d-%H%M")

    # Configuración de rutas
    home = os.path.expanduser("~")
    backup_folder = os.path.join(home, ".SENTUBackup")

    # Asegurar que los directorios XDG estén configurados
    if not os.path.exists(os.path.join(home, ".config", "user-dirs.dirs")):
        subprocess.run(["xdg-user-dirs-update"])

    # Preguntar por la configuración de nvim si no se proporcionó
    if try_nvim is None:
        color_print(
            [
                (
                    "Si ya tienes una configuración NEOVIM potente y súper Pro, escribe 'n' en la siguiente pregunta.\n",
                    COLORS["amarillo"],
                )
            ]
        )
        color_print(
            [
                (
                    "Si respondes 'y', tu configuración de neovim se moverá al directorio de respaldo.\n",
                    COLORS["amarillo"],
                )
            ]
        )

        try_nvim = inquirer.confirm(
            message="¿Quieres probar mi configuración de nvim?", default=True
        ).execute()
        try_nvim = "y" if try_nvim else "n"

    # Crear carpeta de respaldo si no existe
    os.makedirs(backup_folder, exist_ok=True)

    color_print(
        [
            (
                f"Los archivos de respaldo se almacenarán en {backup_folder}\n",
                COLORS["verde"],
            )
        ]
    )

    # Carpetas para respaldar
    config_folders = [
        "bspwm",
        "alacritty",
        "picom",
        "rofi",
        "eww",
        "sxhkd",
        "dunst",
        "kitty",
        "polybar",
        "ncmpcpp",
        "ranger",
        "tmux",
        "zsh",
        "mpd",
        "paru",
    ]

    # Respaldar configuraciones existentes
    for folder in config_folders:
        folder_path = os.path.join(home, ".config", folder)
        if os.path.exists(folder_path):
            try:
                backup_path = os.path.join(backup_folder, f"{folder}_{date}")
                shutil.move(folder_path, backup_path)
                color_print(
                    [
                        (f"{folder}", COLORS["amarillo"]),
                        (" carpeta respaldada exitosamente en ", COLORS["verde"]),
                        (f"{backup_path}\n", COLORS["azul"]),
                    ]
                )
            except Exception as e:
                color_print(
                    [
                        (
                            f"No se pudo respaldar la carpeta {folder}. Error: {str(e)}\n",
                            COLORS["rojo"],
                        )
                    ]
                )
        else:
            color_print(
                [
                    (f"{folder}", COLORS["amarillo"]),
                    (" carpeta no existe, no se necesita respaldo\n", COLORS["verde"]),
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
                        ("Carpeta nvim respaldada exitosamente en ", COLORS["verde"]),
                        (f"{backup_path}\n", COLORS["azul"]),
                    ]
                )
            except Exception as e:
                color_print(
                    [
                        (
                            f"No se pudo respaldar la carpeta nvim. Error: {str(e)}\n",
                            COLORS["rojo"],
                        )
                    ]
                )
        else:
            color_print(
                [("Carpeta nvim no existe, no se necesita respaldo\n", COLORS["verde"])]
            )

    # Respaldar configuraciones de Firefox
    firefox_profile = None
    firefox_path = os.path.join(home, ".mozilla", "firefox")
    if os.path.exists(firefox_path):
        profiles = [
            d for d in os.listdir(firefox_path) if d.endswith("default-release")
        ]
        if profiles:
            firefox_profile = profiles[0]

            # Respaldar carpeta chrome
            chrome_path = os.path.join(firefox_path, firefox_profile, "chrome")
            if os.path.exists(chrome_path):
                try:
                    backup_path = os.path.join(backup_folder, f"chrome_{date}")
                    shutil.move(chrome_path, backup_path)
                    color_print(
                        [
                            (
                                "Carpeta Chrome respaldada exitosamente en ",
                                COLORS["verde"],
                            ),
                            (f"{backup_path}\n", COLORS["azul"]),
                        ]
                    )
                except Exception as e:
                    color_print(
                        [
                            (
                                f"No se pudo respaldar la carpeta Chrome. Error: {str(e)}\n",
                                COLORS["rojo"],
                            )
                        ]
                    )

            # Respaldar user.js
            user_js_path = os.path.join(firefox_path, firefox_profile, "user.js")
            if os.path.exists(user_js_path):
                try:
                    backup_path = os.path.join(backup_folder, f"user.js_{date}")
                    shutil.move(user_js_path, backup_path)
                    color_print(
                        [
                            (
                                "Archivo user.js respaldado exitosamente en ",
                                COLORS["verde"],
                            ),
                            (f"{backup_path}\n", COLORS["azul"]),
                        ]
                    )
                except Exception as e:
                    color_print(
                        [
                            (
                                f"No se pudo respaldar el archivo user.js. Error: {str(e)}\n",
                                COLORS["rojo"],
                            )
                        ]
                    )

    # Respaldar .zshrc
    zshrc_path = os.path.join(home, ".zshrc")
    if os.path.exists(zshrc_path):
        try:
            backup_path = os.path.join(backup_folder, f".zshrc_{date}")
            shutil.move(zshrc_path, backup_path)
            color_print(
                [
                    ("Archivo .zshrc respaldado exitosamente en ", COLORS["verde"]),
                    (f"{backup_path}\n", COLORS["azul"]),
                ]
            )
        except Exception as e:
            color_print(
                [
                    (
                        f"No se pudo respaldar el archivo .zshrc. Error: {str(e)}\n",
                        COLORS["rojo"],
                    )
                ]
            )

    color_print([("¡Respaldo Completado!\n", COLORS["verde"])])

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
                    (f"{item}", COLORS["amarillo"]),
                    (" configuración instalada exitosamente\n", COLORS["verde"]),
                ]
            )
        except Exception as e:
            color_print(
                [
                    (
                        f"No se pudo instalar la configuración de {item}. Error: {str(e)}\n",
                        COLORS["rojo"],
                    )
                ]
            )

    # Copiar carpetas misc
    misc_folders = ["applications", "asciiart", "fonts", "startup-page"]
    for folder in misc_folders:
        try:
            shutil.copytree(
                os.path.join(dotfiles_path, "misc", folder),
                os.path.join(home, ".local", "share", folder),
                dirs_exist_ok=True,
            )
            color_print(
                [
                    (f"{folder}", COLORS["amarillo"]),
                    (" carpeta copiada exitosamente!\n", COLORS["verde"]),
                ]
            )
        except Exception as e:
            color_print(
                [
                    (
                        f"No se pudo copiar la carpeta {folder}. Error: {str(e)}\n",
                        COLORS["rojo"],
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
        color_print([("Carpeta bin copiada exitosamente!\n", COLORS["verde"])])
    except Exception as e:
        color_print(
            [(f"No se pudo copiar la carpeta bin. Error: {str(e)}\n", COLORS["rojo"])]
        )

    # Copiar tema de Firefox si existe el perfil
    if firefox_profile:
        firefox_source = os.path.join(dotfiles_path, "misc", "firefox")
        firefox_dest = os.path.join(firefox_path, firefox_profile)
        try:
            for item in os.listdir(firefox_source):
                src_path = os.path.join(firefox_source, item)
                dst_path = os.path.join(firefox_dest, item)
                if os.path.isfile(src_path):
                    shutil.copy2(src_path, dst_path)
                else:
                    shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
            color_print([("¡Tema de Firefox copiado exitosamente!\n", COLORS["verde"])])
        except Exception as e:
            color_print(
                [
                    (
                        f"No se pudo copiar el tema de Firefox. Error: {str(e)}\n",
                        COLORS["rojo"],
                    )
                ]
            )

        # Actualizar user.js con la ruta correcta
        user_js_path = os.path.join(firefox_dest, "user.js")
        if os.path.exists(user_js_path):
            with open(user_js_path, "r") as f:
                content = f.read()
            content = re.sub(
                r'user_pref\("browser\.startup\.homepage", "file:\/\/\/home\/z0mbi3\/.local',
                f'user_pref("browser.startup.homepage", "file:///home/{os.getenv("USER")}/.local',
                content,
            )
            with open(user_js_path, "w") as f:
                f.write(content)

    # Actualizar configuración de la página de inicio
    startup_config = os.path.join(home, ".local", "share", "startup-page", "config.js")
    if os.path.exists(startup_config):
        with open(startup_config, "r") as f:
            content = f.read()
        content = content.replace("name: 'gh0stzk'", f"name: '{os.getenv('USER')}'")
        with open(startup_config, "w") as f:
            f.write(content)

    # Copiar zshrc
    try:
        shutil.copy2(
            os.path.join(dotfiles_path, "home", ".zshrc"), os.path.join(home, ".zshrc")
        )
    except Exception as e:
        color_print([(f"No se pudo copiar .zshrc. Error: {str(e)}\n", COLORS["rojo"])])

    # Actualizar cache de fuentes
    try:
        subprocess.run(["fc-cache", "-rv"], capture_output=True)
    except Exception as e:
        color_print(
            [
                (
                    f"No se pudo actualizar el cache de fuentes. Error: {str(e)}\n",
                    COLORS["rojo"],
                )
            ]
        )

    color_print([("\n¡Archivos copiados exitosamente!\n", COLORS["verde"])])


if __name__ == "__main__":
    install_dot()
