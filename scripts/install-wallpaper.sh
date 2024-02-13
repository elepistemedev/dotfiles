#!/usr/bin/env sh

# Mensaje de instalación
echo "Instalando Wallpaper extras"

# Crear directorio principal
mkdir -p ~/wallpaper

# Cambiar al directorio principal
cd ~/wallpaper

# Crear carpeta para imágenes
mkdir img

# Clonar proyectos
git clone https://github.com/UbuntuBudgie/budgie-wallpapers.git
git clone https://gitlab.com/dwt1/wallpapers.git

# Extraer imágenes de cada proyecto
for proyecto in budgie-wallpapers wallpapers; do
    # Entrar al directorio del proyecto
    cd "$proyecto"

    # Encontrar archivos de imágenes
    imagenes=$(find . -type f \( -iname "*.jpg" -o -iname "*.png" \))

    # Mover archivos de imágenes a la carpeta img
    for imagen in $imagenes; do
        mv "$imagen" ../img
    done

    # Salir del directorio del proyecto
    cd ..
done

# Mensaje de finalización
echo "**¡Instalación completada!**"
echo "Las imágenes se encuentran en la carpeta ~/wallpaper/img"
