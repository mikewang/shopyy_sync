from PyQt5 import QtWidgets
import sys
import pymysql
import pandas as pd
from PyQt5.QtWidgets import QMainWindow, QDialog, QLabel, QPushButton
from PyQt5.QtCore import Qt, QRect, QDateTime, QDate, QAbstractTableModel
from login import Ui_LoginWindow
from schedule_form import Ui_MainWindow as ScheduleWindow
from order_form import Ui_MainWindow as OrderWindow
from report_form import Ui_MainWindow as ReportWindow
from setting_form import Ui_MainWindow as SettingWindow
from dialog_form import Ui_Dialog as Dialog


uid = ''
uname = ''
jobs = ''
db_ip = '192.168.0.103'
db_user = 'wfg'
db_password = 'wfg025+'
db_db = 'stdb'
db_port = 3306


def showDialog(message):
    dialog = QDialog()
    (x, y, w, h) = main.geometry().getRect()
    (px, py) = (x + w/2.0, y + h/2.0)
    w = w * 0.7
    h = h * 0.5
    x = px - w/2.0
    y = py - h/2.0
    dialog.setGeometry(QRect(x, y, w*0.7, h*0.3))
    dialog.setWindowModality(Qt.ApplicationModal)
    dialog.setWindowTitle("提示")
    label = QLabel(message, dialog)
    label.move(10, 10)
    label.setText(message)
    btn = QPushButton("OK", dialog)
    btn.clicked.connect(dialog.close)
    btn.move(10, 50)
    dialog.exec_()


class TableModel(QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def selectedRows(self, index):
        row = self._data.iloc[index.row()]
        return row

    def selectedRowID(self, index):
        rowid = self._data.iloc[index.row(), 0]
        return rowid

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])
            if orientation == Qt.Vertical:
                return str(self._data.index[section])


