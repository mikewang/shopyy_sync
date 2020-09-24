# 导入tkinter必要的模块
import tkinter as tk
import sqlite3

import numpy as np
import matplotlib.pyplot as plt

import time
import tkinter.messagebox as tkm

def procinit1():  # 清空文本框内容
    entryXh.delete(0, 'end')
    entryXm.delete(0, 'end')
    entryXb.delete(0, 'end')
    entrySy.delete(0, 'end')
    entrySytj.delete(0, 'end')
    entryXbtj.delete(0, 'end')
    entryXstj.delete(0, 'end')
    entrySrsf.delete(0, 'end')
    entrySrxb.delete(0, 'end')
    entrySrxs.delete(0, 'end')


def procinit2():  # 读取文本框内容
    Xh = entryXh.get()
    Xm = entryXm.get()
    Xb = entryXb.get()
    Sy = entrySy.get()
    sr = (Xh, Xm, Xb, Sy)
    return sr


def proc1():  # '插入记录'按钮关联的事件程序
    studdb = sqlite3.connect("student.db")  # 定义/打开数据库student.db，建立数据库连接对象studdb
    studcur = studdb.cursor()  # 创建一个游标对象studcur
    Xh = entryXh.get()
    print(Xh)
    Xm = entryXm.get()
    Xb = entryXb.get()
    Sy = entrySy.get()
    sql = "Insert into stud values (?,?,?,?)"
    studcur.execute(sql, (Xh, Xm, Xb, Sy))  # 执行插入命令
    procinit1()  # 清空文本框
    studdb.commit()
    studdb.close();  # 关闭数据库连接


def proc2():  # '删除记录'按钮关联的事件程序
    studdb = sqlite3.connect("student.db")  # 定义/打开数据库student.db，建立数据库连接对象studdb
    studcur = studdb.cursor()  # 创建一个游标对象studcur
    Xh = entryXh.get()
    Xh = Xh.strip()  # strip()方法删除Xh两边空格
    sql = "delete from stud where 学号=?"
    studcur.execute(sql, (Xh,))  # 执行删除命令
    procinit1()  # 清空文本框
    studdb.commit()  # ()
    studdb.close();  # 关闭数据库连接


def proc3():  # "修改记录"按钮关联的事件程序
    studdb = sqlite3.connect("student.db")  # 定义/打开数据库student.db，建立数据库连接对象studdb
    studcur = studdb.cursor()  # 创建一个游标对象studcur
    Xh = entryXh.get()
    Xh = Xh.strip()  # strip()方法删除Xh两边空格
    sql = "select * from stud where 学号=?"
    studcur.execute(sql, (Xh,))
    # res=studcur.fetchone()     #res是元组
    res = studcur.fetchall()  # res是元组构成的列表
    if len(res) != 0:
        sr1 = procinit2()  # 读取文本框内容---元组
        ress = list(res[0])  # 元组res[0]转为列表ress
        for i in range(4):
            if sr1[i].strip() != '':
                ress[i] = sr1[i]  # 文本框非空表示需修改
        sql = "update stud set 学号=?,姓名=?,性别=?,生源=? where 学号=?"
        # 方法一：res=tuple(ress)   #列表ress转换回元组res
        # 方法一：studcur.execute(sql,(res[0],res[1],res[2],res[3],Xh))
        # 或方法二：以下三句
        ress.append(Xh)
        res = tuple(ress)  # 列表ress转换回元组res
        studcur.execute(sql, res)
    procinit1()  # 清空文本框
    studdb.commit()  # ()
    studdb.close();  # 关闭数据库连接


def proc4():  # '查询记录'按钮关联的事件程序
    studdb = sqlite3.connect("student.db")  # 定义/打开数据库student.db，建立数据库连接对象studdb
    studcur = studdb.cursor()  # 创建一个游标对象studcur
    Xh = entryXh.get()
    Xh = Xh.strip()  # strip()方法删除Xh两边空格
    sql = "select * from stud where 学号=?"
    studcur.execute(sql, (Xh,))
    # res=studcur.fetchone()     #res是元组
    res = studcur.fetchall()  # res是元组构成的列表
    if len(res) != 0:
        procinit1()  # 清空文本框
        entryXh.insert(0, res[0][0])
        entryXm.insert(0, res[0][1])
        entryXb.insert(0, res[0][2])
        entrySy.insert(0, res[0][3])
    else:
        procinit1()  # 清空文本框
        entryXh.insert(0, Xh + " 查无此人!")
    studdb.commit()  # ()
    studdb.close();  # 关闭数据库连接


