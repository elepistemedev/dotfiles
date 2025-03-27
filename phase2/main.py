import json
from InquirerPy import inquirer
from common.logo import show as logo
from common.system_info import SystemInfo
from common.system_operations import (
    run_step,
    read_file
)
from InquirerPy.utils import color_print
from common.install_dotfiles import install_dot
from common.logger_utils import setup_logger

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
    
    logger = setup_logger()
    # Cargar la configuración del instalador
    config_path = "common/installer_config.json"
    config_data = json.loads(read_file(config_path))

    # Obtener los pasos de la fase 2
    phase_2_steps = config_data.get("phase_2", {}).get("steps", [])

    # Ejecutar cada paso
    for step in phase_2_steps:
        if not run_step(step, system_info, config_data):
            logger.error(f"Error al ejecutar el paso: {step.get('task')}")
            return
        
    logo("🎉 Fase 2 completada exitosamente")


def main():
    # Mostrar el logo personalizado
    logo("💾 Post Instalación - 2da Fase")

    # Preguntar al usuario si desea continuar
    action = inquirer.select(  # type: ignore
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
