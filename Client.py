from tkinter import *
from Gui import Gui
from UdpServer import UdpServer
from Udp import Udp
from Tcp import Tcp
import hashlib

# BUGS:


class Client(object):

    def __init__(self):
        self.gui = Gui(self)
        self.tcp = Tcp("localhost", 27999, self)
        self.udpServer = UdpServer(self)
        self.udp = Udp(self, self.udpServer)
        self.chatPartner = "";


    def hashPw(self, toHash):
        print(hashlib.sha256(toHash.encode('utf-8')).hexdigest())
        return hashlib.sha256(toHash.encode('utf-8')).hexdigest()

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


    def quit(self):
        self.tcp.thread.join()
        self.tcp.socket.detach()
        self.udp.thread.join()
        self.udp.clientSocket.close()
        self.udpServer.udpserver_thread.join()
        self.udpServer.close()


if __name__ == "__main__":
    client = Client()
    client.hashPw("hallo")
    mainloop()




