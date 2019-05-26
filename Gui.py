from tkinter import *


class Gui(object):
    def __init__(self, client):
        self.client = client
        self.root = Tk()
        self.root.geometry('800x600')
        self.chat_box = Frame()

        self.s_msg = StringVar()
        self.msg_list = Listbox(self.chat_box, height=30, width=80)
        self.chat_msg = Entry(textvariable=self.s_msg)
        self.send_button = Button(text="Senden", command=client.send)
        self.connect_button = Button(text="Verbiden", command=client.connect)

        self.setup()

    def setup(self):
        self.root.title("Chat")
        self.root.protocol('WM_DELETE_WINDOW', self.client.quit)
        self.connect_button.pack()

        self.msg_list.pack(fill=BOTH)
        self.chat_box.pack()

        self.chat_msg.bind("<Return>", self.client.send)
        self.chat_msg.pack(fill=X)

        self.send_button.pack()
