from socket import *
import  threading



class Udp(object):

    def __init__(self, client, udpServer):
        self.client = client
        self.serverName = udpServer.name
        self.serverPort = udpServer.port
        self.clientSocket = None
        self.partnerAdress = ("", 0)
        self.messages = []
        self.pill2kill = threading.Event()
        self.thread = threading.Thread(target=self.receive, args=(self.pill2kill, "task"))





    def send(self, msg, seq):
        self.clientSocket.settimeout(2.0);
        print("Client sendet :" + msg + "an:" + self.serverName + str(self.serverPort))
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
        if self.thread.is_alive():
            self.pill2kill.set()
            self.thread.join()
        self.clientSocket.close()

    def setConnection(self, ip, port):
        self.serverName = ip
        self.serverPort = port
        print("Connected to:" + self.serverName + str(self.serverPort))
        if self.pill2kill:
            self.pill2kill.clear()
        print("2KillSet: " + str(self.pill2kill.isSet()))
        self.clientSocket = socket(AF_INET, SOCK_DGRAM)
        self.connect()


        self.thread = threading.Thread(target=self.receive, args=(self.pill2kill, "task"))
        self.thread.start()


    def receive(self, stop_event, arg ):
        while not stop_event.wait(1):
            try:

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







