import logging
import os
from pathlib import Path
import shutil
from subprocess import CalledProcessError, run
import sys
import tempfile
from urllib.error import URLError
import urllib.request
import zipfile

from dotenv import load_dotenv
from rich.console import Console
import typer

# Configuración básica del logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

RYE_INSTALL_URL = "https://rye-up.com/install"
RYE_EXECUTABLE = "rye"

# Inicializar la aplicación Typer
app = typer.Typer()

# Inicializar la consola de rich
console = Console()


def is_rye_installed() -> bool:
    """Verifica si Rye está instalado en el sistema."""
    try:
        run([RYE_EXECUTABLE, "--version"], check=True, capture_output=True)
        return True
    except FileNotFoundError:
        return False
    except CalledProcessError:
        return False


def install_rye() -> None:
    """Instala Rye en el sistema."""
    console.print("[bold blue]Rye no está instalado. Procediendo con la instalación...[/bold blue]")
    try:
        with urllib.request.urlopen(RYE_INSTALL_URL) as response:
            install_script = response.read().decode("utf-8")

        # Guardar el script de instalación en un archivo temporal
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".sh") as tmp_file:
            tmp_file.write(install_script)
            install_script_path = tmp_file.name

        # Ejecutar el script de instalación
        console.print(
            f"[bold green]Ejecutando script de instalación de Rye desde:[/bold green] [italic]{install_script_path}[/italic]"
        )
        run(["sh", install_script_path], check=True)
        console.print("[bold green]Instalación de Rye completada.[/bold green] Asegúrate de que esté en tu PATH.")
        console.print("\n[bold red]********************************************************************[/bold red]")
        console.print("[bold red]¡Importante! Es posible que necesites cerrar y volver a abrir tu terminal[/bold red]")
        console.print("[bold red]para que Rye esté disponible en tu PATH.[/bold red]")
        console.print("[bold red]********************************************************************[/bold red]\n")
    except URLError as e:
        console.print(
            f"[bold red]Error al descargar el script de instalación de Rye desde[/bold red] [italic]{RYE_INSTALL_URL}[/italic]: [bold]{e}[/bold]",
            style="red",
        )
        sys.exit(1)
    except CalledProcessError as e:
        console.print(
            f"[bold red]Error al ejecutar el script de instalación de Rye:[/bold red] [bold]{e}[/bold]", style="red"
        )
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Error inesperado al instalar Rye:[/bold red] [bold]{e}[/bold]", style="red")
        sys.exit(1)
    finally:
        if "install_script_path" in locals() and os.path.exists(install_script_path):
            os.remove(install_script_path)


def download_and_extract(repo_url: str, temp_dir: Path) -> Path:
    """Descarga y extrae el repositorio en un directorio temporal."""
    zip_path = temp_dir / "repo.zip"
    try:
        console.print("[bold blue]Descargando repositorio...[/bold blue]")
        urllib.request.urlretrieve(repo_url, zip_path)
        console.print(f"[bold green]Repositorio descargado correctamente en:[/bold green] [italic]{zip_path}[/italic]")

        console.print("[bold blue]Extrayendo archivos...[/bold blue]")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(temp_dir)
        extracted_path = temp_dir
        console.print(
            f"[bold green]Archivos extraídos correctamente en:[/bold green] [italic]{extracted_path}[/italic]"
        )
        return extracted_path
    except URLError as e:
        console.print(
            f"[bold red]Error al descargar el repositorio desde[/bold red] [italic]{repo_url}[/italic]: [bold]{e}[/bold]",
            style="red",
        )
        sys.exit(1)
    except zipfile.BadZipFile:
        console.print(
            "[bold red]El archivo descargado no es un archivo ZIP válido:[/bold red] [bold]{e}[/bold]", style="red"
        )
        sys.exit(1)
    except Exception as e:
        console.print(
            f"[bold red]Error inesperado al descargar o extraer el repositorio:[/bold red] [bold]{e}[/bold]",
            style="red",
        )
        sys.exit(1)


def execute_phase1(temp_dir: Path) -> None:
    """Ejecuta el script de la primera fase desde el directorio temporal."""
    main_script = temp_dir / "dotfiles-dev" / "phase1" / "main.py"
    project_root = temp_dir / "dotfiles-dev"

    console.print(f"[bold blue]Buscando archivo main.py en:[/bold blue] [italic]{main_script}[/italic]")
    if not main_script.exists():
        console.print(f"[bold red]El archivo main.py no existe en:[/bold red] [italic]{main_script}[/italic]")
        sys.exit(1)

    console.print("[bold blue]Ejecutando Fase 1 desde el directorio temporal...[/bold blue]")
    try:
        # Agregar el directorio raíz del proyecto al PYTHONPATH
        env = dict(PYTHONPATH=str(project_root), **os.environ)
        run([sys.executable, str(main_script)], check=True, env=env)
        console.print("[bold green]Fase 1 ejecutada correctamente.[/bold green]")
    except FileNotFoundError:
        console.print("[bold red]El ejecutable de Python no se encontró.[/bold red]")
        sys.exit(1)
    except CalledProcessError as e:
        console.print(f"[bold red]Error durante la ejecución de Fase 1:[/bold red] [bold]{e}[/bold]", style="red")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Error inesperado al ejecutar Fase 1:[/bold red] [bold]{e}[/bold]", style="red")
        sys.exit(1)


