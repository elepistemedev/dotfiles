from shared.logger_utils import setup_logger
from shared.system_info import SystemInfo
from shared.system_operations import update_system, install_dependencies
from shared.logo import show as logo

logger = setup_logger()


def main():
    logo("💾 Post Instalación - 1ra Fase")
    logger.info("Iniciando fase 1 (Bootstrap)...")

    # Detectar sistema operativo
    system_info = SystemInfo()
    logger.info(f"Sistema detectado: {system_info.system}")
    if system_info.distribution:
        logger.info(f"Distribución: {system_info.distribution} {system_info.version}")
        logger.info(f"Gestor de paquetes: {system_info.package_manager}")

    # Actualizar sistema
    if not update_system(system_info):
        logger.error("No se pudo actualizar el sistema")
        return

    # Instalar dependencias básicas
    if not install_dependencies(system_info):
        logger.error("No se pudieron instalar las dependencias")
        return

    logger.info("\n=== Fase 1 completada exitosamente ===")


if __name__ == "__main__":
    main()
