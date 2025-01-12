# BUG: Eliminar este archivo
from rich.panel import Panel
from rich import console
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TimeElapsedColumn,
)
from rich.prompt import Prompt
import questionary
from pathlib import Path
import subprocess
import json
import sys

console = Console()

# Definición de aplicaciones disponibles
AVAILABLE_APPS = {
    "Desarrollo": {
        "visual-studio-code": "Editor de código",
        "sublime-text": "Editor de texto",
        "docker": "Containerización",
        "postman": "Cliente API REST",
        "git-kraken": "Cliente Git GUI",
    },
    "Internet": {
        "firefox": "Navegador web Firefox",
        "chrome": "Navegador web Chrome",
        "thunderbird": "Cliente de correo",
    },
    "Utilidades": {
        "vlc": "Reproductor multimedia",
        "obs-studio": "Software de streaming",
        "timeshift": "Copias de seguridad",
        "htop": "Monitor del sistema",
    },
    "Productividad": {
        "libreoffice": "Suite ofimática",
        "dropbox": "Almacenamiento en la nube",
        "notion": "Toma de notas",
    },
}


def show_welcome():
    """Muestra un mensaje de bienvenida"""
    console.print(
        Panel.fit(
            "[bold blue]Bienvenido a la Fase 2 de la Configuración del Sistema[/]\n\n"
            "Este asistente te ayudará a instalar y configurar las aplicaciones que necesitas.\n"
            "Por favor, sigue las instrucciones en pantalla.",
            title="🚀 Configuración del Sistema",
            border_style="blue",
        )
    )


def get_package_manager():
    """Determina el gestor de paquetes del sistema"""
    # Implementar la lógica de detección del gestor de paquetes
    # Similar a la fase 1
    pass


def select_applications():
    """Permite al usuario seleccionar las aplicaciones a instalar"""
    selected_apps = []

    console.print("\n[bold cyan]Selección de Aplicaciones[/]")

    for category, apps in AVAILABLE_APPS.items():
        console.print(f"\n[yellow]{category}:[/]")

        choices = [
            questionary.Checkbox(
                f"Selecciona las aplicaciones de {category}:",
                choices=[
                    questionary.Choice(f"{name} - {description}", value=name)
                    for name, description in apps.items()
                ],
            )
        ]

        result = questionary.prompt(choices)
        if result:
            selected_apps.extend(result[f"Selecciona las aplicaciones de {category}:"])

    return selected_apps


def install_applications(apps):
    """Instala las aplicaciones seleccionadas con barra de progreso"""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Instalando aplicaciones...", total=len(apps))

        for app in apps:
            progress.update(task, description=f"[cyan]Instalando {app}...")
            # Aquí iría la lógica real de instalación
            # Simular instalación para el ejemplo
            import time

            time.sleep(2)
            progress.advance(task)


def main():
    show_welcome()

    try:
        # Seleccionar aplicaciones
        console.print("\n[bold green]Paso 1:[/] Selección de aplicaciones")
        selected_apps = select_applications()

        if not selected_apps:
            console.print("[yellow]No se seleccionaron aplicaciones.[/]")
            return

        # Confirmar selección
        console.print("\n[bold]Aplicaciones seleccionadas:[/]")
        for app in selected_apps:
            console.print(f"  ✓ {app}")

        if questionary.confirm("¿Deseas proceder con la instalación?").ask():
            # Instalar aplicaciones
            console.print("\n[bold green]Paso 2:[/] Instalando aplicaciones")
            install_applications(selected_apps)

            console.print("\n[bold green]¡Instalación completada![/]")
        else:
            console.print("\n[yellow]Instalación cancelada.[/]")

    except KeyboardInterrupt:
        console.print("\n[red]Proceso cancelado por el usuario.[/]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]Error: {str(e)}[/]")
        sys.exit(1)


if __name__ == "__main__":
    main()
