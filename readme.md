
# Proyecto de Sistemas Distribuidos - Servidor TCP con Hilos y Selectores en Python

Este proyecto tiene como objetivo implementar un servidor TCP utilizando hilos (`threading`) y selectores (`selectors`) en Python. El servidor permite la conexión simultánea de varios clientes, gestionando la comunicación de manera eficiente con el uso de hilos para cada conexión, mientras utiliza `selectors` para la aceptación de conexiones sin bloquear el servidor principal.

## Descripción del Proyecto

El servidor TCP desarrollado acepta múltiples conexiones de clientes y asigna un hilo independiente para cada cliente conectado, manejando la comunicación y desconexión de manera asíncrona. Cada cliente puede enviar mensajes al servidor, y el servidor responde con un mensaje de eco.

### Modificaciones Recientes
- **Uso de Selectores**: El servidor utiliza `selectors` para manejar la aceptación de nuevas conexiones sin bloquear las operaciones de red, lo que mejora la escalabilidad del sistema.
- **Hilos para Comunicación**: Cada conexión de cliente se gestiona a través de un hilo (`threading.Thread`), lo que permite realizar múltiples comunicaciones simultáneas sin bloquear la ejecución.
- **Manejo de Sockets no Bloqueantes**: Se ha añadido el manejo de sockets no bloqueantes mediante `select.select()` para evitar errores como `BlockingIOError`.
- **Mejor Manejo de Desconexiones**: Ahora el servidor elimina correctamente a los clientes desconectados y actualiza el número de conexiones activas.

## Estructura del Proyecto

El proyecto está organizado de manera modular, con cada funcionalidad importante en su propio archivo:

```
├── **main.py**               # Archivo principal que ejecuta el servidor
├── **servidor.py**           # Clase Servidor, gestiona las conexiones TCP mediante selectores y hilos
├── **hilo_conexiones.py**    # Clase HiloConexiones, administra las conexiones de los clientes
└── **hilo_comunicacion.py**  # Clase HiloComunicacion, gestiona la comunicación cliente-servidor
└── **cliente.py**            # Archivo principal que ejecuta el cliente
```

### Descripción de Archivos

- **main.py**: Es el punto de entrada del servidor. Crea una instancia del servidor y lo pone en funcionamiento.
- **servidor.py**: Implementa la lógica del servidor. Usa `selectors` para aceptar conexiones sin bloquear y lanza hilos para cada cliente.
- **hilo_conexiones.py**: Gestiona las conexiones de los clientes en hilos separados y delega la comunicación a `HiloComunicacion`.
- **hilo_comunicacion.py**: Maneja la comunicación entre el servidor y cada cliente. Utiliza `select.select()` para asegurar que el socket esté listo para lectura antes de recibir datos.
- **cliente.py**: Ejecuta el cliente TCP. Permite a los usuarios enviar mensajes al servidor y recibir respuestas de eco.

## Requisitos

- **Python 3.x** (preferentemente la última versión estable).

## Ejecución del Servidor

Para iniciar el servidor TCP, ejecuta el archivo **main.py**:

```bash
python main.py
```

El servidor estará escuchando en `localhost` en el puerto `8080`.

## Conectar un Cliente

Para conectar un cliente, ejecuta el archivo **cliente.py** en una nueva terminal:

```bash
python cliente.py
```

Cada cliente puede enviar mensajes al servidor, y el servidor responderá con un eco del mensaje recibido. Para desconectar el cliente, ingresa el comando **salir**.

## Ejemplo de Uso

1. Ejecuta el servidor:
   ```bash
   python main.py
   ```

2. Conecta un cliente:
   ```bash
   python cliente.py
   ```

3. Envía mensajes desde el cliente y recibe respuestas del servidor. Para desconectar, ingresa:
   ```bash
   salir
   ```

## Manejo de Desconexiones

Cuando un cliente se desconecta, el servidor detecta la desconexión y actualiza el número de conexiones activas, eliminando correctamente al cliente desconectado de su lista interna.

## Notas

- El servidor puede gestionar múltiples conexiones simultáneas de clientes gracias al uso de hilos.
- Los clientes pueden desconectarse enviando el mensaje "salir" o cerrando la conexión de manera manual.
