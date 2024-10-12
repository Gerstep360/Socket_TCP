import socket
import selectors
import threading
from hilo_conexiones import HiloConexiones

# Clase 2: Servidor - Configura el socket y maneja las conexiones con eventos
class Servidor:
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        # Crear el socket TCP
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setblocking(False)  # Para no bloquear las operaciones de conexión
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(20)
        
        # Crear un selector para gestionar eventos
        self.selector = selectors.DefaultSelector()

        # Registrar el servidor en el selector para aceptar conexiones
        self.selector.register(self.server_socket, selectors.EVENT_READ, self.aceptar_conexiones)

        self.conexiones = {}

    def iniciar_servidor(self):
        print(f"Servidor escuchando en {self.host}:{self.port}")
        # Hilo que se encargará de monitorear los eventos del selector
        hilo_aceptacion = threading.Thread(target=self.event_loop)
        hilo_aceptacion.start()

    def event_loop(self):
        # Este método espera eventos y los maneja en el hilo principal
        while True:
            eventos = self.selector.select(timeout=None)  # Bloquea hasta que haya eventos
            for llave, mascara in eventos:
                # Ejecutar la función asociada al evento
                callback = llave.data
                callback(llave.fileobj)

    def aceptar_conexiones(self, server_socket):
        # Acepta una nueva conexión y lanza un hilo de conexión
        cliente_socket, direccion = server_socket.accept()
        cliente_socket.setblocking(False)  # Para no bloquear las operaciones de lectura/escritura
        print(f"Conexión aceptada desde {direccion}")

        # Crear una instancia de HiloConexiones (ahora es un hilo)
        hilo_conexion = HiloConexiones(cliente_socket, self, direccion)
        hilo_conexion.start()  # Iniciar el hilo para manejar la conexión


    def agregar_usuario(self, direccion, socket):
        self.conexiones[direccion] = socket
        print(f"Usuario {direccion} conectado. Usuarios conectados: {len(self.conexiones)}")

    def obtener_usuario(self, direccion):
        return self.conexiones.get(direccion, None)

    def eliminar_usuario(self, direccion):
        if direccion in self.conexiones:
            del self.conexiones[direccion]
            print(f"Usuario {direccion} desconectado. Usuarios conectados: {len(self.conexiones)}")