class ScheduleMainWindow(ScheduleWindow):
    # def __init__(self, parent=None):
    #     super(ScheduleMainWindow, self).__init__(parent)
    #     # self.setupUi(self)
    #     # # #添加登录按钮信号和槽。注意display函数不加小括号()
    #     # # self.login_Button.clicked.connect(self.display)
    #     # # #添加退出按钮信号和槽。调用close函数
    #     # # self.cancel_Button.clicked.connect(self.close)

    def display(self):
        pass
        # #利用line Edit控件对象text()函数获取界面输入
        # username = self.user_lineEdit.text()
        # password = self.pwd_lineEdit.text()
        # #利用text Browser控件对象setText()函数设置界面显示
        # self.user_textBrowser.setText("登录成功!\n" + "用户名是: "+ username+ ",密码是： "+ password)

    def reset(self):
        self.input_schedule_date.setDateTime(QDateTime.currentDateTime())
        self.label_schedule_created.setText((QDateTime.currentDateTime()).toString("yyyy-MM-dd hh:mm:ss"))
        self.input_schedule_day_select.setDate(QDate.currentDate())
        self.input_schedule_day_table.setDate(QDate.currentDate())
        self.input_combox_schedule_type.setCurrentText(self.input_combox_schedule_type.itemText(2))
        self.input_customer.setText("")
        self.input_combox_customer_type.setCurrentText((self.input_combox_customer_type.itemText(1)))
        self.input_customer_tel.setText("")
        self.input_schedule_table_no.setText("")
        self.input_customer_num.setText("1")
        self.input_note.setText("")

    def save(self):
        try:
            print("insert schedule")
            conn_mysql = pymysql.connect(host=db_ip, user=db_user, passwd=db_password, db=db_db, port=db_port)
            cursor = conn_mysql.cursor()
            schedule_date = self.input_schedule_date.text()
            customer = self.input_customer.text()
            customer_type = self.input_combox_customer_type.currentText()
            customer_tel = self.input_customer_tel.text()
            schedule_table_no = self.input_schedule_table_no.text()
            customer_num = int(self.input_customer_num.text())
            note = self.input_note.toPlainText()
            sql = "insert into t_schedule_info" \
                  "(schedule_date, customer, customer_type, customer_tel, schedule_table_no, customer_num, note, created)" \
                  " values(%s,%s,%s,%s,%s,%s,%s,now())"
            row = cursor.execute(sql, (schedule_date, customer, customer_type, customer_tel, schedule_table_no, customer_num, note))
            conn_mysql.commit()
            rowid = cursor.lastrowid
            # 订单编号
            print("预定ID编号", rowid)
            order_no = self.input_schedule_date.text().split(" ")[0].replace("-", "") + "" + str(rowid).zfill(3)
            sql = "update t_schedule_info set order_no=%s where id = %s"
            cursor.execute(sql, (order_no, rowid))
            conn_mysql.commit()
            cursor.close()
            conn_mysql.close()
        except Exception as e:
            print(e)

    def selectSchedule(self):
        try:
            print("select schedule")
            conn_mysql = pymysql.connect(host=db_ip, user=db_user, passwd=db_password, db=db_db, port=db_port)
            cursor = conn_mysql.cursor()
            schedule_date = self.input_schedule_day_select.text()
            customer = self.input_customer_select.text()
            customer_tel = self.input_customer_tel_select.text()
            print(schedule_date,customer, customer_tel)
            sql = "select id, order_no, date_format(schedule_date,'%%Y-%%m-%%d %%H:%%i:%%S') as schedule_date, " \
                  "customer, customer_type, customer_tel, schedule_table_no, customer_num, note, " \
                  "date_format(created,'%%Y-%%m-%%d %%H:%%i:%%S') as  created from t_schedule_info " \
                  " where schedule_date between %s and %s and customer like %s and customer_tel like %s"
            cursor.execute(sql, (schedule_date + " 00:00:00", schedule_date + " 23:59:59", '%' + customer + '%', '%' + customer_tel + '%'))
            rows = cursor.fetchall()
            for row in rows:
                print(row)
            print("查询结果", rows)
            # print(sql)
            srs = []
            columns = ["订单号", "桌台号", "客户", "联系电话"]
            indexes = []
            for row in rows:
                sr = [row[1], row[6], row[3], row[5]]
                srs.append(sr)
                indexes.append(str(len(srs)))
            data = pd.DataFrame(srs, columns=columns, index=indexes)
            model = TableModel(data)
            self.table_schedule_select.setModel(model)
            self.table_schedule_select.update()
            cursor.close()
            conn_mysql.commit()
            conn_mysql.close()
        except Exception as e:
            print(e)

    def selectScheduleTable(self):
        try:
            print("select schedule table")
            conn_mysql = pymysql.connect(host=db_ip, user=db_user, passwd=db_password, db=db_db, port=db_port)
            cursor = conn_mysql.cursor()
            schedule_date = self.input_schedule_day_table.text()
            schedule_type = self.input_combox_schedule_type_table.currentText()
            if schedule_type == "早餐":
                b_time = "06:00:00"
                e_time = "09:00:00"
            elif schedule_type == "中餐":
                b_time = "11:00:00"
                e_time = "15:00:00"
            else:
                b_time = "15:00:00"
                e_time = "23:59:59"
            sql = "select a.table_no,a.spec,a.location,IFNULL(b.customer,'可用') as status " \
                  " from t_table_info a left join (select * from t_schedule_info where schedule_date BETWEEN %s and %s) b " \
                  "on a.table_no=b.schedule_table_no order by a.table_no"
            cursor.execute(sql, (schedule_date + " " + b_time, schedule_date + " " + e_time))
            rows = cursor.fetchall()
            # print(sql)
            srs = []
            columns = ["桌台号", "规格", "位置", "状态"]
            indexes = []
            for row in rows:
                sr = [row[0], row[1], row[2], row[3]]
                srs.append(sr)
                indexes.append(str(len(srs)))
            data = pd.DataFrame(srs, columns=columns, index=indexes)
            model = TableModel(data)
            self.table_select_table.setModel(model)
            self.table_select_table.update()
            cursor.close()
            conn_mysql.commit()
            conn_mysql.close()
        except Exception as e:
            print(e)


    def showWidget(self, name):
        self.widget_schedule.hide()
        self.widget_table.hide()
        self.widget_table.setGeometry(self.widget_schedule.geometry())
        self.reset()
        self.btn_schedule_reset.clicked.connect(self.reset)
        self.btn_schedule_ok.clicked.connect(self.save)
        self.btn_schedule_select.clicked.connect(self.selectSchedule)
        self.btn_select_table.clicked.connect(self.selectScheduleTable)

        if name == self.actionSchedule.objectName():
            self.widget_schedule.show()
        elif name == self.actionTable.objectName():
            self.widget_table.show()
        else:
            self.widget_schedule.show()


