import socket

# Configuración del cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8080))
print("Para cancelar la conexion teclea: (salir)")
try:
    while True:
        # Envía un mensaje al servidor
        message = input("Escribe un mensaje: ")
        client_socket.send(message.encode())

        # Recibe la respuesta del servidor
        response = client_socket.recv(1024).decode()
        print(f"Respuesta del servidor: {response}")

        if message.lower() == 'salir':
            break
finally:
    client_socket.close()
