from tkinter import *
import sys


class Gui(object):
    def __init__(self,client):
        self.client = client
        self.root = Tk()
        self.root.geometry("%dx%d%+d%+d" % (200, 800, 800, 125))
        self.root.withdraw()
        self.root.title("Chat")

        self.top = Toplevel()
        self.top.geometry("%dx%d%+d%+d" % (300, 300, 800, 125))

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

        self.close_btn = Button(self.top, text="Close", command=self.close_top)
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
        self.userlist = Listbox(self.userlist_box, selectmode ="browse")
        self.userlist_refresh_btn = Button(text="Refresh", command =self.refresh_user_list)
        self.userlist_btn = Button(text="Chatten", command=self.client.choose_chat)
        self.userlist_box.pack()
        self.userlist.pack()
        self.userlist_btn.pack()
        self.userlist_refresh_btn.pack()

        self.chat_box = Frame()
        self.s_msg = StringVar()
        self.msg_list = Listbox(self.chat_box, height=30, width=80)
        self.chat_msg = Entry(self.chat_box, textvariable=self.s_msg)
        self.send_button = Button(self.chat_box, text="Senden", command=self.client.send_udp_txt)
        self.logout_button = Button(text="Ausloggen", command=self.client.logout)

        self.root.protocol('WM_DELETE_WINDOW', self.client.quit)
        self.msg_list.pack(fill=BOTH)
        self.chat_box.pack()
        self.chat_msg.bind("<Return>", self.client.send_udp_txt)
        self.chat_msg.pack(fill=X)
        self.send_button.pack()
        self.logout_button.pack()
        self.chat_box.pack_forget()


        self.chatrequest_window = Toplevel()
        self.chatrequest_window.geometry("%dx%d%+d%+d" % (50, 50, 800, 200))
        self.chatrequest_accept_btn = Button(self.chatrequest_window, text="Accept", command=lambda: self.client.tcp.send_chatanswer("accept"))
        self.chatrequest_decline_btn = Button(self.chatrequest_window, text="Decline", command=lambda: self.client.tcp.send_chatanswer("decline"))
        self.chatrequest_accept_btn.pack()
        self.chatrequest_decline_btn.pack()
        self.chatrequest_window.withdraw()

        self.login_user_msg.set("Max")
        self.login_pw_msg.set("hallo")


    def close_top(self):
        self.top.destroy()
        sys.exit()

    def register(self):
        self.client.tcp.register()

    def login(self):
        self.client.tcp.login()

    def refresh_user_list(self):
        self.userlist.delete(0, END)
        self.client.tcp.users_list()

    def update_msg_list(self, msg):
        self.msg_list.insert(END, msg)

    def update_users_list(self, user):
        self.userlist.insert(END, user)