class OrderMainWindow(OrderWindow):
    foods_selected = []

    def showWidget(self, name):
        self.widget_order_new.hide()
        self.widget_order_list.hide()
        self.widget_order_list.setGeometry(self.widget_order_new.geometry())
        self.btn_order_check.clicked.connect(self.orderCheck)
        self.btn_food_query.clicked.connect(self.orderFoodQuery)
        self.btn_food_check.clicked.connect(self.orderFoodCheck)
        self.btn_order_query_account.clicked.connect(self.orderQueryAccount)
        self.btn_order_save_account.clicked.connect(self.orderSaveAccount)
        self.input_order_clicked.setDateTime(QDateTime.currentDateTime())
        self.btn_order_save_account.setEnabled(False)
        if name == self.actionOrderNew.objectName():
            self.widget_order_new.show()
        elif name == self.actionOrderList.objectName():
            self.widget_order_list.show()
        else:
            self.widget_order_new.show()

    def orderCheck(self):
        try:
            print("select order  info and order food list ")
            self.input_order_clicked.setDateTime(QDateTime.currentDateTime())
            conn_mysql = pymysql.connect(host=db_ip, user=db_user, passwd=db_password, db=db_db, port=db_port)
            cursor = conn_mysql.cursor()
            order_no = self.input_order_no.text()
            sql = "select  order_no, customer, schedule_table_no from t_schedule_info where order_no = %s"
            cursor.execute(sql, (order_no))
            row = cursor.fetchone()
            if row is None:
                showDialog("没有这笔订单，请核实")
                self.checkBox_order_checked.setChecked(False)
            else:
                showDialog("读取订单详情")
                self.checkBox_order_checked.setChecked(True)
                self.input_customer.setText(row[1])
                self.input_table_no.setText(row[2])
            sql = "select b.`name`,b.price,a.food_num from t_order_detail a join t_food_info b " \
                  "on a.food_no=b.food_no where a.order_no = %s"
            cursor.execute(sql, (order_no))
            rows = cursor.fetchall()
            print(rows)
            srs = []
            columns = ["菜名", "价格", "数量"]
            indexes = []
            for row in rows:
                sr = [row[0], row[1], row[2]]
                srs.append(sr)
                indexes.append(str(len(srs)))
            data = pd.DataFrame(srs, columns=columns, index=indexes)
            model = TableModel(data)
            self.table_order_food_list.setModel(model)
            self.table_order_food_list.update()
            cursor.close()
            conn_mysql.commit()
            conn_mysql.close()
        except Exception as e:
            print(e)

    def orderSave(self):
        pass

    def orderFoodQuery(self):
        try:
            print("select food list ")
            self.input_order_clicked.setDateTime(QDateTime.currentDateTime())
            conn_mysql = pymysql.connect(host=db_ip, user=db_user, passwd=db_password, db=db_db, port=db_port)
            cursor = conn_mysql.cursor()
            food_name = self.input_food_name.text()
            sql = "select food_no, name,category,price from t_food_info where name like %s"
            cursor.execute(sql, ('%' + food_name + '%'))
            rows = cursor.fetchall()
            print(rows)
            srs = []
            columns = ["编号", "菜名", "类别", "价格"]
            indexes = []
            for row in rows:
                sr = [row[0], row[1], row[2], row[3]]
                srs.append(sr)
                indexes.append(str(len(srs)))
            data = pd.DataFrame(srs, columns=columns, index=indexes)
            model = TableModel(data)
            self.table_food_query.setModel(model)
            self.table_food_query.update()
            cursor.close()
            conn_mysql.commit()
            conn_mysql.close()
        except Exception as e:
            print(e)

    def orderFoodCheck(self):
        try:
            order_no = self.input_order_no.text()
            index = self.table_food_query.selectedIndexes()[0]
            row = self.table_food_query.model().selectedRows(index)
            order_checked = self.checkBox_order_checked.isChecked()
            if row is not None and order_checked == True:
                food_name = row[1]
                food_no = row[0]
                showDialog("菜:" + food_name + " 选中")
                conn_mysql = pymysql.connect(host=db_ip, user=db_user, passwd=db_password, db=db_db, port=db_port)
                cursor = conn_mysql.cursor()
                sql = "select * from t_order_info where order_no=%s"
                cursor.execute(sql, (order_no))
                row = cursor.fetchone()
                if row is None:
                    sql = "insert into t_order_info(order_no,userid,customer,table_no,account_date) " \
                          "values(%s,%s,%s,%s,now())"
                    cursor.execute(sql, (order_no, uid, self.input_customer.text(),self.input_table_no.text()))
                sql = "insert into t_order_detail(order_no,food_no,food_num) values(%s,%s,1)"
                cursor.execute(sql, (order_no, food_no))
                cursor.close()
                conn_mysql.commit()
                conn_mysql.close()
        except Exception as e:
            print(e)

    def orderQueryAccount(self):
        try:
            conn_mysql = pymysql.connect(host=db_ip, user=db_user, passwd=db_password, db=db_db, port=db_port)
            cursor = conn_mysql.cursor()
            order_no = self.input_order_no_account.text()
            sql = "select  order_no, customer, schedule_table_no from t_schedule_info where order_no = %s"
            cursor.execute(sql, (order_no))
            row = cursor.fetchone()
            if row is None:
                showDialog("没有这笔订单，请核实")
                self.btn_order_save_account.setEnabled(False)
            else:
                showDialog("读取订单详情")
                self.btn_order_save_account.setEnabled(True)
                self.input_table_no_account.setText(row[2])
            sql = "select b.`name`,b.price,sum(a.food_num) as food_nums, b.price*sum(a.food_num) as total_nums " \
                  " from t_order_detail a join t_food_info b " \
                  "on a.food_no=b.food_no where a.order_no = %s group by b.`name`,b.price"
            cursor.execute(sql, (order_no))
            rows = cursor.fetchall()
            print(rows)
            srs = []
            columns = ["菜名",  "价格", "数量", "总价"]
            indexes = []
            for row in rows:
                sr = [row[0], row[1], row[2], row[3]]
                srs.append(sr)
                indexes.append(str(len(srs)))
            data = pd.DataFrame(srs, columns=columns, index=indexes)
            model = TableModel(data)
            self.table_order_food_list_account.setModel(model)
            self.table_order_food_list_account.update()
            sql = "select sum(a.food_num*b.price) as should_money from t_order_detail a join t_food_info b " \
                  "on a.food_no=b.food_no where a.order_no = %s"
            cursor.execute(sql, (order_no))
            row = cursor.fetchone()
            if row is not None:
                self.input_should_money_account.setText(str(row[0]))
            cursor.close()
            conn_mysql.commit()
            conn_mysql.close()
        except Exception as e:
            print(e)

    def orderSaveAccount(self):
        try:
            stt = (QDateTime.currentDateTime()).toString("hhmmss")
            order_no = self.input_order_no_account.text()
            should_money = self.input_should_money_account.text()
            real_money = self.input_real_money_account.text()
            money_type = self.input_combox_money_type_account.currentText()
            account_no = order_no + stt
            conn_mysql = pymysql.connect(host=db_ip, user=db_user, passwd=db_password, db=db_db, port=db_port)
            cursor = conn_mysql.cursor()
            sql = "insert into t_account_info(account_no,should_money,real_money,money_type,created) " \
                  "values(%s, %s, %s, %s, now())"
            cursor.execute(sql, (account_no, should_money, real_money, money_type))
            sql = "insert into t_order_account(order_no,account_no,account_time) values(%s,%s,now())"
            cursor.execute(sql, (order_no, account_no))
            cursor.close()
            conn_mysql.commit()
            conn_mysql.close()
            self.btn_order_save_account.setEnabled(False)
            showDialog("结算成功，支付完成")
        except Exception as e:
            print(e)

