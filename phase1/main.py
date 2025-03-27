import json

from common.flatpak_installer import install_flatpak
from common.logger_utils import setup_logger
from common.logo import show as logo
from common.system_info import SystemInfo
from common.system_operations import (
    read_file,
    run_step,
)

logger = setup_logger()


def main():
    # Mostrar el logo de inicio
    logo("💾 Post Instalación - 1ra Fase")
    logger.info("Iniciando fase 1 (Bootstrap)...")

    # Detectar sistema operativo
    system_info = SystemInfo()
    # Cargar la configuración del instalador
    config_path = "common/installer_config.json"
    config_data = json.loads(read_file(config_path))

    # Obtener los pasos de la fase 1
    phase_1_steps = config_data.get("phase_1", {}).get("steps", [])

    # Ejecutar cada paso
    for step in phase_1_steps:
        if not run_step(step, system_info, config_data):
            logger.error(f"Error al ejecutar el paso: {step.get('task')}")
            return

    # instalar flatpak
    if not install_flatpak(system_info, config_data):
        logger.error("No se pudo instalar Flatpak")

    logo("🎉 Fase 1 completada exitosamente")
    print("Recuerda reiniciar el terminal")
    print("Te recuerdo configurar una fuente Nertfonts para mejor experiencia")


if __name__ == "__main__":
    main()
