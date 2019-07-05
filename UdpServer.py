from socket import AF_INET, socket, SOCK_DGRAM, timeout
import random
from threading import Thread


class UdpServer:

    def __init__(self, client):
        self.port = self.generatePort()
        self.client = client
        self.name = "localhost"
        #self.port = 12000
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind(("", self.port))
        self.clients = []
        self.messages = []
        self.udpserver_thread = Thread(target=self.handle)
        self.udpserver_thread.start()
        print("UDP Server läuft mit Port: " + str(self.port))

    def generatePort(self):
        # port numbers between 49152 to 65535
        return 49152 + random.randrange(15000)

    def send(self, user, msg, seq, c):
        self.socket.settimeout(2.0);
        message = bytes(user + ":|:" + msg + ":|:" + str(seq), "utf-8")
        try:
            self.socket.sendto(message, c)
        except timeout as err:
            print(err)
            self.send(msg,int(seq)+1)

    def broadcast(self, user, message):
        for c in self.clients:
            print(str(c))
            self.send(user, message, 0, c)

    def close(self):
        print("Server geschlossen")



    def handle(self):
        while 1:
            try:
                msg, clientAddress = self.socket.recvfrom(2048)
                user, message, seq = self.client.udp.decode_split(msg)
                self.messages.append((user, message, seq))
                print(message)
                if int(seq) > 0:
                    seqMin = 0
                    for u, m, s in self.messages:
                        if u == user and message == m and s <= seqMin:
                            seqMin = s
                    for u, m, s in self.messages:
                        if s > seqMin:
                            self.messages.remove((u, m, s))
                            print("Duplikat")
                            return

                if message == "connect":
                    if clientAddress not in self.clients:
                        self.clients.append(clientAddress)
                elif message == "disconnect":
                    if clientAddress in self.clients:
                        self.clients.remove(clientAddress)
                        self.broadcast(user, message)
                else:
                    self.broadcast(user, message)

            except timeout:
                continue