class ReportMainWindow(ReportWindow):
    def showWidget(self, name):
        self.widget_report_query.hide()
        self.widget_report_month.hide()
        self.widget_report_month.setGeometry(self.widget_report_query.geometry())
        self.input_begin_date.setDateTime(QDateTime.currentDateTime())
        self.input_end_date.setDateTime(QDateTime.currentDateTime())
        self.input_month.setDateTime(QDateTime.currentDateTime())
        self.btn_order_query.clicked.connect(self.orderQuery)
        self.btn_order_report.clicked.connect(self.orderReport)

        if name == self.actionOrderQuery.objectName():
            self.widget_report_query.show()
        elif name == self.actionAccountReport.objectName():
            self.widget_report_month.show()
        else:
            self.widget_report_query.show()

    def orderQuery(self):
        try:
            conn_mysql = pymysql.connect(host=db_ip, user=db_user, passwd=db_password, db=db_db, port=db_port)
            cursor = conn_mysql.cursor()
            order_no = self.input_order_no.text()
            if len(order_no) > 0:
                sql = "select DATE_FORMAT(a.account_date,'%%Y-%%m-%%d') as dayid, a.order_no,c.`name`,b.food_num " \
                      "from t_order_info a JOIN t_order_detail b on a.order_no = b.order_no join t_food_info c " \
                      "on b.food_no = c.food_no where a.order_no=%s"
                cursor.execute(sql, (order_no))
                rows = cursor.fetchall()
                print(rows)
                srs = []
                columns = ["日期", "订单号", "菜", "数量"]
                indexes = []
                for row in rows:
                    sr = [row[0], row[1], row[2], row[3]]
                    srs.append(sr)
                    indexes.append(str(len(srs)))
                data = pd.DataFrame(srs, columns=columns, index=indexes)
                model = TableModel(data)
                self.table_order_query.setModel(model)
                self.table_order_query.update()
                cursor.close()
            else:
                begin_date = self.input_begin_date.text()
                end_date = self.input_end_date.text()
                sql = "select DATE_FORMAT(a.account_date,'%%Y-%%m-%%d') as dayid, a.order_no,c.`name`,b.food_num " \
                      "from t_order_info a JOIN t_order_detail b on a.order_no = b.order_no join t_food_info c " \
                      "on b.food_no = c.food_no where a.account_date BETWEEN %s and %s"
                cursor.execute(sql, (begin_date, end_date))
                rows = cursor.fetchall()
                print(rows)
                srs = []
                columns = ["日期", "订单号", "菜", "数量"]
                indexes = []
                for row in rows:
                    sr = [row[0], row[1], row[2], row[3]]
                    srs.append(sr)
                    indexes.append(str(len(srs)))
                data = pd.DataFrame(srs, columns=columns, index=indexes)
                model = TableModel(data)
                self.table_order_query.setModel(model)
                self.table_order_query.update()
                cursor.close()

            conn_mysql.commit()
            conn_mysql.close()
        except Exception as e:
            print(e)

    def orderReport(self):
        try:
            conn_mysql = pymysql.connect(host=db_ip, user=db_user, passwd=db_password, db=db_db, port=db_port)
            cursor = conn_mysql.cursor()
            input_month = self.input_month.text()
            begin_date = QDateTime.fromString(input_month, "yyyy-MM").toString("yyyy-MM-dd hh:mm:ss")
            end_date = QDateTime.fromString(input_month, "yyyy-MM").addMonths(1).toString("yyyy-MM-dd hh:mm:ss")
            sql = "select DATE_FORMAT(a.account_date,'%%Y-%%m-%%d') as dayid, c.`name`,sum(b.food_num) as nums " \
                  "from t_order_info a JOIN t_order_detail b on a.order_no = b.order_no join t_food_info c " \
                  "on b.food_no = c.food_no where a.account_date BETWEEN %s and %s " \
                  "group by DATE_FORMAT(a.account_date,'%%Y-%%m-%%d'),c.`name` " \
                  "order by DATE_FORMAT(a.account_date,'%%Y-%%m-%%d') "
            cursor.execute(sql, (begin_date, end_date))
            rows = cursor.fetchall()
            print(rows)
            srs = []
            columns = ["日期", "菜", "数量"]
            indexes = []
            for row in rows:
                sr = [row[0], row[1], row[2]]
                srs.append(sr)
                indexes.append(str(len(srs)))
            data = pd.DataFrame(srs, columns=columns, index=indexes)
            model = TableModel(data)
            self.table_order_report.setModel(model)
            self.table_order_report.update()
            cursor.close()

            conn_mysql.commit()
            conn_mysql.close()
        except Exception as e:
            print(e)

