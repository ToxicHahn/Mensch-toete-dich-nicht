import threading
import socket
import re
import time

class Server:
    def __init__(self, host = '10.16.206.7', port=5000):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = []
        self.clientss = []
        self.game_state = {}
        self.player = ""
        self.game_started = False
        self.lock = threading.Lock()

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(4)
        print(f"Server gestartet auf {self.host}:{self.port}")
        
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Verbindung von {client_address} angenommen.")
            self.clients.append(client_socket)
            #print(self.clients)
            
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        #print(client_socket)
        while True:
            with self.lock:
                if len(self.clientss) == 4 and not self.game_started:
                    self.game_started = True  # Spiel wurde gestartet
                    threading.Thread(target=self.start_game).start()
                    print("Start Spiel!")
            
            message = client_socket.recv(1024).decode('utf-8')
            anzahl = message.count('/')
            if anzahl == 2:
                parts = message.split("/")
                parts.pop(0)
                for messagee in parts:
                    print(f"Nachricht erhalten: {messagee}")
                    if messagee.startswith("done"):
                        self.nextTurnF(messagee)
                    elif messagee.startswith("win"):
                        self.win(messagee, client_socket)
                    elif messagee.startswith("move"):
                        self.move(messagee, client_socket)
                    elif messagee.startswith("player"):
                        #print("/Player erhalten")
                        self.getPlayer(client_socket)
                    elif messagee.startswith("color"):
                        self.defineColor(messagee, client_socket)
                    elif messagee.startswith("whisper"):
                        parts = messagee.split("#")
                        self.send(messagee, parts[3])
                        time.sleep(0.1)
                    elif messagee.startswith("message"):
                        self.broadcast(messagee)
                        time.sleep(0.1)
    

            elif message:
                print(f"Nachricht erhalten: {message}")
                if message.startswith("/done"):
                    self.nextTurnF(message)
                elif message.startswith("/win"):
                    self.win(message, client_socket)
                elif message.startswith("/move"):
                    self.move(message, client_socket)
                elif message.startswith("/player"):
                    #print("/Player erhalten")
                    self.getPlayer(client_socket)
                elif message.startswith("/color"):
                    self.defineColor(message, client_socket)
                elif message.startswith("/whisper"):
                    print(message)
                    parts = message.split("#")
                    self.send(message, parts[3][0])
                    time.sleep(0.1)
                elif message.startswith("/message"):
                    print(f"MESSAGEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE {message}")
                    self.broadcast(message, client_socket)
                    time.sleep(0.1)
                


        #except Exception as e:
        #    print(f"Fehler beim Verarbeiten des Clients: {e}")
        #    ind = self.clients.index(client_socket)
          #  username = self.clientss[ind]
        #    self.clients.remove(client_socket)
        #    self.clientss.remove(username)
        #    client_socket.close()
        #print(self.clientss)


    def move(self, message, client_socket):
        #parts = message.split(' ', 4)
        # parts[0]= /move
        # parts[1]= self.player
        # parts[2]= (row, col)
        # parts[3]= button
        self.broadcast(message, client_socket)

    def defineColor(self, message, client_socket):
        data = message.split("#")
        color = data[1]
        if color in self.clientss:
            self.clients.remove(client_socket)
            messageD = f'/decline#Bitte eine andere Farbe wählen!'
            self.send(messageD, client_socket)
            time.sleep(0.1)
        else:
            self.clientss.append(color)
            print(f"{self.clientss[-1]} hat sich verbunden.")
            print(self.clientss)
            messageB = f'/connect#{color}'
            self.broadcast(messageB)
            time.sleep(0.1)
            messageS = f'/colors#self.clientss'
            self.send(messageS, client_socket)
            time.sleep(0.1)

    def broadcast(self, message, sender_socket = None):
        for client_socket in self.clients:
            if client_socket != sender_socket:
                try:
                    print(f"MESAGGEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE {message}")
                    client_socket.send(message.encode('utf-8'))
                    time.sleep(0.1)
                except:
                    client_socket.close()
                    self.clients.remove(client_socket)


    def end(self):
        for client_socket in self.clients:
            client_socket.close()
            self.clients.remove(client_socket)


    def start_game(self):
        color1 = self.clientss[0]
        color2 = self.clientss[1]
        color3 = self.clientss[2]
        color4 = self.clientss[3]

        message = f'/finalColor#{color1}#{color2}#{color3}#{color4}'
        print(f' BROADCAST{message}')
        self.broadcast(message)

        time.sleep(0.1)

        message = f'/start'
        self.broadcast(message)
        print("Das Spiel startet mit den folgenden Spielern:", self.clientss)
        self.index = 0
        self.nextTurn()

    def win(self, message, client_socket):
        self.broadcast(message, client_socket)
        self.end()

    def nextTurnF(self, message):
        parts = message.split(' ')
        x = self.index -1
        #print(self.clientss[x])
        y = re.sub(r'[[]', '', self.clientss[x])
        z = re.sub(r'[]]', '', y)
        #print(parts[1])
        #print(z)
        if z == parts[1]:
            self.nextTurn()



    def nextTurn(self):
        #f'NEXT TURN {self.index}')
        target = self.clients[self.index]
        #print(target)
        message = f'/turn'
        self.send(message, target)
        time.sleep(0.1)
        self.index = self.index + 1
        if self.index == len(self.clients):
            self.index = 0

    def send(self, message, target):
        #print(target)
        print(target)
        
        target.send(message.encode('utf-8'))
        time.sleep(0.1)

    def getPlayer(self, client_socket):
        playerr = F'/player#{self.clientss[self.index-1]}#'
        self.broadcast(playerr)
        time.sleep(0.1)
        

#if __name__ == '__main__':
#    server = Server()
#    server.start_server()