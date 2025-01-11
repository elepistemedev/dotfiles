def show(message: str = "con Python 🐍"):
    """
    Muestra el logo del proyecto junto a un mensaje personalizado.
    Args:
        message (str): El mensaje que se mostrará debajo del logo.
    """
    encabezado = "Ingeniería de Datos & Data Science"
    mensaje = message

    # Determinar la longitud máxima
    max_len = max(len(encabezado), len(mensaje))

    # Centrar ambas cadenas según la longitud máxima
    encabezado_ajustado = encabezado.center(max_len)
    mensaje_ajustado = mensaje.center(max_len)

    logo = f"""
    \033[1m\033[33m█▀ █▀▀ █▄░█ ▀█▀ █░█\033[0m  ┎┤ {encabezado_ajustado} ├┒ 
    \033[1m\033[33m▄█ ██▄ █░▀█ ░█░ █▄█\033[0m  ┖┤ \033[1m{mensaje_ajustado}\033[0m├┚
                .studio
    """
    print(logo)
