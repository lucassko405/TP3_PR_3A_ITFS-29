import socket
import json
import threading
from concurrent.futures import ThreadPoolExecutor

# Pool de hilos compartido para todos los clientes
# Así las tareas se distribuyen entre los workers disponibles
pool_compartido = ThreadPoolExecutor(max_workers=4)

def procesar_tarea(tarea):
    # Extrae el tipo y los datos de la tarea recibida
    tipo = tarea.get("tipo", "")
    datos = tarea.get("datos", "")
    # Según el tipo, aplica la transformación correspondiente
    if tipo == "upper":
        return datos.upper()
    elif tipo == "reverse":
        return datos[::-1]
    elif tipo == "count":
        return str(len(datos))
    elif tipo == "suma":
        a, b = datos
        return str(a + b)
    elif tipo == "resta":
        a, b = datos
        return str(a - b)
    else:
        # Si no es un tipo conocido
        return f"Tarea '{tipo}' procesada con: {datos}"

def manejar_cliente(conn, addr):
    # Maneja la comunicación con un cliente conectado
    print(f"[CONEXIÓN] Cliente {addr}")
    with conn:
        while True:
            try:
                # Recibe y decodifica el mensaje JSON del cliente
                data = conn.recv(4096).decode("utf-8")
                if not data:
                    break
                tarea = json.loads(data)
                # Si el cliente solicita salir, cierra la conexión
                if tarea.get("tipo") == "exit":
                    print(f"[DESCONEXIÓN] {addr}")
                    break
                print(f"[TAREA] {tarea} de {addr}")
                # Envía la tarea al pool compartido para que la procese un worker libre
                futuro = pool_compartido.submit(procesar_tarea, tarea)
                resultado = futuro.result()
                # Envía el resultado de vuelta al cliente como JSON
                conn.sendall(json.dumps({"resultado": resultado}).encode("utf-8"))
            except Exception as e:
                # Si ocurre un error, lo informa al cliente y cierra la conexión
                conn.sendall(json.dumps({"error": str(e)}).encode("utf-8"))
                break

def iniciar_servidor():
    # Crea el socket TCP/IP del servidor
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Permite reusar la dirección para evitar errores al reiniciar
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Asocia el socket a localhost en el puerto 5000
    srv.bind(("localhost", 5000))
    # Pone el socket en modo escucha (máximo 5 conexiones en cola)
    srv.listen()
    print("[SERVIDOR] Escuchando en localhost:5000 ...")
    # Bucle principal: acepta conexiones entrantes y crea un hilo por cliente
    while True:
        conn, addr = srv.accept()
        hilo = threading.Thread(target=manejar_cliente, args=(conn, addr))
        hilo.start()

if __name__ == "__main__":
    iniciar_servidor()
