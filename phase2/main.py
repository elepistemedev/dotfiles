from InquirerPy import inquirer
from common.logo import show as logo


def main():
    # Mostrar el logo personalizado
    logo("💾 Post Instalación - 2da Fase")

    # Preguntar al usuario si desea continuar
    action = inquirer.select(
        message="¿Deseas continuar con la Fase 2 o salir?",
        choices=[
            "Continuar con la Fase 2",
            "Salir",
        ],
    ).execute()

    # Procesar la elección del usuario
    if action == "Continuar con la Fase 2":
        print("Iniciando la Fase 2...")
        # Aquí puedes llamar a las funciones de la Fase 2
    else:
        print("Saliendo del instalador. ¡Hasta luego!")
        exit(0)


if __name__ == "__main__":
    main()
