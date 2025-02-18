from SPIELFELDD import MenschAergereDichNicht
from PyQt5.QtWidgets import QApplication

# Initialisiere QApplication
app = QApplication([])  # QApplication erstellen

# Initialisiere das Spielfeld
spielfeld = MenschAergereDichNicht("red", "green", "yellow", "blue", "red")

# Server starten (dies läuft unabhängig von der PyQt-Eventschleife)
import socket
import threading

clients = {}
lock = threading.Lock()

MAX_MESSAGE_LENGTH = 100

def broadcast(message, sender_socket):
    with lock:
        for client_socket, client_name in clients.items():
            if client_socket != sender_socket:
                try:
                    client_socket.send(message.encode('utf-8'))
                except:
                    client_socket.close()
                    del clients[client_socket]

def handle_client(client_socket, client_address):
    global spielfeld
    try:
        client_socket.send("Gib deinen Benutzernamen ein: ".encode('utf-8'))
        username = client_socket.recv(256).decode('utf-8').strip()

        if len(username) > 256:
            client_socket.send("Benutzername zu lang (max. 256 Zeichen erlaubt).".encode('utf-8'))
            client_socket.close()
            return

        with lock:
            clients[client_socket] = username

        print(f"{username} hat sich verbunden.")

        client_socket.send(f"Willkommen {username}!\n".encode('utf-8'))

        while True:
            try:
                message = client_socket.recv(256).decode('utf-8')

                if len(message) > MAX_MESSAGE_LENGTH:
                    client_socket.send(f"NACHRICHT ZU LANG (max. {MAX_MESSAGE_LENGTH} ZEICHEN ERLAUBT).".encode('utf-8'))
                    continue

                if message:
                    if message.startswith("/move"):
                        parts = message.split(' ')
                        if len(parts) == 3:
                            try:
                                figur = parts[1]
                                steps = int(parts[2])  # Schritte müssen eine Zahl sein
                                
                                # Rufe die `move`-Methode des Spielfelds auf
                                ausgang = (0, 0)  # Beispiel: Startposition
                                spielfeld.move(None, steps, ausgang)  # Übergib die Schritte und Ausgangsposition
                                
                                client_socket.send("Zug erfolgreich ausgeführt.\n".encode('utf-8'))
                            except Exception as e:
                                client_socket.send(f"Fehler beim Ausführen des Zugs: {e}\n".encode('utf-8'))
                        else:
                            client_socket.send("Bewegungs-Befehl falsch formatiert. Benutze: /move <Figur> <Schritte>\n".encode('utf-8'))
                    else:
                        print(f"{username}: {message}")
                        broadcast(f"{username}: {message}", client_socket)
            except Exception as e:
                print(f"Fehler bei der Verbindung mit {client_address}: {e}")
                break
    finally:
        with lock:
            if client_socket in clients:
                del clients[client_socket]
        client_socket.close()

def start_server():
    server_ip = '0.0.0.0'
    server_port = 5555

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen()

    print(f"Server gestartet, wartet auf Verbindungen auf {server_ip}:{server_port}...")

    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True).start()


def whisper(message, sender_socket, target_name):
    with lock:
        for client_socket, client_name in clients.items():
            if client_name == target_name:
                try:
                    client_socket.send(f"Flüster-Nachricht: {message}".encode('utf-8'))
                    sender_socket.send(f"Flüster an {target_name}: {message}".encode('utf-8'))
                    return
                except Exception as e:
                    print(f"Fehler beim Senden der Flüster-Nachricht: {e}")
                    sender_socket.send(f"Fehler beim Senden der Nachricht an {target_name}. Bitte versuche es später erneut.".encode('utf-8'))
                    return
        sender_socket.send(f"Benutzer {target_name} nicht gefunden.".encode('utf-8'))
        
if __name__ == "__main__":
    threading.Thread(target=start_server, daemon=True).start()

    # Zeige das Spielfeld-Fenster
    spielfeld.show()

    # Starte die PyQt-Eventschleife
    app.exec_()
