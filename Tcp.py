import hashlib
from socket import AF_INET, socket, SOCK_STREAM, SOCK_DGRAM
from threading import Thread


class Tcp(object):

    def __init__(self, tcp_server, tcp_port, client):
        self.client = client
        self.serverName = tcp_server
        self.serverPort = tcp_port
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect((self.serverName, self.serverPort))
        self.username = ""
        self.thread = Thread(target=self.receive)
        self.run = True
        self.thread.start()


    def send(self, msg):
        print("Send:" + msg)
        self.socket.send(bytes(msg + "\n", "utf-8"))

    def receive(self):
        while self.run:
            received = self.socket.recv(1024).decode("utf-8")
            self.handle(received)

    def handle(self, received):
        print("handle: "+received)
        if received.startswith("10"):
            users = received.replace("\n", "").split("*")
            users.pop(0)
            for user in users:
                if user != self.username:
                    self.client.gui.update_users_list(user)
        elif received == "12\n":
            self.username = self.client.gui.login_user_msg.get()
            pw_msg = "LoginP" + self.client.gui.login_pw_msg.get()
            pw_hash_msg = "LoginP" + self.client.hashPw(self.client.gui.register_pw_msg.get())
            self.send(pw_msg)
        elif received == "13\n":
            self.username = self.client.gui.register_user_msg.get()
            pw_msg = "RegP" + self.client.gui.register_pw_msg.get()
            pw_hash_msg = "RegP" + self.client.hashPw(self.client.gui.register_pw_msg.get())
            self.send(pw_msg)
        elif received == "14\n":
            self.complete_tcp()
        elif received == "15\n":
            self.complete_tcp()
        elif received == "40\n":
            self.client.gui.info_label_msg.set("Fehler")
        elif received == "41\n":
            self.client.gui.info_label_msg.set("Leeres Feld")
        elif received == "42\n":
            self.client.gui.login_user_msg.set("")
            self.client.gui.login_pw_msg.set("")
            self.client.gui.info_label_msg.set("Benutzername nicht gefunden")
        elif received == "43\n" or received == "44\n":
            self.client.gui.info_label_msg.set("Benutzername ist schon vergeben!")
        elif received == "45\n":
            self.client.gui.login_user_msg.set("")
            self.client.gui.login_pw_msg.set("")
            self.client.gui.info_label_msg.set("Falsches Passwort")

        elif received.startswith("30"):
            self.client.gui.chatrequest_window.deiconify()
            chatanswer = received.replace("\n", "").split("*")
            self.client.udp.setConnection(chatanswer[1], chatanswer[2])
        elif received == "0\n":
            print("Chat abgelehnt")
            self.client.gui.show_chatrefused()
        elif received == "1\n":
            self.client.udp.setConnection(self.client.udpServer.name, self.client.udpServer.port)
            self.client.gui.show_chat_window()
            print("Chat angenommen")





    def register(self, event=None):
        user_msg = "RegU" + self.client.gui.register_user_msg.get()
        self.send(user_msg)

    def login(self, event=None):
        user_msg = "LoginU" + self.client.gui.login_user_msg.get()
        self.send(user_msg)

    def complete_tcp(self):
        self.client.gui.root.deiconify()
        self.client.gui.top.destroy()
        self.users_list()

    def users_list(self):
        self.send("list")

    def send_chatrequest(self):
        print("Chat" + self.client.chatPartner + "*" + str(self.client.udp.serverName) + "*" + str(self.client.udp.serverPort))
        self.send("Chat" + self.client.chatPartner + "*" + str(self.client.udp.serverName) + "*" + str(self.client.udp.serverPort))

    def send_chatanswer(self,answer):
        print(answer)
        if answer == "1":
            self.client.udp.connect()
            self.client.gui.show_chat_window()
        self.client.gui.chatrequest_window.withdraw()
        self.send(answer)
        return
