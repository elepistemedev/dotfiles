from InquirerPy import inquirer
from common.logo import show as logo
from common.system_info import SystemInfo
from common.system_operations import (
    update_system,
    install_dependencies,
    install_lazyvim,
    configurar_docker,
    install_luapack,
)
from InquirerPy.utils import color_print


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
        return
    color_print([("green", "✓ Docker configurado correctamente")])

    # Mensaje final de éxito
    color_print(
        [
            (
                "green",
                "✨ Todas las instalaciones y configuraciones se completaron con éxito!",
            )
        ]
    )


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
