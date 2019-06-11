from socket import AF_INET, socket, SOCK_STREAM, SOCK_DGRAM


class Tcp(object):

    def __init__(self, tcp_server, tcp_port, client):
        self.client = client
        self.tcp_server = tcp_server
        self.tcp_port = tcp_port
        self.tcp_socket = socket(AF_INET, SOCK_STREAM)
        self.tcp_socket.connect((self.tcp_server, self.tcp_port))
        self.username = ""
        self.passwort = ""

    def send_tcp(self, msg):
        self.tcp_socket.send(bytes(msg + "\n", "utf-8"))

    def register(self, event=None):
        user_msg = "RegU" + self.client.gui.register_user_msg.get()
        pw_msg = "RegP" + self.client.gui.register_pw_msg.get()
        self.send_tcp(user_msg)

        received = self.tcp_socket.recv(1024).decode("utf-8")
        if received == "43\n" or received == "44\n":
            self.client.gui.info_label_msg.set("Benutzername ist schon vergeben!")
            return
        elif received == "41\n":
            self.client.gui.info_label_msg.set("Leeres Feld")
            return

        self.client.gui.info_label_msg.set(received)
        self.send_tcp(pw_msg)
        received = self.tcp_socket.recv(1024).decode("utf-8")
        if received == "41\n":
            self.client.gui.info_label_msg.set("Leeres Feld")
        elif received == "40\n":
            self.client.gui.info_label_msg.set("Fehler")
        else:
            self.complete_tcp()

    def login(self, event=None):
        user_msg = "LoginU" + self.client.gui.login_user_msg.get()
        pw_msg = "LoginP" + self.client.gui.login_pw_msg.get()

        self.send_tcp(user_msg)
        received = self.tcp_socket.recv(1024).decode("utf-8")
        if received == "41\n":
            self.client.gui.login_user_msg.set("")
            self.client.gui.login_pw_msg.set("")
            self.client.gui.info_label_msg.set("Leeres Feld")
            return
        elif received == "42\n":
            self.client.gui.login_user_msg.set("")
            self.client.gui.login_pw_msg.set("")
            self.client.gui.info_label_msg.set("Benutzername nicht gefunden")
            return
        elif received == "40\n":
            self.client.gui.info_label_msg.set("Fehler")
            return

        self.send_tcp(pw_msg)
        received = self.tcp_socket.recv(1024).decode("utf-8")
        print(received)
        if received == "41\n":
            self.client.gui.login_user_msg.set("")
            self.client.gui.login_pw_msg.set("")
            self.client.gui.info_label_msg.set("Leeres Feld")
        elif received == "45\n":
            self.client.gui.login_user_msg.set("")
            self.client.gui.login_pw_msg.set("")
            self.client.gui.info_label_msg.set("Falsches Passwort")
        else:
            self.complete_tcp()

    def complete_tcp(self):
        self.username = self.client.gui.login_user_msg.get()
        self.client.gui.root.deiconify()
        self.client.gui.top.destroy()
        self.users_list()

    def users_list(self):
        self.send_tcp("10")
        rec = self.tcp_socket.recv(1024).decode("utf-8")
        print(str(rec))
        users = rec.replace("\n", "").split("*")
        print(users)
        for user in users:
            if user != self.username and user != "10":
                self.client.gui.update_users_list(user)