class SettingMainWindow(SettingWindow):
    def showWidget(self, name):
        self.widget_user_list.hide()
        self.widget_table_list.hide()
        self.widget_food_list.hide()
        self.widget_table_list.setGeometry(self.widget_user_list.geometry())
        self.widget_food_list.setGeometry(self.widget_user_list.geometry())
        if name == self.actionUserList.objectName():
            self.widget_user_list.show()
        elif name == self.actionTableList.objectName():
            self.widget_table_list.show()
        elif name == self.actionFoodList.objectName():
            self.widget_food_list.show()
        else:
            self.widget_user_list.show()


def login(login_ui):
    try:
        global uid
        uid = login_ui.input_uid.text().rstrip().lstrip()
        passwd = login_ui.input_passwd.text().rstrip().lstrip()
        if uid == '' or passwd == '':
            showDialog("用户名或密码为空")
        else:
            conn_mysql = pymysql.connect(host=db_ip, user=db_user, passwd=db_password, db=db_db, port=db_port)
            cursor = conn_mysql.cursor()
            cursor.execute("select name,jobs from t_user where uid = %s and passwd = %s limit 1", (uid, passwd))
            row = cursor.fetchone()
            print(row)
            if row is None:
                showDialog("用户不存在或者密码不正确")
            else:
                global uname
                uname = row[0]
                global jobs
                jobs = row[1]
                schedule_window(None)
                # # 初始化
                # main.destroy()
                # myWin = ScheduleWindow()
                # myWin.setWindowTitle("工号：" + uid + " 姓名：" + uname)
                # # 将窗口控件显示在屏幕上
                # myWin.show()
                # # 程序运行，sys.exit方法确保程序完整退出。
    except Exception as e:
        print(e)


