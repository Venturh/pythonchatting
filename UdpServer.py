from socket import AF_INET, socket, SOCK_DGRAM
import random
from threading import Thread


class UdpServer:

    def __init__(self):
        self.port = self.generatePort()
        self.socket =  socket(AF_INET, SOCK_DGRAM)
        self.socket.bind(("", self.port))
        print("UDP Server läuft mit Port: " + str(self.port))
        Thread(target=self.handle).start()

    def generatePort(self):
        # port numbers between 49152 to 65535
        return 49152 + random.randrange(15000)

    def handle(self):
        while 1:
            # read client's message AND REMEMBER client's address (IP and port)
            message, clientAddress = self.socket.recvfrom(2048)
            # output to console the sentence received from client over UDP
            print("Received from Client: ", message)
            self.socket.sendto(message, clientAddress)
            print("Sent back to Client: ", message)

a = UdpServer()





