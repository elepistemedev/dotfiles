from common.logger_utils import setup_logger
from common.system_info import SystemInfo
from system_operations import (
    update_system,
    install_dependencies,
    install_and_configure_zsh,
    clone_repo,
    setup_anaconda,
    install_python_packages,
    install_prompt,
)
from common.logo import show as logo

logger = setup_logger()


def main():
    logo("💾 Post Instalación - 1ra Fase")
    logger.info("Iniciando fase 1 (Bootstrap)...")

    # 1. Detectar sistema operativo
    system_info = SystemInfo()
    logger.info(f"Sistema detectado: {system_info.system}")
    if system_info.distribution:
        logger.info(f"Distribución: {system_info.distribution} {system_info.version}")
        logger.info(f"Gestor de paquetes: {system_info.package_manager}")

    # 2. Actualizar sistema
    if not update_system(system_info):
        logger.error("No se pudo actualizar el sistema")
        return

    # 3 Instalar dependencias básicas
    if not install_dependencies(system_info):
        logger.error("No se pudieron instalar las dependencias")
        return

    # 4. Instalar y configurar zsh
    if not install_and_configure_zsh():
        logger.error("No se pudo instalar/configurar zsh")
        return

    # 5. Clonar repositorio desde github
    if not clone_repo():
        logger.error("No se pudo clonar el repositorio desde github")
        return

    # 6. Instalar Anaconda
    if not setup_anaconda():
        logger.error("No se pudo instalar Anaconda")
        return

    # 7. Instalar paquetes Python necesarios
    if not install_python_packages():
        logger.error("No se pudieron instalar los paquetes Python")
        return

    # 8. Instalar prompt Starship
    if not install_prompt():
        logger.error("No se pudo instalar el prompt Starship")
        return

    # TODO: Falta instalar Node
    # TODO: Falta instalar rust
    # TODO: Falta instalar go

    logo("🎉 Fase 1 completada exitosamente")


if __name__ == "__main__":
    main()