def proc5():  # '生源统计'按钮关联的事件程序
    studdb = sqlite3.connect("student.db")  # 定义/打开数据库student.db，建立数据库连接对象studdb
    studcur = studdb.cursor()  # 创建一个游标对象studcur
    Sf = entrySrsf.get()
    Sf.strip()  # strip()方法删除Sf两边空格
    sql = "select count(*) from stud where substr(生源,1,length(?))=?"
    studcur.execute(sql, (Sf, Sf))
    res = studcur.fetchall()  # res是元组构成的列表
    entrySytj.delete(0, 'end')
    entrySytj.insert(0, Sf + "有" + str(res[0][0]) + "人")
    studdb.commit()  # ()
    studdb.close();  # 关闭数据库连接


def proc6():  # '性别统计'按钮关联的事件程序
    studdb = sqlite3.connect("student.db")  # 定义/打开数据库student.db，建立数据库连接对象studdb
    studcur = studdb.cursor()  # 创建一个游标对象studcur
    Xb = entrySrxb.get()
    Xb.strip()  # strip()方法删除Xb两边空格
    sql = "select count(*) from stud where substr(性别,1,length(?))=?"
    studcur.execute(sql, (Xb, Xb))
    res = studcur.fetchall()  # res是元组构成的列表
    entryXbtj.delete(0, 'end')
    entryXbtj.insert(0, "性别：" + Xb + "：有" + str(res[0][0]) + "人")
    studdb.commit()  # ()
    studdb.close();  # 关闭数据库连接


def proc7():  # '姓氏统计'按钮关联的事件程序
    studdb = sqlite3.connect("student.db")  # 定义/打开数据库student.db，建立数据库连接对象studdb
    studcur = studdb.cursor()  # 创建一个游标对象studcur
    Xs = entrySrxs.get()
    Xs.strip()  # strip()方法删除Xb两边空格
    sql = "select count(*) from stud where substr(姓名,1,length(?))=?"
    studcur.execute(sql, (Xs, Xs))
    res = studcur.fetchall()  # res是元组构成的列表
    entryXstj.delete(0, 'end')
    entryXstj.insert(0, "姓氏：" + Xs + "：有" + str(res[0][0]) + "人")
    studdb.commit()
    studdb.close();  # 关闭数据库连接


def proc8():  # '清空文本框'按钮关联的事件程序
    procinit1()  # 清空文本框内容

def proc_load():  # 清空文本框内容
    entryXh.delete(0, 'end')
    entryZybh.delete(0, 'end')
    entryBjh.delete(0, 'end')
    entryCj.delete(0, 'end')
    entryTip.delete(0, 'end')
    entryTip.insert(0,"正在查询作业成绩单汇总情况，请稍等!")



def proc_clear():  # 清空文本框内容
    entryXh.delete(0, 'end')
    entryZybh.delete(0, 'end')
    entryBjh.delete(0, 'end')
    entryCj.delete(0, 'end')


def proc_select():
    print("select clicked.")
    try:
        studdb = sqlite3.connect("test.db")  # 定义/打开数据库student.db，建立数据库连接对象studdb
        studcur = studdb.cursor()  # 创建一个游标对象studcur
        print("database is ok.")
        Xh = entryXh.get()
        print(Xh)
        Zybh = entryZybh.get()


        sql = "select 班级号,学生号,作业编号,提交时间,成绩 from 学生作业表 where 学生号=? and 作业编号=?"
        studcur.execute(sql, (Xh, Zybh))  # 执行插入命令

        res = studcur.fetchall()  # res是元组构成的列表
        if len(res) != 0:
            root.update()
            proc_clear()  # 清空文本框
            entryBjh.insert(0, res[0][0])
            entryXh.insert(0, res[0][1])
            entryZybh.insert(0, res[0][2])
            entryTime.insert(0, res[0][3])
            entryCj.insert(0, res[0][4])
        else:
            root.update()
            proc_clear()  # 清空文本框
            entryXh.insert(0, Xh + " 查无此人!")

        studdb.commit()
    except Exception as err:
        print('Query Failed: %s\nError: %s' % (query, str(err)))
        tkm.showinfo('新增记录失败: %s\nError: %s' % (query, str(err)))
    finally:
        studdb.close();  # 关闭数据库连接

