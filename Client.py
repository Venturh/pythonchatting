from tkinter import *
from Gui import Gui
from UdpServer import UdpServer
from Udp import Udp
from Tcp import Tcp
from threading import *

# BUGS:


class Client(object):

    def __init__(self):
        self.gui = Gui(self)
        self.tcp = Tcp("localhost", 27999, self)
        self.udp = Udp(self)
        self.udpServer = UdpServer(self)
        self.chatPartner = "";

    def send_udp_txt(self, event=None):
        msg = self.gui.s_msg.get()
        self.gui.s_msg.set("")
        self.udp.send(msg, 0)


    def choose_chat(self):
        choose_list = self.gui.userlist.curselection()
        item = choose_list[0]
        choosed = self.gui.userlist.get(item)
        self.chatPartner = choosed;
        print(choosed)
        self.tcp.send_chatrequest()
        self.udp.connect()

    def quit(self):
        self.tcp.thread.join()
        self.tcp.socket.detach()
        self.udp.thread.join()
        self.udp.clientSocket.close()
        self.udpServer.udpserver_thread.join()
        self.udpServer.close()


if __name__ == "__main__":
    client = Client()
    client.tcp.thread.start()
    client.udp.thread.start()
    client.udpServer.udpserver_thread.start()
    mainloop()




