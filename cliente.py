import socket
import json

def menu():
    # Muestra las opciones disponibles al usuario
    print("\n--- SISTEMA DISTRIBUIDO - ENVÍO DE TAREAS ---")
    print("1. Convertir texto a MAYÚSCULAS")
    print("2. Invertir texto")
    print("3. Contar caracteres")
    print("4. Sumar números")
    print("5. Restar números")
    print("6. Salir")

def iniciar_cliente():
    # Crea el socket TCP y se conecta al servidor en localhost:5000
    cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cli.connect(("localhost", 5000))
    print("[CLIENTE] Conectado al servidor.")

    while True:
        # Muestra el menú y pide una opción al usuario
        menu()
        op = input("Seleccioná una opción: ")
        # Opción 6: sale del programa
        if op == "6":
            cli.sendall(json.dumps({"tipo": "exit"}).encode("utf-8"))
            break

        # Construye la tarea según la opción elegida
        if op == "1":
            texto = input("Texto: ")
            tarea = {"tipo": "upper", "datos": texto}
        elif op == "2":
            texto = input("Texto: ")
            tarea = {"tipo": "reverse", "datos": texto}
        elif op == "3":
            texto = input("Texto: ")
            tarea = {"tipo": "count", "datos": texto}
        elif op in ("4", "5"):
            tipo = "suma" if op == "4" else "resta"
            try: #comprueba qye sea numerico
                a = float(input("Primer número: "))
                b = float(input("Segundo número: "))
            except ValueError:
                print("Error: debe ingresar un número válido.")
                continue
            tarea = {"tipo": tipo, "datos": [a, b]}
        else:
            print("Opción inválida.")
            continue

        # Envía la tarea al servidor como JSON y espera la respuesta
        cli.sendall(json.dumps(tarea).encode("utf-8"))
        respuesta = json.loads(cli.recv(4096).decode("utf-8"))
        print(f"[RESULTADO] {respuesta.get('resultado', respuesta.get('error'))}")

    # Cierra la conexión con el servidor
    cli.close()
    print("[CLIENTE] Desconectado.")

if __name__ == "__main__":
    iniciar_cliente()
