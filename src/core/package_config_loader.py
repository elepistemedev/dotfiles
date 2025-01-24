import os
from pathlib import Path
from typing import Any, ClassVar, Optional

import yaml


class PackageManagerConfigLoader:
    """
    Gestor de configuraciones de gestores de paquetes por distribución.

    Carga y proporciona configuraciones desde archivos YAML.
    """

    _configs: ClassVar[dict[str, dict[str, Any]]] = {}
    _config_dir: str = "config/package_managers"

    @classmethod
    def load_configs(cls, config_dir: Optional[str] = None) -> None:
        """
        Carga configuraciones YAML de gestores de paquetes.

        Args:
            config_dir: Ruta al directorio de configuraciones (opcional)
        """
        # Usar directorio por defecto o el proporcionado
        load_dir = config_dir or cls._config_dir

        # Asegurar ruta absoluta
        config_path = Path(os.path.join(os.getcwd(), load_dir))

        # Cargar cada archivo YAML
        for yaml_file in config_path.glob("*.yaml"):
            distribution = yaml_file.stem
            try:
                with open(str(yaml_file), encoding="utf-8") as f:
                    cls._configs[distribution] = yaml.safe_load(f)
            except (OSError, yaml.YAMLError) as e:
                print(f"Error cargando configuración {distribution}: {e}")

    @classmethod
    def get_config(cls, distribution: str) -> dict[str, Any]:
        """
        Obtiene configuración para una distribución específica.

        Args:
            distribution: Nombre de la distribución

        Returns:
            Configuración del gestor de paquetes
        """
        # Cargar configuraciones si aún no se han cargado
        if not cls._configs:
            cls.load_configs()

        return cls._configs.get(distribution, {})


# Cargar configuraciones al importar
PackageManagerConfigLoader.load_configs()
