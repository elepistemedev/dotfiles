```
█▀ █▀▀ █▄░█ ▀█▀ █░█  ┎┤ DATA ENGINEER                                       ├┒
▄█ ██▄ █░▀█ ░█░ █▄█  ┖┤ Obteniendo datos para empresas, personas... para ti ├┚
                STUDIO
```
# Guía de instalación del sistema operativo para SENTU.studio

## Preparación

Descargamos la imagen iso y el archivo b2sums.txt desde el repositorio global de archlinux:

> Index of /archlinux/iso/2024.06.01

```bash
wget -c  https://geo.mirror.pkgbuild.com/iso/2024.06.01/archlinux-2024.06.01-x86_64.iso && \
wget -c  https://geo.mirror.pkgbuild.com/iso/2024.06.01/b2sums.txt
```

### Verificación Efectiva de la descarga

```bash
b2sum -c b2sums.txt
```

## Instalación

```bash
loadkeys la-latin1
```

Verificando la conectividad de internet

```bash
ping 8.8.8.8
```

A continuación usamos el comando archinstall para configurar el pre-installer

```bash
archinstall
```



## Post-instalación dotfiles

Respaldo de mis archivos de configuración para linux. Optimizado para la distro de Archlinux.

```bash
# Descargamos el autoscript
curl https://raw.githubusercontent.com/elepistemedev/dotfiles/archlinux/SENTUInstaller -o SENTUInstaller.sh

# Le damos permisos de ejecucion
chmod +x SENTUInstaller.sh

# Ejecutamos
./SENTUInstaller.sh
```
