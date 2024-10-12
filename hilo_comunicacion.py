import threading
import select  
# Clase 4: HiloComunicacion - Maneja la comunicación entre el servidor y el cliente
class HiloComunicacion(threading.Thread):
    def __init__(self, cliente_socket, servidor, direccion):
        super().__init__()
        self.cliente_socket = cliente_socket
        self.servidor = servidor
        self.direccion = direccion
        self.conexion_cerrada = False

    def run(self):
        try:
            while True:
                # Usamos select para asegurarnos de que el socket esté listo para la lectura
                leer, _, _ = select.select([self.cliente_socket], [], [], 0.1)  # Timeout de 0.1 segundos

                if leer:
                    mensaje = self.cliente_socket.recv(1024).decode()

                    if mensaje.strip():  # Comprobar que el mensaje no esté vacío
                        print(f"Mensaje recibido de {self.direccion}: {mensaje}")
                        # Envía una respuesta de vuelta al cliente
                        self.cliente_socket.send(f"Tu mensaje desde {self.direccion} es: {mensaje}".encode())
                    else:
                        # Si no hay mensaje, se marca la conexión como cerrada
                        self.cerrar_conexion()
                        break
                else:
                    # Si no hay datos disponibles para leer, continuamos esperando
                    continue

        except ConnectionResetError:
            # Si hay un error de conexión, cerrar el socket
            self.cerrar_conexion()

    def cerrar_conexion(self):
        # Cerrar el socket cuando termine la comunicación
        print(f"Cliente {self.direccion} se ha desconectado.")

        # Eliminar el usuario de la lista de conexiones activas antes de mostrar las conexiones activas
        self.servidor.eliminar_usuario(self.direccion)

        # Mostrar la cantidad de conexiones activas después de eliminar al usuario
        print(f"Usuarios conectados: {len(self.servidor.conexiones)}")

        # Marcar que la conexión ha sido cerrada
        self.conexion_cerrada = True
