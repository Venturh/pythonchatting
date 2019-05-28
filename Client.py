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
        print(msg)
        self.socket.send(bytes(msg + "\n", "utf-8"))

    def quit(self):
        if self.connected:
            self.socket.close()
        self.gui.root.quit()

    def send_txt(self, event=None):
        msg = self.gui.s_msg.get()
        self.gui.s_msg.set("")
        self.send(msg)

    def register(self):
        user_msg = "RegU" + self.gui.register_user_msg.get()
        pw_msg = "RegU" + self.gui.register_pw_msg.get()
        self.send(user_msg)
        self.send(pw_msg)

        received = self.socket.recv(1024).decode("utf-8")
        if received == "Nutzername bereits vergeben":
            self.gui.info_label_msg.set("Benutzername ist schon vergeben!")
        else:
            self.gui.info_label_msg.set("Erfolgreich! Bitte einloggen")
            self.gui.register_user_msg.set("")
            self.gui.register_pw_msg.set("")

    def login(self):
        user_msg = "LoginU" + self.gui.login_user_msg.get()
        pw_msg = "LoginU" + self.gui.login_pw_msg.get()
        self.send(user_msg)
        self.send(pw_msg)

        received = self.socket.recv(1024).decode("utf-8")
        if received == "Nutzername oder Passwort falsch":
            self.gui.login_user_msg.set("")
            self.gui.login_pw_msg.set("")
            self.gui.info_label_msg.set("Falsche Anmeldedaten!")
        elif received == "LoginU"+"\n":
            self.gui.login_user_msg.set("")
            self.gui.login_pw_msg.set("")
            self.gui.info_label_msg.set("Keine Leeren Felder!")
        else:
            print("angemeldet")
            self.gui.root.deiconify()
            self.gui.top.destroy()
            self.thread = Thread(target=client.receive)
            self.thread.start()

    def logout(self):
        self.send("end")
        self.gui.root.destroy()
        self.thread.join()
        sys.exit(0)



if __name__ == "__main__":
    client = Client("localhost", 27999)

    mainloop()




