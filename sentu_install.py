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

RYE_INSTALL_URL = "https://rye.astral.sh/get"
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
    """Instala Rye en el sistema usando el método recomendado."""
    print("\033[1m\033[94mRye no está instalado. Procediendo con la instalación...\033[0m")
    try:
        install_command = f"curl -sSf {RYE_INSTALL_URL} | bash"
        print(f"\033[1m\033[92mEjecutando comando para instalar Rye:\033[0m \033[3m{install_command}\033[0m")
        run(install_command, shell=True, check=True)
        print("\033[1m\033[92mInstalación de Rye completada.\033[0m Asegúrate de que esté en tu PATH.")
        print("\n\033[1m\033[91m********************************************************************\033[0m")
        print("\033[1m\033[91m¡Importante! Es posible que necesites cerrar y volver a abrir tu terminal\033[0m")
        print("\033[1m\033[91mpara que Rye esté disponible en tu PATH.\033[0m")
        print("\033[1m\033[91m********************************************************************\033[0m\n")
    except CalledProcessError as e:
        print(f"\033[1m\033[91mError al ejecutar el comando de instalación de Rye:\033[0m \033[1m{e}\033[0m")
        sys.exit(1)
    except Exception as e:
        print("\033[1m\033[91mError inesperado al instalar Rye:\033[0m")
        print(e)
        sys.exit(1)


def download_and_extract(repo_url: str, temp_dir: Path) -> Path:
    """Descarga y extrae el repositorio en un directorio temporal."""
    zip_path = temp_dir / "repo.zip"
    try:
        print("\033[1m\033[94mDescargando repositorio...\033[0m")
        urllib.request.urlretrieve(repo_url, zip_path)
        print(f"\033[1m\033[92mRepositorio descargado correctamente en:\033[0m \033[3m{zip_path}\033[0m")

        print("\033[1m\033[94mExtrayendo archivos...\033[0m")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(temp_dir)
        extracted_path = temp_dir
        print(f"\033[1m\033[92mArchivos extraídos correctamente en:\033[0m \033[3m{extracted_path}\033[0m")
        return extracted_path
    except URLError as e:
        print(
            f"\033[1m\033[91mError al descargar el repositorio desde\033[0m \033[3m{repo_url}\033[0m: \033[1m{e}\033[0m",
        )
        sys.exit(1)
    except zipfile.BadZipFile:
        print(
            "\033[1m\033[91mEl archivo descargado no es un archivo ZIP válido:\033[0m \033[1m{e}\033[0m",
        )
        sys.exit(1)
    except Exception as e:
        print(
            "\033[1m\033[91mError inesperado al descargar o extraer el repositorio:\033[0m",
        )
        print(e)
        sys.exit(1)


def execute_phase1(temp_dir: Path) -> None:
    """Ejecuta el script de la primera fase desde el directorio temporal."""
    main_script = temp_dir / "dotfiles-dev" / "phase1" / "main.py"
    project_root = temp_dir / "dotfiles-dev"

    print(f"\033[1m\033[94mBuscando archivo main.py en:\033[0m \033[3m{main_script}\033[0m")
    if not main_script.exists():
        print(f"\033[1m\033[91mEl archivo main.py no existe en:\033[0m \033[3m{main_script}\033[0m")
        sys.exit(1)

    print("\033[1m\033[94mEjecutando Fase 1 desde el directorio temporal...\033[0m")
    try:
        # Agregar el directorio raíz del proyecto al PYTHONPATH
        env = dict(PYTHONPATH=str(project_root), **os.environ)
        run([sys.executable, str(main_script)], check=True, env=env)
        print("\033[1m\033[92mFase 1 ejecutada correctamente.\033[0m")
    except FileNotFoundError:
        print("\033[1m\033[91mEl ejecutable de Python no se encontró.\033[0m")
        sys.exit(1)
    except CalledProcessError as e:
        print(
            "\033[1m\033[91mError durante la ejecución de Fase 1:\033[0m",
        )
        print(e)
        sys.exit(1)
    except Exception as e:
        print(
            "\033[1m\033[91mError inesperado al ejecutar Fase 1:\033[0m",
        )
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    # Simular la consola de rich con prints formateados (muy básico)
    class SimpleConsole:
        def print(self, text):
            if "[bold" in text:
                text = text.replace("[bold", "\033[1m")
            if "[/bold]" in text:
                text = text.replace("[/bold]", "\033[0m")
            if "[blue]" in text:
                text = text.replace("[blue]", "\033[94m")
            if "[/blue]" in text:
                text = text.replace("[/blue]", "\033[0m")
            if "[green]" in text:
                text = text.replace("[green]", "\033[92m")
            if "[/green]" in text:
                text = text.replace("[/green]", "\033[0m")
            if "[red]" in text:
                text = text.replace("[red]", "\033[91m")
            if "[/red]" in text:
                text = text.replace("[/red]", "\033[0m")
            if "[yellow]" in text:
                text = text.replace("[yellow]", "\033[93m")
            if "[/yellow]" in text:
                text = text.replace("[/yellow]", "\033[0m")
            if "[italic]" in text:
                text = text.replace("[italic]", "\033[3m")
            if "[/italic]" in text:
                text = text.replace("[/italic]", "\033[0m")
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
