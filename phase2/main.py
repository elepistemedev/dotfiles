from textual.app import App
from textual.widgets import Header, Footer, Button, Static
from textual.containers import Center, Vertical, Horizontal


class Fase2App(App):
    """Aplicación interactiva para la Fase 2."""

    def compose(self):
        # Agregar un encabezado, un mensaje, botones y un pie de página
        yield Header()
        yield Vertical(
            Center(Static("💾 ¿Deseas continuar con la Fase 2 o salir?", id="message")),
            Horizontal(
                Center(Button("Continuar", id="continue", variant="success")),
                Center(Button("Salir", id="exit", variant="error")),
            ),
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        """Manejar la acción cuando se presiona un botón."""
        button_id = event.button.id  # Ahora accedemos a `event.button.id`
        if button_id == "continue":
            self.exit("continue")
        elif button_id == "exit":
            self.exit("exit")


if __name__ == "__main__":
    # Ejecutar la aplicación y capturar la decisión del usuario
    result = Fase2App().run()
    if result == "continue":
        print("Iniciando la Fase 2...")
        # Aquí puedes continuar con la lógica de la Fase 2
    else:
        print("Saliendo del instalador. ¡Hasta luego!")
