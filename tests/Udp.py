from socket import *
from threading import Thread

class Udp(object):

    def __init__(self, client):
        self.client = client
        self.serverName = "localhost"
        self.serverPort = 12000
        self.clientSocket = socket(AF_INET, SOCK_DGRAM)
        self.clientSocket.connect((self.serverName,self.serverPort))
        self.partnerAdress = ("", 0)
        self.thread = Thread(target=self.receive).start()


    def send(self,msg):
        message = bytes(self.client.tcp.username+": " + msg, "utf-8")
        self.clientSocket.sendto(message, (self.serverName, self.serverPort))

    def connect(self):
        self.clientSocket.sendto(bytes("connect", "utf-8"),(self.serverName, self.serverPort))

    def close(self):
        self.clientSocket.close()

    def receive(self):
        while 1:
            msg, serverAddress = self.clientSocket.recvfrom(2048)
            print("Empfangen: " + str(msg, "utf-8"))
            self.client.gui.update_msg_list(msg)

    def getPartnerAdress(self):
        self.partnerAdress = self.client.udpServer.adress;