def proc_add():
    print("add new record.")
    try:
        studdb = sqlite3.connect("test.db")  # 定义/打开数据库student.db，建立数据库连接对象studdb
        studcur = studdb.cursor()  # 创建一个游标对象studcur
        print("database is ok.")
        Xh = entryXh.get()
        print(Xh)
        Zybh = entryZybh.get()
        Bjh = entryBjh.get()
        Cj = entryCj.get()
        timestr = int(time.time())
        sql = "Insert into 学生作业表 values (?,?,?,?,?)"
        studcur.execute(sql, (Bjh, Xh, Zybh, timestr, Cj))  # 执行插入命令
        tkm.showinfo('新增记录成功。')
        root.update()
        proc_clear()  # 清空文本框
        studdb.commit()
    except Exception as err:
        print('Query Failed: %s\nError: %s' % (query, str(err)))
        tkm.showinfo('新增记录失败: %s\nError: %s' % (query, str(err)))
    finally:
        studdb.close();  # 关闭数据库连接


def proc_pie_report( ):
    print("select clicked.")
    try:
        studdb = sqlite3.connect("test.db")  # 定义/打开数据库student.db，建立数据库连接对象studdb
        studcur = studdb.cursor()  # 创建一个游标对象studcur
        print("database is ok.")
        Xh = entryXh.get()
        print(Xh)
        Zybh = entryZybh.get()


        sql = "select 班级号,学生号,作业编号,提交时间,成绩 from 学生作业表 where 学生号=? and 作业编号=?"
        studcur.execute(sql, (Xh, Zybh))  # 执行插入命令

        res = studcur.fetchall()  # res是元组构成的列表
        if len(res) != 0:
            root.update()
            proc_clear()  # 清空文本框
            entryBjh.insert(0, res[0][0])
            entryXh.insert(0, res[0][1])
            entryZybh.insert(0, res[0][2])
            entryTime.insert(0, res[0][3])
            entryCj.insert(0, res[0][4])
        else:
            root.update()
            proc_clear()  # 清空文本框
            entryXh.insert(0, Xh + " 查无此人!")

        studdb.commit()
    except Exception as err:
        print('Query Failed: %s\nError: %s' % (query, str(err)))
        tkm.showinfo('新增记录失败: %s\nError: %s' % (query, str(err)))
    finally:
        studdb.close();  # 关闭数据库连接

def proc_pie_report2( ):
    print("select clicked.")
    try:
        studdb = sqlite3.connect("test.db")  # 定义/打开数据库student.db，建立数据库连接对象studdb
        studcur = studdb.cursor()  # 创建一个游标对象studcur
        print("database is ok.")
        Xh = entryXh.get()
        print(Xh)
        Zybh = entryZybh.get()

        sql = "SELECT  CASE WHEN 1 < 2 THEN \"True\" ELSE \"False\" END "
        sql = "select  班级号, 作业编号,iif(成绩=100,1,0) as s1,iif(成绩<100 and 成绩 >= 80,1,0) as s2 from  学生作业表"
        studcur.execute(sql)  # 执行插入命令

        res = studcur.fetchall()  # res是元组构成的列表
        if len(res) != 0:
            print("test " + str(res[0][0]))
        else:
            print("test failure " + str(res[0][0]))

        studdb.commit()
    except Exception as err:
        print('Query Failed: %s\nError: %s' % (query, str(err)))
        tkm.showinfo('新增记录失败: %s\nError: %s' % (query, str(err)))
    finally:
        studdb.close();  # 关闭数据库连接

