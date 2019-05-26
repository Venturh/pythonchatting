from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from tkinter import *
from Gui import Gui


class Client:

    def __init__(self, server, port):
        self.server = server
        self.port = port
        self.socket = None
        self.connected = False
        self.gui = Gui(self)
        self.thread = None

    def connect(self):
        try:
            self.socket = socket(AF_INET, SOCK_STREAM)
            self.socket.connect((self.server, self.port))
            self.gui.connect_button.destroy()
        except socket.timeout:
            print("Verbindung getrennt")
            self.gui.connect_button.pack()
        finally:
            self.connected = True
            self.thread = Thread(target=client.receive)
            self.thread.start()

    def receive(self):
        while True:
            try:
                received = self.socket.recv(1024)
                self.gui.msg_list.insert(END, received)
            except OSError:
                break

    def send(self, event=None):
        msg = self.gui.s_msg.get()
        self.gui.s_msg.set("")
        self.socket.send(bytes(msg + "\n", "utf-8"))

    def quit(self):
        if self.connected:
            self.socket.close()
        self.gui.root.quit()


if __name__ == "__main__":
    client = Client("localhost", 27999)
    mainloop()




