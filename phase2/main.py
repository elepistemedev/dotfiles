from InquirerPy import inquirer
from common.logo import show as logo
from common.system_info import SystemInfo
from common.system_operations import (
    update_system,
    install_dependencies,
    install_lazyvim,
    configurar_docker,
    install_luapack,
    install_lazygit,
    install_post_install,
)
from InquirerPy.utils import color_print
from common.install_dotfiles import install_dot


def fase2():
    # 1. Detectar sistema operativo
    system_info = SystemInfo()
    color_print([("yellow", f"Sistema detectado: {system_info.system}")])

    if system_info.distribution:
        color_print(
            [
                (
                    "yellow",
                    f"Distribución: {system_info.distribution} {system_info.version}",
                ),
            ]
        )
        color_print([("yellow", f"Gestor de paquetes: {system_info.package_manager}")])

    # 2. Actualizar sistema
    color_print([("cyan", "⚡ Actualizando sistema...")])
    if not update_system(system_info, use_repo=True):
        color_print([("red", "❌ No se pudo actualizar el sistema")])
        return
    color_print([("green", "✓ Sistema actualizado correctamente")])

    # 3. Instalar dependencias básicas
    color_print([("cyan", "⚡ Instalando dependencias básicas...")])
    if not install_dependencies(system_info, use_extended=True):
        color_print([("red", "❌ No se pudieron instalar las dependencias")])
        return
    color_print([("green", "✓ Dependencias instaladas correctamente")])

    # 4. Instalar Lazyvim
    color_print([("cyan", "⚡ Instalando Lazyvim...")])
    if not install_lazyvim():
        color_print([("red", "❌ No se pudo instalar Lazyvim")])
        return
    color_print([("green", "✓ Lazyvim instalado correctamente")])

    # 5. Instalando paquetes para Lua
    color_print([("cyan", "⚡ Instalando paquetes Lua...")])
    if not install_luapack():
        color_print([("red", "❌ No se pudo instalar paquetes para Lua")])
        return
    color_print([("green", "✓ Paquetes Lua instalados correctamente")])

    # 6. Configurar Docker
    color_print([("cyan", "⚡ Configurando Docker...")])
    if not configurar_docker():
        color_print([("red", "❌ No se pudo configurar Docker")])
    color_print([("green", "✓ Docker configurado correctamente")])

    # 7. Instalar Lazygit
    color_print([("cyan", "⚡ Instalando Lazygit...")])
    if not install_lazygit():
        color_print([("red", "❌ No se pudo Instalar Lazygit")])
    color_print([("green", "✓ Lazygit instalado correctamente")])

    # 8. Instalar d2
    color_print([("cyan", "⚡ Ejecutando post-instalaciones...")])
    if not install_post_install():
        color_print([("red", "❌ No se pudo ejecutar las post-instalaciones")])
    color_print([("green", "✓ Las post-instalaciones se ejecutaron correctamente")])

    # TODO: Faltan las post-instalaciones

    # 99. Instalar dotfiles
    color_print([("cyan", "⚡ Instalando dotfiles...")])
    if not install_dot():
        color_print([("red", "❌ No se pudo instalar dotfiles")])
        return
    color_print([("green", "✓ dotfiles instalados correctamente")])

    # Mensaje final de éxito
    color_print(
        [
            (
                "green",
                "✨ Todas las instalaciones y configuraciones se completaron con éxito!",
            )
        ]
    )

    logo("🎉 Fase 2 completada exitosamente")


def main():
    # Mostrar el logo personalizado
    logo("💾 Post Instalación - 2da Fase")

    # Preguntar al usuario si desea continuar
    action = inquirer.select(
        message="¿Deseas continuar con la Fase 2 o salir?",
        choices=[
            "Continuar con la Fase 2",
            "Salir",
        ],
    ).execute()

    # Procesar la elección del usuario
    if action == "Continuar con la Fase 2":
        print("Iniciando la Fase 2...")
        color_print([("cyan", "⚡ Iniciando la Fase 2 de instalación...")])
        fase2()
    else:
        print("Saliendo del instalador. ¡Hasta luego!")
        exit(0)


if __name__ == "__main__":
    main()
