from tkinter import *
from threading import Thread
import queue as queue
import sys


class Gui(object):
    def __init__(self,client):

        self.client = client
        self.root = Tk()
        self.root.geometry("%dx%d%+d%+d" % (200, 400, 1000, 200))
        self.root.withdraw()
        self.root.title("Chat")

        self.top = Toplevel()
        self.top.geometry("%dx%d%+d%+d" % (300, 300, 1000, 200))

        self.register_label = Label(self.top, text="Register here:")
        self.register_user_msg = StringVar()
        self.register_pw_msg = StringVar()
        self.register_user = Entry(self.top, textvariable=self.register_user_msg)
        self.register_pw = Entry(self.top,textvariable=self.register_pw_msg)
        self.register_btn = Button(self.top, text="Register", command=self.register)
        self.info_label_msg = StringVar()
        self.info_label = Label(self.top, textvariable=self.info_label_msg)

        self.login_label = Label(self.top, text="Login here:")
        self.login_user_msg = StringVar()
        self.login_pw_msg = StringVar()
        self.login_user = Entry(self.top, textvariable=self.login_user_msg)
        self.login_pw = Entry(self.top, textvariable=self.login_pw_msg)
        self.login_btn = Button(self.top, text="Login", command=self.login)

        self.close_btn = Button(self.top, text="Close", command=self.close)
        self.register_label.pack()
        self.register_user.pack()
        self.register_pw.pack()
        self.register_btn.pack()
        self.info_label.pack()
        self.login_label.pack()
        self.login_user.pack()
        self.login_pw.pack()
        self.login_btn.pack()
        self.close_btn.pack()

        self.userlist_box = Frame()
        self.userlist = Listbox(self.userlist_box, selectmode="browse", height=20)
        self.userlist_refresh_btn = Button(text="Refresh", command =self.refresh_user_list)
        self.userlist_btn = Button(text="Chatten", command=self.client.choose_chat)

        scrollbar = Scrollbar(self.userlist_box, orient="vertical")
        scrollbar.config(command=self.userlist.yview)
        scrollbar.pack(side="right", fill="y")

        self.userlist_box.pack()
        self.userlist.pack()
        self.userlist_btn.pack()
        self.userlist_refresh_btn.pack()

        self.chatrequest_window = Toplevel()
        self.chatrequest_window.geometry("%dx%d%+d%+d" % (100, 100, 800, 200))
        self.chat_request_label = Label(self.chatrequest_window, text="You got a chat request")
        self.chatrequest_accept_btn = Button(self.chatrequest_window, text="Accept", command=lambda: self.client.tcp.send_chatanswer("1"))
        self.chatrequest_decline_btn = Button(self.chatrequest_window, text="Decline", command=lambda: self.client.tcp.send_chatanswer("0"))
        self.chat_request_label.pack()
        self.chatrequest_accept_btn.pack()
        self.chatrequest_decline_btn.pack()
        self.chatrequest_window.withdraw()

        self.chat_refused_window = Toplevel()
        self.chat_refused_window.geometry("%dx%d%+d%+d" % (200, 100, 1000, 200))
        self.chat_refused_label = Label(self.chat_refused_window, text="Your chatrequest got refused :(")
        self.chatrefused_accept_btn = Button(self.chat_refused_window, text="ok", command=lambda: self.chat_refused_window.withdraw())
        self.chat_refused_label.pack()
        self.chatrefused_accept_btn.pack()
        self.chat_refused_window.withdraw()

        self.chat_window = Toplevel()
        self.chat_window.geometry("%dx%d%+d%+d" % (800, 600, 800, 200))
        self.chat_box = Frame(self.chat_window)
        self.s_msg = StringVar()
        self.msg_list = Listbox(self.chat_box, height=34, width=120)
        self.chat_msg = Entry(self.chat_box, textvariable=self.s_msg)
        self.send_button = Button(self.chat_box, text="Senden", command=self.client.send_udp_txt)
        self.hidechat_btn = Button(self.chat_box, text="Ende", command=self.hide_chat_window)

        scrollbar = Scrollbar(self.chat_box, orient="vertical")
        scrollbar.config(command=self.msg_list.yview)
        scrollbar.pack(side="right", fill="y")
        self.chat_box.pack()
        self.chat_window.withdraw()

        self.msg_list.pack(fill=X)
        self.chat_msg.bind("<Return>", self.client.send_udp_txt)
        self.chat_msg.pack(fill=X)
        self.hidechat_btn.pack(side=LEFT)
        self.send_button.pack(side=RIGHT)

        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.login_user_msg.set("Max")
        self.login_pw_msg.set("hallo")

        self.queue = queue.Queue()
        self.queue_check()


    def register(self):
        self.client.tcp.register()

    def login(self):
        self.client.tcp.login()

    def refresh_user_list(self):
        self.userlist.delete(0, END)
        self.client.tcp.users_list()

    def update_msg_list(self, msg):
        m = 125
        if len(msg) >= m:
            message = [msg[i: i + m] for i in range(0, len(msg), m)]
            for e in message:
                self.msg_list.insert(END, e)
        else:
            self.msg_list.insert(END, msg)

    def update_users_list(self, user):
        self.userlist.insert(END, user)

    def show_chat_window(self):
        self.root.withdraw()
        self.chat_window.deiconify()

    def hide_chat_window(self):
        self.client.udp.disconnect()
        self.msg_list.delete(0, END)
        self.client.tcp.send("31");
        self.root.deiconify()
        self.chat_window.withdraw()

    def close(self):
        test = Thread(target=self.client.quit)
        test.start()
        self.top.destroy()
        self.chat_window.destroy()
        self.chatrequest_window.destroy()
        self.root.destroy()
        test.join()

    def queue_check(self):
        try:
            item = str(self.queue.get_nowait())
            print("updated gui")
            self.update_msg_list(item)
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.queue_check)

    def show_chatrefused(self):
        self.chat_refused_window.deiconify()










