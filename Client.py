from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from tkinter import *
from Gui import Gui


class Client:

    def __init__(self, server, port):
        self.server = server
        self.port = port
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.connected = True
        self.gui = Gui(self)
        self.thread = None
        self.socket.connect((self.server, self.port))

    def receive(self):
        while True:
            try:
                received = self.socket.recv(1024)
                self.gui.msg_list.insert(END, received)
            except OSError:
                break

    def send(self, msg):
        self.socket.send(bytes(msg + "\n", "utf-8"))

    def send_txt(self, event=None):
        msg = self.gui.s_msg.get()
        self.gui.s_msg.set("")
        self.send(msg)

    def register(self, event=None):
        user_msg = "RegU" + self.gui.register_user_msg.get()
        pw_msg = "RegP" + self.gui.register_pw_msg.get()
        self.send(user_msg)

        received = self.socket.recv(1024).decode("utf-8")
        if received == "error: username taken\n":
            self.gui.info_label_msg.set("Benutzername ist schon vergeben!")
            return
        elif self.gui.register_user_msg.get() == "":
            self.gui.info_label_msg.set("Leeres Feld")
            return

        self.gui.info_label_msg.set(received)
        self.send(pw_msg)
        received = self.socket.recv(1024).decode("utf-8")
        if self.gui.register_pw_msg.get() == "":
            self.gui.info_label_msg.set("Leeres Feld")
        else:
            self.gui.info_label_msg.set(received)
            self.gui.root.deiconify()
            self.gui.top.destroy()
            self.thread = Thread(target=client.receive)
            self.thread.start()

    def login(self, event=None):
        user_msg = "LoginU" + self.gui.login_user_msg.get()
        pw_msg = "LoginP" + self.gui.login_pw_msg.get()

        self.send(user_msg)
        received = self.socket.recv(1024).decode("utf-8")
        if received == "error: username empty\n":
            self.gui.login_user_msg.set("")
            self.gui.login_pw_msg.set("")
            self.gui.info_label_msg.set(received)
            return
        elif received == "error: username not found\n":
            self.gui.login_user_msg.set("")
            self.gui.login_pw_msg.set("")
            self.gui.info_label_msg.set(received)
            return
        elif received == "unknown command\n":
            self.gui.info_label_msg.set(received)
            return

        self.send(pw_msg)
        received = self.socket.recv(1024).decode("utf-8")
        if received == "error: password empty\n":
            self.gui.login_user_msg.set("")
            self.gui.login_pw_msg.set("")
            self.gui.info_label_msg.set(received)
        elif received == "error: password wrong\n":
            self.gui.login_user_msg.set("")
            self.gui.login_pw_msg.set("")
            self.gui.info_label_msg.set(received)
        else:
            print(received)
            self.gui.root.deiconify()
            self.gui.top.destroy()
            self.thread = Thread(target=client.receive)
            self.thread.start()

    def quit(self):
        if self.connected:
            self.socket.close()
        self.gui.root.quit()

    def logout(self):
        self.send("end")
        self.gui.root.destroy()
        self.thread.join()
        sys.exit(0)


if __name__ == "__main__":
    client = Client("localhost", 27999)
    mainloop()