def schedule_window(name):
    try:
        global uid
        global uname
        global jobs
        print("schedule", uid, uname)
        ui = ScheduleMainWindow()
        ui.setupUi(main)
        if name is None:
            if jobs != "admin" and jobs != "leader":
                ui.menu_5.setEnabled(False)
                ui.menu_4.setEnabled(False)

        ui.showWidget(name)
        # 1
        ui.actionSchedule.triggered.connect(lambda: ui.showWidget(ui.actionSchedule.objectName()))
        ui.actionTable.triggered.connect(lambda: ui.showWidget(ui.actionTable.objectName()))
        # 2
        ui.actionOrderNew.triggered.connect(lambda: order_window(ui.actionOrderNew.objectName()))
        ui.actionOrderList.triggered.connect(lambda: order_window(ui.actionOrderList.objectName()))
        # 3
        ui.actionOrderQuery.triggered.connect(lambda: report_window(ui.actionOrderQuery.objectName()))
        ui.actionAccountReport.triggered.connect(lambda: report_window(ui.actionAccountReport.objectName()))
        # 4
        ui.actionUserList.triggered.connect(lambda: report_window(ui.actionUserList.objectName()))
        ui.actionTableList.triggered.connect(lambda: report_window(ui.actionTableList.objectName()))
        ui.actionFoodList.triggered.connect(lambda: report_window(ui.actionFoodList.objectName()))

        main.setGeometry(QRect(100, 100, 480, 700))
        main.show()
        main.setWindowTitle("工号：" + uid + " 姓名：" + uname)
    except Exception as e:
        print(e)