def execute_phase2(temp_dir: Path) -> None:
    """
    Ejecuta el script de la segunda fase desde el directorio temporal usando Rye.
    """
    main_script = temp_dir / "dotfiles-dev" / "phase2" / "main.py"
    project_root = temp_dir / "dotfiles-dev"

    console.print(f"[bold blue]Buscando archivo main.py para Fase 2 en:[/bold blue] [italic]{main_script}[/italic]")
    if not main_script.exists():
        console.print(
            f"[bold red]El archivo main.py para Fase 2 no existe en:[/bold red] [italic]{main_script}[/italic]"
        )
        sys.exit(1)

    console.print("[bold blue]Ejecutando Fase 2 desde el directorio temporal usando Rye...[/bold blue]")
    try:
        # Asegurarse de que estamos en el directorio del proyecto para ejecutar comandos de Rye
        phase2_dir = temp_dir / "dotfiles-dev" / "phase2"
        os.chdir(phase2_dir)
        logging.info(f"Cambiando el directorio de trabajo a: {phase2_dir}")

        # Inicializar Rye si no está inicializado
        if not (phase2_dir / "pyproject.toml").exists():
            console.print("[bold blue]Inicializando Rye en el directorio de la Fase 2...[/bold blue]")
            run([RYE_EXECUTABLE, "init", "--no-input"], check=True)
            console.print("[bold green]Rye inicializado.[/bold green]")

        # Sincronizar las dependencias (si las hay)
        if (phase2_dir / "pyproject.toml").exists():
            console.print("[bold blue]Sincronizando dependencias de Rye para la Fase 2...[/bold blue]")
            run([RYE_EXECUTABLE, "sync"], check=True)
            console.print("[bold green]Dependencias de Rye sincronizadas.[/bold green]")

        # Ejecutar el script de la Fase 2 usando Rye
        run([RYE_EXECUTABLE, "run", "python", str(main_script.relative_to(phase2_dir))], check=True)
        console.print("[bold green]Fase 2 ejecutada correctamente.[/bold green]")

    except FileNotFoundError:
        console.print("[bold red]El ejecutable de Python o Rye no se encontraron.[/bold red]")
        sys.exit(1)
    except CalledProcessError as e:
        console.print(f"[bold red]Error durante la ejecución de la Fase 2:[/bold red] [bold]{e}[/bold]", style="red")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Error inesperado al ejecutar la Fase 2:[/bold red] [bold]{e}[/bold]", style="red")
        sys.exit(1)
    finally:
        # Volver al directorio temporal principal
        os.chdir(temp_dir)


@app.command()
def bootstrap(
    repo_url: str = typer.Option(None, help="URL del repositorio ZIP a descargar."),
    start_phase1: bool = typer.Option(False, "--phase1", help="Ejecutar solo la Fase 1."),
    start_phase2: bool = typer.Option(False, "--phase2", help="Ejecutar solo la Fase 2."),
):
    """
    Herramienta para la instalación y configuración inicial del sistema.

    Descarga un repositorio ZIP, instala Rye si es necesario, y ejecuta las fases de configuración.

    Args:
        repo_url (str, opcional): URL del repositorio ZIP a descargar. Si no se proporciona, se intenta leer desde el archivo .env.
        start_phase1 (bool, opcional): Si se establece, solo se ejecuta la Fase 1. Por defecto es False.
        start_phase2 (bool, opcional): Si se establece, solo se ejecuta la Fase 2. Por defecto es False.
    """
    console.print("[bold blue]Iniciando instalación y configuración...[/bold blue]")
    temp_dir = Path(tempfile.mkdtemp(prefix="bootstrap_phase1_"))
    console.print(f"[bold green]Directorio temporal creado:[/bold green] [italic]{temp_dir}[/italic]")

    try:
        # Paso 1: Determinar la URL del repositorio
        final_repo_url = repo_url if repo_url else os.getenv("REPO_URL")
        if not final_repo_url:
            console.print(
                "[bold red]Error: No se proporcionó la URL del repositorio ni se encontró en el archivo .env[/bold red]",
                style="red",
            )
            sys.exit(1)
        console.print(f"[bold blue]Usando URL del repositorio:[/bold blue] [italic]{final_repo_url}[/italic]")

        # Paso 2: Descargar y extraer el repositorio
        extracted_path = download_and_extract(final_repo_url, temp_dir)

        # Paso 3: Verificar e instalar Rye si es necesario
        if not is_rye_installed():
            install_rye()
        else:
            console.print("[bold green]Rye ya está instalado.[/bold green]")

        # Paso 4: Ejecutar las fases según las opciones
        if start_phase1:
            console.print("[bold blue]Ejecutando solo la Fase 1...[/bold blue]")
            execute_phase1(extracted_path)
        elif start_phase2:
            console.print("[bold blue]Ejecutando solo la Fase 2...[/bold blue]")
            execute_phase2(extracted_path)
        else:
            console.print("[bold blue]Ejecutando Fase 1 y Fase 2...[/bold blue]")
            execute_phase1(extracted_path)
            execute_phase2(extracted_path)

    finally:
        # Limpieza del directorio temporal
        console.print(f"[bold blue]Limpiando el directorio temporal:[/bold blue] [italic]{temp_dir}[/italic]")
        shutil.rmtree(temp_dir, ignore_errors=True)
        console.print("[bold green]Directorio temporal eliminado. Proceso completado.[/bold green]")


if __name__ == "__main__":
    app()
