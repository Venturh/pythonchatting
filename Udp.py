from socket import *
from threading import Thread


class Udp(object):

    def __init__(self, client, udpServer):
        self.client = client
        self.serverName = udpServer.name
        self.serverPort = udpServer.port
        self.clientSocket = None

        self.partnerAdress = ("", 0)
        self.messages = []
        self.thread = Thread(target=self.receive)
        self.run = True





    def send(self, msg, seq):
        print("IP+Port: " + self.serverName + "+" + str(self.serverPort))
        self.clientSocket.settimeout(2.0);
        message = bytes(self.client.tcp.username + ": " + ":|:" + msg + ":|:" + str(seq), "utf-8")
        try:
            self.clientSocket.sendto(message, (self.serverName, int(self.serverPort)))
        except timeout as err:
            print(err)
            self.send(msg, seq + 1)

    def connect(self):
        self.clientSocket.settimeout(2.0);
        self.send("connect", 0)

    def disconnect(self):
        self.clientSocket.settimeout(2.0);
        self.send("disconnect", 0)
        self.run = False
        if self.thread.is_alive():
            self.thread.join()
        self.clientSocket.close()



    def setConnection(self, ip, port):
        self.clientSocket = socket(AF_INET, SOCK_DGRAM)
        self.serverName = ip
        self.serverPort = port
        self.clientSocket.connect((self.serverName, int(self.serverPort)))
        self.thread.start()
        print("Connected to:" + self.serverName + str(self.serverPort))

    def receive(self, ):
        while self.run:
            try:
                print(self.run)
                msg, clientAddress = self.clientSocket.recvfrom(2048)
                user, message, seq = self.decode_split(msg)
                self.messages.append((user, message, seq))
                print(message)
                print("Seq: " + seq)
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
                if message == "disconnect":
                    self.client.gui.update_msg_list("Dein Chatpartner " + user + "hat den Chat verlassen")
                else:
                    #self.client.gui.update_msg_list(user + message)
                    self.client.gui.queue.put(user + message)

            except timeout:
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

    def saveAndQuit(self):
        self.running = False
        self.trackingThread.join(timeout=0.05)
        # if thread is still alive, return control to the Qt event loop
        # and rerun this function in 50 milliseconds
        if self.thread.is_alive():
            QTimer.singleShot(50, self.saveAndQuit)
            return
        # if the thread has ended, then save and quit!
        else:
            self.save()
            QApplication.instance().quit()





