import threading
from hilo_comunicacion import HiloComunicacion

# Clase 3: HiloConexiones - Administra las conexiones de los clientes en hilos separados
class HiloConexiones(threading.Thread):
    def __init__(self, cliente_socket, servidor, direccion):
        super().__init__()
        self.cliente_socket = cliente_socket
        self.servidor = servidor
        self.direccion = direccion

        # Agregar el usuario al servidor
        self.servidor.agregar_usuario(self.direccion, self.cliente_socket)

    def run(self):
        # Crear un hilo de comunicación para gestionar la interacción con el cliente
        hilo_comunicacion = HiloComunicacion(self.cliente_socket, self.servidor, self.direccion)
        hilo_comunicacion.start()  # Iniciar el hilo de comunicación

        # Esperar a que el hilo de comunicación termine
        hilo_comunicacion.join()

        # Eliminar el usuario una vez que la comunicación ha terminado
        self.servidor.eliminar_usuario(self.direccion)
