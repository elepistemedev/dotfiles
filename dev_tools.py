#!/usr/bin/env python3
import typer
import subprocess
import os
from typing import Optional
from enum import Enum

# Definimos las distribuciones soportadas como una enumeración
class Distribucion(str, Enum):
    FEDORA = "fedora"
    UBUNTU = "ubuntu"
    ARCH = "archlinux"

# Creamos la aplicación Typer
app = typer.Typer(help="Gestor de contenedores Docker")

def ejecutar_comando(comando: str) -> None:
    """
    Ejecuta un comando de shell y maneja posibles errores
    """
    try:
        subprocess.run(comando, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        typer.echo(f"Error ejecutando el comando: {e}")
        raise typer.Exit(1)

@app.command()
def listar_contenedores(todos: bool = typer.Option(False, "--todos", "-a", help="Mostrar todos los contenedores, incluso los detenidos")):
    """
    Lista los contenedores activos o todos los contenedores
    """
    comando = "docker ps" + (" -a" if todos else "")
    ejecutar_comando(comando)

@app.command()
def detener_contenedor(container_id: str):
    """
    Detiene un contenedor específico
    """
    ejecutar_comando(f"docker stop {container_id}")

@app.command()
def eliminar_contenedor(container_id: str, forzar: bool = typer.Option(False, "--forzar", "-f", help="Forzar eliminación")):
    """
    Elimina un contenedor específico
    """
    comando = f"docker rm {'-f' if forzar else ''} {container_id}"
    ejecutar_comando(comando)

@app.command()
def listar_volumenes():
    """
    Lista todos los volúmenes Docker
    """
    ejecutar_comando("docker volume ls")

@app.command()
def inspeccionar_volumen(nombre: str):
    """
    Inspecciona un volumen específico
    """
    ejecutar_comando(f"docker volume inspect {nombre}")

@app.command()
def eliminar_volumen(nombre: str):
    """
    Elimina un volumen específico
    """
    ejecutar_comando(f"docker volume rm {nombre}")

@app.command()
def limpiar_volumenes():
    """
    Elimina todos los volúmenes no utilizados
    """
    ejecutar_comando("docker volume prune -f")

@app.command()
def ejecutar_contenedor(
    distribucion: Distribucion,
    nombre: Optional[str] = typer.Option(None, "--nombre", "-n", help="Nombre del contenedor"),
    volumen: Optional[str] = typer.Option(None, "--volumen", "-v", help="Nombre del volumen")
):
    """
    Ejecuta un contenedor con la configuración especificada
    """
    # Comandos específicos para cada distribución
    comandos_dist = {
        Distribucion.FEDORA: "dnf install -y shadow-utils util-linux sudo python3",
        Distribucion.UBUNTU: "apt-get update && apt-get install -y sudo python3",
        Distribucion.ARCH: "pacman -Syu --noconfirm && pacman -S --noconfirm shadow util-linux sudo python3"
    }

    nombre_cont = nombre or f"mi-{distribucion.value}"
    volumen_mount = f"-v {volumen}:/home" if volumen else ""
    
    comando = f"""
    docker run --name {nombre_cont} \
        --rm \
        -ti \
        {volumen_mount} \
        {distribucion.value} \
        bash -c "{comandos_dist[distribucion]} && \
                 useradd -m el && \
                 echo 'el:el' | chpasswd && \
                 usermod -aG wheel el && \
                 sed -i 's/^# %wheel/%wheel/' /etc/sudoers && \
                 exec su - el"
    """
    ejecutar_comando(comando)

@app.command()
def limpiar_todo():
    """
    Limpia todos los recursos Docker no utilizados
    """
    typer.echo("Deteniendo todos los contenedores...")
    ejecutar_comando("docker stop $(docker ps -aq)")
    
    typer.echo("Eliminando todos los contenedores...")
    ejecutar_comando("docker rm $(docker ps -aq)")
    
    typer.echo("Eliminando volúmenes no utilizados...")
    ejecutar_comando("docker volume prune -f")
    
    typer.echo("Eliminando imágenes no utilizadas...")
    ejecutar_comando("docker image prune -f")

@app.command()
def crear_checkpoint(container_id: str, nombre: str):
    """
    Crea un checkpoint (imagen) de un contenedor
    """
    ejecutar_comando(f"docker commit {container_id} {nombre}")

if __name__ == "__main__":
    app()
