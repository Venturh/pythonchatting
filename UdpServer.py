from socket import AF_INET, socket, SOCK_DGRAM, timeout
import random
from threading import Thread


class UdpServer:

    def __init__(self, client):
        #self.port = self.generatePort()
        self.client = client
        self.name = "localhost"
        self.port = 12000
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind(("", self.port))
        self.clients = []
        self.messages = []
        self.udpserver_thread = Thread(target=self.handle).start()
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
        finally:
            self.socket.settimeout(None);

    def handle(self):
        while 1:
            msg, clientAddress = self.socket.recvfrom(2048)
            user, message, seq = self.client.udp.decode_split(msg)
            self.messages.append((user, message, seq))
            print("Seq: "+seq)
            if int(seq) > 0:
                for u, m, s in self.messages:
                    if s < int(seq) and message == m:
                        print("Duplikat")
                        self.messages.remove((u, m, s))
                        #muss noch gesendet werden oder nicht?
                        #self.send(user, "duplikat, 0, c")

            if message == "connect":
                if clientAddress not in self.clients:
                    self.clients.append(clientAddress)
            else:
                for c in self.clients:
                    print(str(c))
                    self.send(user, message, 0, c)









