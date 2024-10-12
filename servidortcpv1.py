import socket
import threading

# Clase 1: Main - Ejecuta las clases de conexión y administración de hilos
class Main:
    def __init__(self):
        # Crear una instancia del servidor
        self.servidor = Servidor()

    def run(self):
        # Ejecutar el servidor
        self.servidor.iniciar_servidor()


# Clase 2: Servidor - Configura el socket y maneja las conexiones
class Servidor:
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        # Crear el socket TCP
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conexiones = []

    def iniciar_servidor(self):
        # Vincular el socket a la dirección y puerto
        self.server_socket.bind((self.host, self.port))
        # Escuchar hasta 5 conexiones simultáneas
        self.server_socket.listen(5)
        print(f"Servidor escuchando en {self.host}:{self.port}")

        # Bucle infinito para aceptar nuevas conexiones
        while True:
            cliente_socket, direccion = self.server_socket.accept()
            print(f"Conexión aceptada desde {direccion}")
            # Crear un nuevo hilo para manejar la conexión
            hilo_conexion = HiloConexiones(cliente_socket, self, direccion)
            hilo_conexion.start()


# Clase 3: HiloConexiones - Administra las conexiones de los clientes en hilos separados
class HiloConexiones(threading.Thread):
    def __init__(self, cliente_socket, servidor, direccion):
        super().__init__()
        self.cliente_socket = cliente_socket
        self.servidor = servidor
        self.direccion = direccion

    def run(self):
        # Agregar la nueva conexión a la lista de conexiones
        self.servidor.conexiones.append(self.cliente_socket)
        print(f"Conexiones activas: {len(self.servidor.conexiones)}")
        
        # Crear un nuevo hilo para manejar la comunicación con este cliente
        hilo_comunicacion = HiloComunicacion(self.cliente_socket, self.servidor, self.direccion)
        hilo_comunicacion.start()


# Clase 4: HiloComunicacion - Maneja la comunicación entre el servidor y el cliente
class HiloComunicacion(threading.Thread):
    def __init__(self, cliente_socket, servidor, direccion):
        super().__init__()
        self.cliente_socket = cliente_socket
        self.servidor = servidor
        self.direccion = direccion

    def run(self):
        while True:
            try:
                # Recibe el mensaje del cliente
                mensaje = self.cliente_socket.recv(1024).decode()
                if mensaje:
                    print(f"Mensaje recibido de {self.direccion}: {mensaje}")
                    # Envía una respuesta de vuelta al cliente
                    self.cliente_socket.send(f"Eco: {mensaje}".encode())
                else:
                    # Si no hay mensaje, el cliente ha cerrado la conexión
                    break
            except ConnectionResetError:
                # Si hay un error de conexión, cerrar el socket
                break

        # Cerrar el socket cuando termine la comunicación
        self.cliente_socket.close()
        
        # Eliminar la conexión de la lista de conexiones activas
        self.servidor.conexiones.remove(self.cliente_socket)
        print(f"Cliente {self.direccion} se ha desconectado.")
        
        # Mostrar la cantidad de conexiones activas
        print(f"Conexiones activas: {len(self.servidor.conexiones)}")


# Iniciar la aplicación
if __name__ == "__main__":
    main = Main()
    main.run()
