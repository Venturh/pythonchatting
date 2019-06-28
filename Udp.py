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
        self.messages = []
        self.thread = Thread(target=self.receive).start()



    def send(self, msg, seq):
        self.clientSocket.settimeout(2.0);
        message = bytes(self.client.tcp.username + ": " + ":|:" + msg + ":|:" + str(seq), "utf-8")
        try:
            self.clientSocket.sendto(message, (self.serverName, self.serverPort))
        except timeout as err:
            print(err)
            self.send(msg, seq + 1)

    def connect(self):
        self.clientSocket.settimeout(2.0);
        self.send("connect", 0)

    def receive(self):
        while 1:
            try:
                self.clientSocket.settimeout(None);
                msg, clientAddress = self.clientSocket.recvfrom(2048)
                user, message, seq = self.decode_split(msg)
                self.messages.append((user, message, seq))
                print("Seq: " + seq)
                if int(seq) > 0:
                    for u, m, s in self.messages:
                        if s >= int(seq) and message == m:
                            print("Duplikat")
                            # muss noch gesendet werden oder nicht?
                            # self.send(user, "duplikat, 0, c")
                self.client.gui.update_msg_list(user + message)
            except timeout:
                print("timout")
                continue;


    def decode_split(self,msg):
        message = str(msg, "utf-8")
        message = message.split(":|:")
        user = message[0]
        seq = message[2]
        message = message[1]
        return user, message, seq

    def getPartnerAdress(self):
        self.partnerAdress = self.client.udpServer.adress;

    def close(self):
        self.clientSocket.close()





