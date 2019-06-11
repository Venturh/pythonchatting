from tkinter import *
from Gui import Gui
from UdpServer import UdpServer
from Udp import Udp
from Tcp import Tcp
from threading import *


class Client(object):

    def __init__(self):
        self.gui = Gui(self)
        self.tcp = Tcp("localhost", 27999, self)
        self.udp = Udp(self)


    def send_udp_txt(self):
        msg = self.gui.s_msg.get()
        self.gui.s_msg.set("")
        self.udp.send(msg)

    def choose_chat(self):
        choose_list = self.gui.userlist.curselection()
        item = choose_list[0]
        choosed = self.gui.userlist.get(item)
        print(choosed)
        self.gui.chat_box.pack()
        self.udp.connect()

    def quit(self):
        self.tcp.tcp_socket.close()
        self.gui.root.quit()

    def logout(self):
        self.tcp.tcp_socket.close()
        self.udp.clientSocket.close()
        self.udpServer.socket.close()
        self.gui.root.destroy()
        sys.exit(0)


if __name__ == "__main__":
    client = Client()
    mainloop()




