from socket import AF_INET, socket, SOCK_DGRAM, timeout
import random
from threading import Thread


class UdpServer:

    def __init__(self, client):
        self.port = self.generatePort()
        self.client = client
        self.name = "localhost"
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind(("", self.port))
        self.clients = []
        self.seqnumber = 0
        self.seqnumbers = []
        self.udpserver_thread = Thread(target=self.handle)
        self.udpserver_thread.start()
        print("UDP Server läuft mit Port: " + str(self.port))

    def generatePort(self):
        return 4900 + random.randrange(2000)

    def send(self, user, msg, c):
        self.socket.settimeout(2.0);
        message = bytes(user + ":|:" + msg + ":|:" + str(int(self.seqnumber)), "utf-8")
        try:
            self.socket.sendto(message, c)
        except timeout as err:
            print(err)
            self.send(user, msg, c)
        finally:
            print("Server send:" + user + " " + msg + " " + str(self.seqnumber))

    def broadcast(self, user, message):
        self.seqnumber += 1
        for c in self.clients:
            print(str(c))
            self.send(user, message, c)

    def close(self):
        print("Server geschlossen")

    def handle(self):
        while 1:
            try:
                msg, clientAddress = self.socket.recvfrom(2048)
                user, message, seq = self.client.udp.decode_split(msg)
                print("Server received:" + user + " " + message + " " + seq)
                for s in self.seqnumbers:
                    if s == seq:
                        print("Duplikat")
                        continue
                self.seqnumbers.append(seq)
                if message == "connect" or message == "connect\n":
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









