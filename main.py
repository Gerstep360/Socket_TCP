from servidor import Servidor

# Clase 1: Main - Ejecuta las clases de conexión y administración de hilos
class Main:
    def __init__(self):
        # Crear una instancia del servidor
        self.servidor = Servidor()

    def run(self):
        # Ejecutar el servidor
        self.servidor.iniciar_servidor()


# Iniciar la aplicación
if __name__ == "__main__":
    main = Main()
    main.run()
