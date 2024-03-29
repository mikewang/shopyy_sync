#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# GUI module generated by PAGE version 4.26
#  in conjunction with Tcl version 8.6
#    Jan 02, 2020 08:51:17 PM CST  platform: Windows NT

import sys
from PIL import Image, ImageTk

import doctor_support
import os.path

login_userid = 0
login_username = ""

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


def vp_start_gui(manager_support=None):
    '''Starting point when module is the main routine.'''
    global val, w, root
    global prog_location
    prog_call = sys.argv[0]
    prog_location = os.path.split(prog_call)[0]
    root = tk.Tk()
    top = Toplevel1(root)
    doctor_support.set_Tk_var()
    doctor_support.init(root, top)
    doctor_support.load_all_patient()
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

    top = Toplevel1(w)
    import doctor_support
    doctor_support.set_Tk_var()
    doctor_support.init(w, top, *args, **kwargs)
    doctor_support.load_all_patient()
    return w, top


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
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#ececec'  # Closest X11 color: 'gray92'
        font10 = "-family 华文楷体 -size 16 -weight normal -slant roman " \
                 "-underline 0 -overstrike 0"
        font12 = "-family 华文楷体 -size 16 -weight normal -slant roman " \
                 "-underline 0 -overstrike 0"
        font13 = "-family 楷体 -size 22 -weight normal -slant roman " \
                 "-underline 0 -overstrike 0"
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.', background=_bgcolor)
        self.style.configure('.', foreground=_fgcolor)
        self.style.configure('.', font="TkDefaultFont")
        self.style.map('.', background=
        [('selected', _compcolor), ('active', _ana2color)])

        top.geometry("1004x771+544+149")
        top.minsize(152, 1)
        top.maxsize(1924, 1055)
        top.resizable(1, 1)
        global login_username
        top.title("医生: " + login_username)
        top.configure(background="#d9d9d9")

        self.canvas = tk.Canvas(root, height=100, width=500)  # 创建画布
        self.image_file = tk.PhotoImage(file="bj.gif")  # 加载图片文件
        self.image = self.canvas.create_image(0, 0, anchor='nw', image=self.image_file)  # 将图片置于画布上
        self.canvas.pack(side='top', fill='both', expand=1)  # 放置画布（为上端）
        root.attributes("-alpha", 1)

        self.Canvas1 = tk.Canvas(top)
        self.Canvas1.place(relx=0.12, rely=0.104, relheight=0.704, relwidth=0.76)
        self.Canvas1.place(relx=0, rely=0, relheight=1, relwidth=1)

        self.Canvas1.configure(background="#FFFFF0")
        self.Canvas1.configure(borderwidth="2")
        self.Canvas1.configure(insertbackground="black")
        self.Canvas1.configure(relief="ridge")
        self.Canvas1.configure(selectbackground="#c4c4c4")
        self.Canvas1.configure(selectforeground="black")

        def callbackPatient(*args):
            s = self.Combobox_patient.get()
            import doctor_support
            doctor_support.load_current_patient_mr()

        self.Label_patientname = tk.Label(self.Canvas1)
        location_x = 10
        location_y = 10
        component_w = 100
        self.Label_patientname.place(x=location_x, y=location_y, height=44, width=component_w)
        self.Label_patientname.configure(background="#FFFFF0")
        self.Label_patientname.configure(disabledforeground="#a3a3a3")
        self.Label_patientname.configure(font="TkFixedFont")
        self.Label_patientname.configure(foreground="#000000")
        self.Label_patientname.configure(text='''待诊病人列表''')

        self.Combobox_patient = ttk.Combobox(self.Canvas1)
        location_x = location_x + component_w
        component_w = 200

        self.Combobox_patient.place(x=location_x, y=location_y+10, height=34, width=component_w)

        self.Combobox_patient.configure(textvariable=tk.StringVar())
        self.Combobox_patient.configure(takefocus="")
        self.Combobox_patient.configure(values=[])
        self.Combobox_patient["state"] = "readonly"
        self.Combobox_patient.bind("<<ComboboxSelected>>", callbackPatient)

        self.Label_patientname = tk.Label(self.Canvas1)
        location_x = location_x + component_w
        component_w = 150
        self.Label_patientname.place(x=location_x, y=location_y, height=44, width=component_w)
        self.Label_patientname.configure(background="#FFFFF0")
        self.Label_patientname.configure(disabledforeground="#a3a3a3")
        self.Label_patientname.configure(font="TkFixedFont")
        self.Label_patientname.configure(foreground="#000000")
        self.Label_patientname.configure(text='''请输入病人名称''')

        v = tk.StringVar()
        self.Entry_patientname = tk.Entry(self.Canvas1, textvariable=v)
        location_x = location_x + component_w
        component_w = 150
        self.Entry_patientname.place(x=location_x, y=location_y+5, height=34, width=component_w)
        self.Entry_patientname.configure(background="white")
        self.Entry_patientname.configure(disabledforeground="#a3a3a3")
        self.Entry_patientname.configure(font="TkFixedFont")
        self.Entry_patientname.configure(foreground="#000000")
        self.Entry_patientname.configure(highlightbackground="#d9d9d9")
        self.Entry_patientname.configure(highlightcolor="black")
        self.Entry_patientname.configure(insertbackground="black")
        self.Entry_patientname.configure(selectbackground="#c4c4c4")
        self.Entry_patientname.configure(selectforeground="black")

        self.Button_queryPatient = tk.Button(self.Canvas1)
        location_x = location_x + component_w + 10
        component_w = 100
        self.Button_queryPatient.place(x=location_x, y=location_y+5, height=34, width=component_w)
        self.Button_queryPatient.configure(activebackground="#ececec")
        self.Button_queryPatient.configure(activeforeground="#000000")
        self.Button_queryPatient.configure(background="#d9d9d9")
        self.Button_queryPatient.configure(command=doctor_support.load_part_patient)
        self.Button_queryPatient.configure(disabledforeground="#a3a3a3")
        self.Button_queryPatient.configure(font="TkFixedFont")
        self.Button_queryPatient.configure(foreground="#000000")
        self.Button_queryPatient.configure(highlightbackground="#d9d9d9")
        self.Button_queryPatient.configure(highlightcolor="black")
        self.Button_queryPatient.configure(pady="0")
        self.Button_queryPatient.configure(text='''查询所有病人''')


        self.Button_adminPatient = tk.Button(self.Canvas1)
        location_x = location_x + component_w + 10
        component_w = 250
        self.Button_adminPatient.place(x=location_x, y=location_y+5, height=34, width=component_w)
        self.Button_adminPatient.configure(activebackground="#ececec")
        self.Button_adminPatient.configure(activeforeground="#000000")
        self.Button_adminPatient.configure(background="#d9d9d9")
        self.Button_adminPatient.configure(command=doctor_support.admin_patient)
        self.Button_adminPatient.configure(disabledforeground="#a3a3a3")
        self.Button_adminPatient.configure(font="TkFixedFont")
        self.Button_adminPatient.configure(foreground="#000000")
        self.Button_adminPatient.configure(highlightbackground="#d9d9d9")
        self.Button_adminPatient.configure(highlightcolor="black")
        self.Button_adminPatient.configure(pady="0")
        self.Button_adminPatient.configure(text='''增加或修改或删除病人信息''')



        #主体信息
        self.Label_pt_name = tk.Label(self.Canvas1)
        location_x = 10
        location_y = location_y + 44 + 20
        component_w = 250

        self.Label_pt_name.place(x=location_x, y=location_y, height=44, width=component_w)
        self.Label_pt_name.configure(activebackground="#f9f9f9")
        self.Label_pt_name.configure(activeforeground="black")
        self.Label_pt_name.configure(background="#FFFFF0")
        self.Label_pt_name.configure(cursor="fleur")
        self.Label_pt_name.configure(disabledforeground="#a3a3a3")
        self.Label_pt_name.configure(font=font12)
        self.Label_pt_name.configure(foreground="#000000")
        self.Label_pt_name.configure(highlightbackground="#d9d9d9")
        self.Label_pt_name.configure(highlightcolor="black")
        self.Label_pt_name.configure(text='''病人名称:-请下拉选择-''')

        self.Label_type_name = tk.Label(self.Canvas1)
        location_x = location_x + component_w
        component_w = 100

        self.Label_type_name.place(x=location_x, y=location_y, height=44, width=component_w)
        self.Label_type_name.configure(activebackground="#f9f9f9")
        self.Label_type_name.configure(activeforeground="black")
        self.Label_type_name.configure(background="#FFFFF0")
        self.Label_type_name.configure(cursor="fleur")
        self.Label_type_name.configure(disabledforeground="#a3a3a3")
        self.Label_type_name.configure(font=font12)
        self.Label_type_name.configure(foreground="#000000")
        self.Label_type_name.configure(highlightbackground="#d9d9d9")
        self.Label_type_name.configure(highlightcolor="black")
        self.Label_type_name.configure(text='''类型''')

        self.Radiobutton_pt_type1 = tk.Radiobutton(self.Canvas1)
        location_x = location_x + component_w
        component_w = 100

        self.Radiobutton_pt_type1.place(x=location_x, y=location_y, height=44, width=component_w)
        self.Radiobutton_pt_type1.configure(activebackground="#ececec")
        self.Radiobutton_pt_type1.configure(activeforeground="#000000")
        self.Radiobutton_pt_type1.configure(background="#ffffff")
        #self.Radiobutton_pt_type1.configure(command=login_support.user_login)
        self.Radiobutton_pt_type1.configure(cursor="hand2")
        self.Radiobutton_pt_type1.configure(disabledforeground="#a3a3a3")
        self.Radiobutton_pt_type1.configure(font="-family {Microsoft YaHei UI} -size 11")
        self.Radiobutton_pt_type1.configure(foreground="#000000")
        self.Radiobutton_pt_type1.configure(highlightbackground="#d9d9d9")
        self.Radiobutton_pt_type1.configure(highlightcolor="black")
        self.Radiobutton_pt_type1.configure(justify='left')
        self.Radiobutton_pt_type1.configure(text='''初诊''')
        self.Radiobutton_pt_type1.configure(value="0")
        self.Radiobutton_pt_type1.configure(variable=doctor_support.mr_type)

        self.Radiobutton_pt_type2 = tk.Radiobutton(self.Canvas1)
        location_x = location_x + component_w
        component_w = 100

        self.Radiobutton_pt_type2.place(x=location_x, y=location_y, height=44, width=component_w)
        self.Radiobutton_pt_type2.configure(activebackground="#ececec")
        self.Radiobutton_pt_type2.configure(activeforeground="#000000")
        self.Radiobutton_pt_type2.configure(background="#ffffff")
        # self.Radiobutton_pt_type2.configure(command=login_support.manager_login)
        self.Radiobutton_pt_type2.configure(cursor="hand2")
        self.Radiobutton_pt_type2.configure(disabledforeground="#a3a3a3")
        self.Radiobutton_pt_type2.configure(font="-family {Microsoft YaHei UI} -size 11")
        self.Radiobutton_pt_type2.configure(foreground="#000000")
        self.Radiobutton_pt_type2.configure(highlightbackground="#d9d9d9")
        self.Radiobutton_pt_type2.configure(highlightcolor="black")
        self.Radiobutton_pt_type2.configure(justify='left')
        self.Radiobutton_pt_type2.configure(text='''复诊''')
        self.Radiobutton_pt_type2.configure(value="1")
        self.Radiobutton_pt_type2.configure(variable=doctor_support.mr_type)

        self.Label_mr_date = tk.Label(self.Canvas1)
        location_x = location_x + component_w + 10
        component_w = 240

        mr_date_str = tk.StringVar()
        import time
        mr_date_str = time.strftime('%Y-%m-%d', time.localtime(time.time()))

        self.Label_mr_date.place(x=location_x, y=location_y, height=44, width=component_w)
        self.Label_mr_date.configure(activebackground="#f9f9f9")
        self.Label_mr_date.configure(activeforeground="black")
        self.Label_mr_date.configure(background="#FFFFF0")
        self.Label_mr_date.configure(cursor="fleur")
        self.Label_mr_date.configure(disabledforeground="#a3a3a3")
        self.Label_mr_date.configure(font=font12)
        self.Label_mr_date.configure(foreground="#000000")
        self.Label_mr_date.configure(highlightbackground="#d9d9d9")
        self.Label_mr_date.configure(highlightcolor="black")
        self.Label_mr_date.configure(text='''诊断日期:''' + mr_date_str)

        self.Button_last_mrid = tk.Button(self.Canvas1)
        location_x = location_x + component_w + 10
        component_w = 150
        self.Button_last_mrid.place(x=location_x, y=location_y+5, height=34, width=component_w)
        self.Button_last_mrid.configure(activebackground="#ececec")
        self.Button_last_mrid.configure(activeforeground="#000000")
        self.Button_last_mrid.configure(background="#d9d9d9")
        self.Button_last_mrid.configure(command=doctor_support.mr_list)
        self.Button_last_mrid.configure(disabledforeground="#a3a3a3")
        self.Button_last_mrid.configure(font=font10)
        self.Button_last_mrid.configure(foreground="#000000")
        self.Button_last_mrid.configure(highlightbackground="#d9d9d9")
        self.Button_last_mrid.configure(highlightcolor="black")
        self.Button_last_mrid.configure(pady="0")
        self.Button_last_mrid.configure(text='''历史病历''')

        self.Text_mr_result = tk.Text(self.Canvas1)
        location_x = 10
        location_y = location_y + 44
        component_w = 950
        self.Text_mr_result.place(x=location_x, y=location_y+5, height=550, relwidth=0.96)

        self.Button1 = tk.Button(self.Canvas1)
        self.Button1.place(relx=0.18, rely=0.91, height=63, width=100)
        self.Button1.configure(activebackground="#ececec")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(command=doctor_support.logout)
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(font=font10)
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''退出登录''')

        self.Button2 = tk.Button(self.Canvas1)
        self.Button2.place(relx=0.48, rely=0.91, height=63, width=100)
        self.Button2.configure(activebackground="#ececec")
        self.Button2.configure(activeforeground="#000000")
        self.Button2.configure(background="#d9d9d9")
        self.Button2.configure(command=doctor_support.save_current_patient_mr)
        self.Button2.configure(disabledforeground="#a3a3a3")
        self.Button2.configure(font=font10)
        self.Button2.configure(foreground="#000000")
        self.Button2.configure(highlightbackground="#d9d9d9")
        self.Button2.configure(highlightcolor="black")
        self.Button2.configure(pady="0")
        self.Button2.configure(text='''确定保存''')

    @staticmethod
    def popup1(event, *args, **kwargs):
        Popupmenu1 = tk.Menu(root, tearoff=0)
        Popupmenu1.configure(activebackground="#f9f9f9")
        Popupmenu1.configure(activeborderwidth="1")
        Popupmenu1.configure(activeforeground="black")
        Popupmenu1.configure(background="#d9d9d9")
        Popupmenu1.configure(borderwidth="1")
        Popupmenu1.configure(disabledforeground="#a3a3a3")
        Popupmenu1.configure(font="{Microsoft YaHei UI} 9")
        Popupmenu1.configure(foreground="black")
        Popupmenu1.post(event.x_root, event.y_root)


if __name__ == '__main__':
    vp_start_gui()
