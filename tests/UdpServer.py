from socket import AF_INET, socket, SOCK_DGRAM
import random
from threading import Thread


class UdpServer:

    def __init__(self,client):
        #self.port = self.generatePort()
        self.client = client
        self.name = "localhost"
        self.port = 12001
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind(("", self.port))
        self.clients = []
        self.udpserver_thread = Thread(target=self.handle)
        print("UDP Server läuft mit Port: " + str(self.port))




    def generatePort(self):
        # port numbers between 49152 to 65535
        return 49152 + random.randrange(15000)


    def handle(self):
        while 1:
            message, clientAddress = self.socket.recvfrom(2048)
            if str(message,"utf-8") == "connect":
                if clientAddress not in self.clients:
                    self.clients.append(clientAddress)
            else:
                for c in self.clients:
                    print(self.client.tcp.username + str(c))
                    self.socket.sendto(message, c)