def order_window(name):
    try:
        global uid
        ui = OrderMainWindow()
        ui.setupUi(main)
        ui.showWidget(name)
        # 1
        ui.actionSchedule.triggered.connect(lambda: schedule_window(ui.actionSchedule.objectName()))
        ui.actionTable.triggered.connect(lambda: schedule_window(ui.actionTable.objectName()))
        # 2
        ui.actionOrderNew.triggered.connect(lambda: ui.showWidget(ui.actionOrderNew.objectName()))
        ui.actionOrderList.triggered.connect(lambda: ui.showWidget(ui.actionOrderList.objectName()))
        # 3
        ui.actionOrderQuery.triggered.connect(lambda: report_window(ui.actionOrderQuery.objectName()))
        ui.actionAccountReport.triggered.connect(lambda: report_window(ui.actionAccountReport.objectName()))
        # 4
        ui.actionUserList.triggered.connect(lambda: setting_window(ui.actionUserList.objectName()))
        ui.actionTableList.triggered.connect(lambda: setting_window(ui.actionTableList.objectName()))
        ui.actionFoodList.triggered.connect(lambda: setting_window(ui.actionFoodList.objectName()))

        main.setGeometry(QRect(100, 100, 480, 700))
        main.show()
        main.setWindowTitle("工号：" + uid + " 姓名：" + uname)
    except Exception as e:
        print(e)


def report_window(name):
    try:
        global uid
        ui = ReportMainWindow()
        ui.setupUi(main)
        ui.showWidget(name)
        ui.actionOrderNew.triggered.connect(lambda: ui.showWidget(ui.actionOrderNew.objectName()))
        ui.actionOrderList.triggered.connect(lambda: ui.showWidget(ui.actionOrderList.objectName()))
        # 1
        ui.actionSchedule.triggered.connect(lambda: schedule_window(ui.actionSchedule.objectName()))
        ui.actionTable.triggered.connect(lambda: schedule_window(ui.actionTable.objectName()))
        # 2
        ui.actionOrderNew.triggered.connect(lambda: order_window(ui.actionOrderNew.objectName()))
        ui.actionOrderList.triggered.connect(lambda: order_window(ui.actionOrderList.objectName()))
        # 3
        ui.actionOrderQuery.triggered.connect(lambda: ui.showWidget(ui.actionOrderQuery.objectName()))
        ui.actionAccountReport.triggered.connect(lambda: ui.showWidget(ui.actionAccountReport.objectName()))
        # 4
        ui.actionUserList.triggered.connect(lambda: setting_window(ui.actionUserList.objectName()))
        ui.actionTableList.triggered.connect(lambda: setting_window(ui.actionTableList.objectName()))
        ui.actionFoodList.triggered.connect(lambda: setting_window(ui.actionFoodList.objectName()))
        main.setGeometry(QRect(100, 100, 480, 700))
        main.show()
        main.setWindowTitle("工号：" + uid + " 姓名：" + uname)
    except Exception as e:
        print(e)


def setting_window(name):
    try:
        global uid
        ui = SettingMainWindow()
        ui.setupUi(main)
        ui.showWidget(name)
        # 1
        ui.actionSchedule.triggered.connect(lambda: schedule_window(ui.actionSchedule.objectName()))
        ui.actionTable.triggered.connect(lambda: schedule_window(ui.actionTable.objectName()))
        # 2
        ui.actionOrderNew.triggered.connect(lambda: order_window(ui.actionOrderNew.objectName()))
        ui.actionOrderList.triggered.connect(lambda: order_window(ui.actionOrderList.objectName()))
        # 3
        ui.actionOrderQuery.triggered.connect(lambda: report_window(ui.actionOrderQuery.objectName()))
        ui.actionAccountReport.triggered.connect(lambda: report_window(ui.actionAccountReport.objectName()))
        # 4
        ui.actionUserList.triggered.connect(lambda: ui.showWidget(ui.actionUserList.objectName()))
        ui.actionTableList.triggered.connect(lambda: ui.showWidget(ui.actionTableList.objectName()))
        ui.actionFoodList.triggered.connect(lambda: ui.showWidget(ui.actionFoodList.objectName()))
        main.setGeometry(QRect(100, 100, 480, 700))
        main.show()
        main.setWindowTitle("工号：" + uid + " 姓名：" + uname)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = QMainWindow()
    main.setGeometry(QRect(100, 100, 480, 700))
    login_ui = Ui_LoginWindow()
    login_ui.setupUi(main)
    btn = login_ui.btn_login
    main.show()
    # btn.clicked.connect(partial(login, login_ui))
    btn.clicked.connect(lambda: login(login_ui))
    app.exec_()


