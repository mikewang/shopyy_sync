#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#


import sys

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

from PIL import Image, ImageTk

import login_support
import os.path

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    global prog_location
    prog_call = sys.argv[0]
    prog_location = os.path.split(prog_call)[0]
    root = tk.Tk()
    login_support.set_Tk_var()
    top = Toplevel1(root)
    login_support.init(root, top)
    root.mainloop()

w = None
def create_Toplevel1(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    global prog_location
    prog_call = sys.argv[0]
    prog_location = os.path.split(prog_call)[0]
    rt = root
    w = tk.Toplevel(root)
    login_support.set_Tk_var()
    top = Toplevel1(w)
    login_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_Toplevel1():
    global w
    w.destroy()
    w = None

class Toplevel1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'

        top.geometry("830x641+478+126")
        top.minsize(152, 1)
        top.maxsize(1604, 881)
        top.resizable(1, 1)
        top.title("病历管理系统")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="#000000")

        self.Canvas1 = tk.Canvas(top)
        self.Canvas1.place(relx=0.3, rely=0.312, relheight=0.613, relwidth=0.461)

        self.Canvas1.configure(background="#ffffff")
        self.Canvas1.configure(borderwidth="2")
        self.Canvas1.configure(highlightbackground="#d9d9d9")
        self.Canvas1.configure(highlightcolor="black")
        self.Canvas1.configure(insertbackground="black")
        self.Canvas1.configure(relief="ridge")
        self.Canvas1.configure(selectbackground="#c4c4c4")
        self.Canvas1.configure(selectforeground="black")
        self.Canvas1 = tk.Canvas(root, height=100, width=500)  # 创建画布
        self.image_file = tk.PhotoImage(file="bj.jpg")  # 加载图片文件
        self.image = self.Canvas1.create_image(0, 0, anchor='nw', image=self.image_file)  # 将图片置于画布上
        self.Canvas1.pack(side='top', fill='both', expand=1)  # 放置画布（为上端）
        root.attributes("-alpha", 1)

        self.Canvas1 = tk.Canvas(top)
        self.Canvas1.place(relx=0.53, rely=0.312, relheight=0.613, relwidth=0.461)
        self.Canvas1.configure(background="#ffffff")
        self.Canvas1.configure(borderwidth="2")
        self.Canvas1.configure(highlightbackground="#d9d9d9")
        self.Canvas1.configure(highlightcolor="black")
        self.Canvas1.configure(insertbackground="black")
        self.Canvas1.configure(relief="ridge")
        self.Canvas1.configure(selectbackground="#c4c4c4")
        self.Canvas1.configure(selectforeground="black")

        self.Label1 = tk.Label(self.Canvas1)
        self.Label1.place(relx=0.052, rely=0.178, height=42, width=41)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(activeforeground="black")
        self.Label1.configure(background="#d9d9d9")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(highlightbackground="#d9d9d9")
        self.Label1.configure(highlightcolor="black")
        photo_location = os.path.join(prog_location,"user.png")
        global _img0
        _img0 = tk.PhotoImage(file=photo_location)
        self.Label1.configure(image=_img0)
        self.Label1.configure(text='''Label''')

        self.Label2 = tk.Label(self.Canvas1)
        self.Label2.place(relx=0.052, rely=0.382, height=48, width=38)
        self.Label2.configure(activebackground="#f9f9f9")
        self.Label2.configure(activeforeground="black")
        self.Label2.configure(background="#d9d9d9")
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(highlightbackground="#d9d9d9")
        self.Label2.configure(highlightcolor="black")
        photo_location = os.path.join(prog_location,"password.jpg")
        global _img1
        _img1 = ImageTk.PhotoImage(file=photo_location)
        self.Label2.configure(image=_img1)
        self.Label2.configure(text='''Label''')

        self.Label3 = tk.Label(self.Canvas1)
        self.Label3.place(relx=0.261, rely=0.204, height=30, width=42)
        self.Label3.configure(activebackground="#f9f9f9")
        self.Label3.configure(activeforeground="black")
        self.Label3.configure(background="#ffffff")
        self.Label3.configure(disabledforeground="#a3a3a3")
        self.Label3.configure(font="-family {Microsoft YaHei UI} -size 11")
        self.Label3.configure(foreground="#000000")
        self.Label3.configure(highlightbackground="#d9d9d9")
        self.Label3.configure(highlightcolor="black")
        self.Label3.configure(text='''账号''')

        self.Label4 = tk.Label(self.Canvas1)
        self.Label4.place(relx=0.261, rely=0.382, height=33, width=46)
        self.Label4.configure(activebackground="#f9f9f9")
        self.Label4.configure(activeforeground="black")
        self.Label4.configure(background="#ffffff")
        self.Label4.configure(disabledforeground="#a3a3a3")
        self.Label4.configure(font="-family {Microsoft YaHei UI} -size 12")
        self.Label4.configure(foreground="#000000")
        self.Label4.configure(highlightbackground="#d9d9d9")
        self.Label4.configure(highlightcolor="black")
        self.Label4.configure(text='''密码''')

        self.Entry_userid = tk.Entry(self.Canvas1)
        self.Entry_userid.place(relx=0.418, rely=0.204, height=27, relwidth=0.428)
        self.Entry_userid.configure(background="white")
        self.Entry_userid.configure(disabledforeground="#a3a3a3")
        self.Entry_userid.configure(font="TkFixedFont")
        self.Entry_userid.configure(foreground="#000000")
        self.Entry_userid.configure(highlightbackground="#d9d9d9")
        self.Entry_userid.configure(highlightcolor="black")
        self.Entry_userid.configure(insertbackground="black")
        self.Entry_userid.configure(selectbackground="#c4c4c4")
        self.Entry_userid.configure(selectforeground="black")

        self.Entry_password = tk.Entry(self.Canvas1)
        self.Entry_password.place(relx=0.418, rely=0.382, height=27, relwidth=0.428)
        self.Entry_password.configure(background="white")
        self.Entry_password.configure(disabledforeground="#a3a3a3")
        self.Entry_password.configure(font="TkFixedFont")
        self.Entry_password.configure(foreground="#000000")
        self.Entry_password.configure(highlightbackground="#d9d9d9")
        self.Entry_password.configure(highlightcolor="black")
        self.Entry_password.configure(insertbackground="black")
        self.Entry_password.configure(selectbackground="#c4c4c4")
        self.Entry_password.configure(selectforeground="black")
        self.Entry_password.configure(show="*")

        self.Button1 = tk.Button(self.Canvas1)
        self.Button1.place(relx=0.313, rely=0.687, height=28, width=159)
        self.Button1.configure(activebackground="#ececec")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#09a0dc")
        self.Button1.configure(command=login_support.login)
        self.Button1.configure(cursor="hand2")
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(font="-family {Microsoft YaHei UI} -size 11")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''登录''')

        self.Button2_2 = tk.Button(self.Canvas1)
        self.Button2_2.place(relx=0.783, rely=0.687, height=28, width=45)
        self.Button2_2.configure(activebackground="#ececec")
        self.Button2_2.configure(activeforeground="#000000")
        self.Button2_2.configure(background="#ffffff")
        self.Button2_2.configure(command=login_support.quit)
        self.Button2_2.configure(disabledforeground="#a3a3a3")
        self.Button2_2.configure(font="-family {Microsoft YaHei UI} -size 10")
        self.Button2_2.configure(foreground="#000000")
        self.Button2_2.configure(highlightbackground="#d9d9d9")
        self.Button2_2.configure(highlightcolor="black")
        self.Button2_2.configure(pady="0")
        self.Button2_2.configure(text='''退出''')

        self.Radiobutton1 = tk.Radiobutton(self.Canvas1)
        self.Radiobutton1.place(relx=0.418, rely=0.509, relheight=0.092
                , relwidth=0.175)
        self.Radiobutton1.configure(activebackground="#ececec")
        self.Radiobutton1.configure(activeforeground="#000000")
        self.Radiobutton1.configure(background="#ffffff")
        self.Radiobutton1.configure(command=login_support.user_login)
        self.Radiobutton1.configure(cursor="hand2")
        self.Radiobutton1.configure(disabledforeground="#a3a3a3")
        self.Radiobutton1.configure(font="-family {Microsoft YaHei UI} -size 11")
        self.Radiobutton1.configure(foreground="#000000")
        self.Radiobutton1.configure(highlightbackground="#d9d9d9")
        self.Radiobutton1.configure(highlightcolor="black")
        self.Radiobutton1.configure(justify='left')
        self.Radiobutton1.configure(text='''医生''')
        self.Radiobutton1.configure(value="0")
        self.Radiobutton1.configure(variable=login_support.selectedButton)

        self.Radiobutton2 = tk.Radiobutton(self.Canvas1)
        self.Radiobutton2.place(relx=0.679, rely=0.509, relheight=0.092,relwidth=0.222)
        self.Radiobutton2.configure(activebackground="#ececec")
        self.Radiobutton2.configure(activeforeground="#000000")
        self.Radiobutton2.configure(background="#ffffff")
        self.Radiobutton2.configure(command=login_support.manager_login)
        self.Radiobutton2.configure(cursor="hand2")
        self.Radiobutton2.configure(disabledforeground="#a3a3a3")
        self.Radiobutton2.configure(font="-family {Microsoft YaHei UI} -size 11")
        self.Radiobutton2.configure(foreground="#000000")
        self.Radiobutton2.configure(highlightbackground="#d9d9d9")
        self.Radiobutton2.configure(highlightcolor="black")
        self.Radiobutton2.configure(justify='left')
        self.Radiobutton2.configure(text='''管理员''')
        self.Radiobutton2.configure(value="1")
        self.Radiobutton2.configure(variable=login_support.selectedButton)

        self.menubar = tk.Menu(top,font="TkMenuFont",bg=_bgcolor,fg=_fgcolor)
        top.configure(menu = self.menubar)

if __name__ == '__main__':
    vp_start_gui()





