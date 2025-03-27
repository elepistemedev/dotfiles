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

# Configuración básica del logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# URL por defecto en caso de que no se encuentre en .env (ahora hardcodeada para simplicidad)
DEFAULT_REPO_URL = "https://github.com/elepistemedev/dotfiles/archive/refs/heads/feature/better_man.zip"

RYE_INSTALL_URL = "https://rye-up.com/install"
RYE_EXECUTABLE = "rye"


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
    print("[bold blue]Rye no está instalado. Procediendo con la instalación...[/bold blue]")
    try:
        with urllib.request.urlopen(RYE_INSTALL_URL) as response:
            install_script = response.read().decode("utf-8")

        # Guardar el script de instalación en un archivo temporal
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".sh") as tmp_file:
            tmp_file.write(install_script)
            install_script_path = tmp_file.name

        # Ejecutar el script de instalación
        print(
            f"[bold green]Ejecutando script de instalación de Rye desde:[/bold green] [italic]{install_script_path}[/italic]"
        )
        run(["sh", install_script_path], check=True)
        print("[bold green]Instalación de Rye completada.[/bold green] Asegúrate de que esté en tu PATH.")
        print("\n[bold red]********************************************************************[/bold red]")
        print("[bold red]¡Importante! Es posible que necesites cerrar y volver a abrir tu terminal[/bold red]")
        print("[bold red]para que Rye esté disponible en tu PATH.[/bold red]")
        print("[bold red]********************************************************************[/bold red]\n")
    except URLError as e:
        print(
            f"[bold red]Error al descargar el script de instalación de Rye desde[/bold red] [italic]{RYE_INSTALL_URL}[/italic]: [bold]{e}[/bold]",
            style="red",
        )
        sys.exit(1)
    except CalledProcessError as e:
        print(f"[bold red]Error al ejecutar el script de instalación de Rye:[/bold red] [bold]{e}[/bold]", style="red")
        sys.exit(1)
    except Exception as e:
        print("[bold red]Error inesperado al instalar Rye:[/bold red]", style="red")
        print(e)
        sys.exit(1)
    finally:
        if "install_script_path" in locals() and os.path.exists(install_script_path):
            os.remove(install_script_path)


def download_and_extract(repo_url: str, temp_dir: Path) -> Path:
    """Descarga y extrae el repositorio en un directorio temporal."""
    zip_path = temp_dir / "repo.zip"
    try:
        print("[bold blue]Descargando repositorio...[/bold blue]")
        urllib.request.urlretrieve(repo_url, zip_path)
        print(f"[bold green]Repositorio descargado correctamente en:[/bold green] [italic]{zip_path}[/italic]")

        print("[bold blue]Extrayendo archivos...[/bold blue]")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(temp_dir)
        extracted_path = temp_dir
        print(f"[bold green]Archivos extraídos correctamente en:[/bold green] [italic]{extracted_path}[/italic]")
        return extracted_path
    except URLError as e:
        print(
            f"[bold red]Error al descargar el repositorio desde[/bold red] [italic]{repo_url}[/italic]: [bold]{e}[/bold]",
            style="red",
        )
        sys.exit(1)
    except zipfile.BadZipFile:
        print("[bold red]El archivo descargado no es un archivo ZIP válido:[/bold red] [bold]{e}[/bold]", style="red")
        sys.exit(1)
    except Exception as e:
        print(
            "[bold red]Error inesperado al descargar o extraer el repositorio:[/bold red]",
            style="red",
        )
        print(e)
        sys.exit(1)


def execute_phase1(temp_dir: Path) -> None:
    """Ejecuta el script de la primera fase desde el directorio temporal."""
    main_script = temp_dir / "dotfiles-dev" / "phase1" / "main.py"
    project_root = temp_dir / "dotfiles-dev"

    print(f"[bold blue]Buscando archivo main.py en:[/bold blue] [italic]{main_script}[/italic]")
    if not main_script.exists():
        print(f"[bold red]El archivo main.py no existe en:[/bold red] [italic]{main_script}[/italic]")
        sys.exit(1)

    print("[bold blue]Ejecutando Fase 1 desde el directorio temporal...[/bold blue]")
    try:
        # Agregar el directorio raíz del proyecto al PYTHONPATH
        env = dict(PYTHONPATH=str(project_root), **os.environ)
        run([sys.executable, str(main_script)], check=True, env=env)
        print("[bold green]Fase 1 ejecutada correctamente.[/bold green]")
    except FileNotFoundError:
        print("[bold red]El ejecutable de Python no se encontró.[/bold red]")
        sys.exit(1)
    except CalledProcessError as e:
        print("[bold red]Error durante la ejecución de Fase 1:[/bold red]", style="red")
        print(e)
        sys.exit(1)
    except Exception as e:
        print("[bold red]Error inesperado al ejecutar Fase 1:[/bold red]", style="red")
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    # Simular la consola de rich con prints formateados (muy básico)
    class SimpleConsole:
        def print(self, text, style=None):
            if "[bold" in text:
                text = text.replace("[bold", "\033[1m")
            if "[/bold]" in text:
                text = text.replace("[/bold]", "\033[0m")
            if "[blue]" in text:
                text = text.replace("[blue]", "\033[94m")
            if "[green]" in text:
                text = text.replace("[green]", "\033[92m")
            if "[red]" in text:
                text = text.replace("[red]", "\033[91m")
            if "[yellow]" in text:
                text = text.replace("[yellow]", "\033[93m")
            if "[italic]" in text:
                text = text.replace("[italic]", "\033[3m")
            if "[/italic]" in text:
                text = text.replace("[/italic]", "\033[0m")
            if "[/blue]" in text:
                text = text.replace("[/blue]", "\033[0m")
            if "[/green]" in text:
                text = text.replace("[/green]", "\033[0m")
            if "[/red]" in text:
                text = text.replace("[/red]", "\033[0m")
            if "[/yellow]" in text:
                text = text.replace("[/yellow]", "\033[0m")
            print(text)

    console = SimpleConsole()

    console.print("[bold blue]Ejecutando instalación de Fase 1 desde curl...[/bold blue]")

    # Verificar e instalar Rye si es necesario
    if not is_rye_installed():
        install_rye()
    else:
        console.print("[bold green]Rye ya está instalado.[/bold green]")

    repo_url_direct = DEFAULT_REPO_URL
    console.print(f"[bold blue]Usando URL del repositorio:[/bold blue] [italic]{repo_url_direct}[/italic]")

    temp_dir_direct = Path(tempfile.mkdtemp(prefix="direct_install_"))
    console.print(f"[bold green]Directorio temporal creado:[/bold green] [italic]{temp_dir_direct}[/italic]")
    extracted_path_direct = download_and_extract(repo_url_direct, temp_dir_direct)

    console.print("[bold blue]Ejecutando Fase 1...[/bold blue]")
    execute_phase1(extracted_path_direct)

    # Limpieza del directorio temporal
    console.print(f"[bold blue]Limpiando el directorio temporal:[/bold blue] [italic]{temp_dir_direct}[/italic]")
    shutil.rmtree(temp_dir_direct, ignore_errors=True)
    console.print("[bold green]Directorio temporal eliminado.[/bold green]")
    sys.exit(0)
