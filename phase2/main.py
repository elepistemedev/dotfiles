from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from common.logo import show as logo

# Crear una consola para imprimir mensajes enriquecidos
console = Console()


def main():
    # Mostrar el logo en un panel con Rich
    logo("💾 Post Instalación - 2da Fase")

    # Preguntar al usuario si desea continuar
    console.print("[bold blue]¿Qué deseas hacer?[/bold blue]", style="bold")
    action = Prompt.ask(
        "[cyan]Selecciona una opción[/cyan]",
        choices=["Continuar", "Salir"],
        default="Continuar",
    )

    # Procesar la elección del usuario
    if action == "Continuar":
        console.print("[bold green]Iniciando la Fase 2...[/bold green]")
        # Aquí puedes llamar a las funciones de la Fase 2
    else:
        console.print("[bold red]Saliendo del instalador. ¡Hasta luego![/bold red]")
        exit(0)


if __name__ == "__main__":
    main()