def proc_pie_report3( ):
    print("select clicked.")

    try:
        studdb = sqlite3.connect("test.db")  # 定义/打开数据库student.db，建立数据库连接对象studdb
        studcur = studdb.cursor()  # 创建一个游标对象studcur
        print("database is ok.")
        Xh = entryXh.get()
        print(Xh)


        sql = "SELECT  * from vv1 where 班级号=? and 作业编号=?"

        Zybh = entryZybh.get()

        Bjh = entryBjh.get()

        studcur.execute(sql,(Bjh,Zybh))  # 执行插入命令

        res = studcur.fetchall()  # res是元组构成的列表
        values = []
        title = "";
        if len(res) != 0:
            print("test " + str(res[0][0]))
            title =str(res[0][0]) + "-" + str(res[0][1])
            values.append(res[0][2])
            values.append(res[0][3])
            values.append(res[0][4])
            values.append(res[0][5])
        else:
            print("test failure " + str(res[0][0]))

        studdb.commit()

        labels = ['<60', '60-80', '80-100', '100']

        # 显示百分比
        # textprops={'fontsize':18,'color':'k'} 设置为字体大小为18，颜色黑色
        plt.pie(values, labels=labels, autopct='%3.2f%%', textprops={'fontsize': 18, 'color': 'k'})
        # 设置x,y的刻度一样，使其饼图为正圆
        plt.axis('equal')
        plt.title = title

        plt.show()

    except Exception as err:
        print('Query Failed: %s\nError: %s' % (query, str(err)))
        tkm.showinfo('新增记录失败: %s\nError: %s' % (query, str(err)))
    finally:
        studdb.close();  # 关闭数据库连接








# 定义窗体/窗口
root = tk.Tk()
root.geometry('800x600')  # 窗口大小
root.title('20200610-作业成绩数据管理')  # 窗口标题
# 建立各行的控件，用于输入、输出或功能选择



lblXh = tk.Label(root, text='学号：')  # 建立标签Label控件
lblXh.grid(row=0, column=0)  # 控件在窗体上的位置：0行0列


entryXh = tk.Entry(root)  # 建立单行文本框控件
entryXh.grid(row=0, column=1)  # 控件在窗体上的位置：0行3列

lblZybh = tk.Label(root, text='作业编号:')  # 建立标签Label控件
lblZybh.grid(row=0, column=2)  # 控件在窗体上的位置：0行0列

v_zybh = tk.StringVar(value='202001')

entryZybh = tk.Entry(root, textvariable=v_zybh)  # 建立单行文本框控件
entryZybh.grid(row=0, column=3)  # 控件在窗体上的位置：0行1列


btnSelect = tk.Button(root, text='查询', command=proc_select)
btnSelect.grid(row=0, column=5)  # 控件在窗体上的位置：0行2列




lblTip = tk.Label(root, text='')  # 建立标签Label控件
lblTip.grid(row=1, column=0)  # 控件在窗体上的位置：0行0列

inittext = tk.StringVar(value='正在初始化')
entryTip = tk.Entry(root, textvariable=inittext, state='disabled')

entryTip.grid(row=1, column=2)  # 控件在窗体上的位置：0行0列



lblTime = tk.Label(root, text='时间：')
lblTime.grid(row=2, column=0)
currdate = tk.StringVar(value='2020-06-10')
entryTime = tk.Entry(root, textvariable=currdate, state='disabled')

entryTime.grid(row=2, column=1)



lblBjh = tk.Label(root, text='班级号:')  # 建立标签Label控件
lblBjh.grid(row=3, column=0)  # 控件在窗体上的位置：0行0列
v_bjh = tk.StringVar(value='101')
entryBjh = tk.Entry(root, textvariable=v_bjh)  # 建立单行文本框控件
entryBjh.grid(row=3, column=1)  # 控件在窗体上的位置：0行1列




lblCj = tk.Label(root, text='成绩：')
lblCj.grid(row=3, column=2)
entryCj = tk.Entry(root)
entryCj.grid(row=3, column=3)

btnAdd = tk.Button(root, text='保存', command=proc_add)
btnAdd.grid(row=3, column=5)  # 控件在窗体上的位置：0行2列


lblTip2 = tk.Label(root, text='')  # 建立标签Label控件
lblTip2.grid(row=4, column=0)  # 控件在窗体上的位置：0行0列


btnCancel = tk.Button(root, text='班级作业成绩占比分布图', command=proc_pie_report3)
btnCancel.grid(row=5, column=1)  # 控件在窗体上的位置：2行2列
#btnOk = tk.Button(root, text='报表2', command=proc_pie_report2)
#btnOk.grid(row=5, column=2)  # 控件在窗体上的位置：2行3列
#btnOk = tk.Button(root, text='', command=proc_pie_report1)
#btnOk.grid(row=5, column=3)  # 控件在窗体上的位置：2行3列

#proc_load()



# 进入主事件循环
root.mainloop()
