# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'order_form.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(989, 754)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget_order_new = QtWidgets.QTabWidget(self.centralwidget)
        self.widget_order_new.setEnabled(True)
        self.widget_order_new.setGeometry(QtCore.QRect(10, 10, 431, 661))
        self.widget_order_new.setObjectName("widget_order_new")
        self.tab_7 = QtWidgets.QWidget()
        self.tab_7.setObjectName("tab_7")
        self.table_order_food_list = QtWidgets.QTableView(self.tab_7)
        self.table_order_food_list.setGeometry(QtCore.QRect(10, 170, 401, 421))
        self.table_order_food_list.setObjectName("table_order_food_list")
        self.label_45 = QtWidgets.QLabel(self.tab_7)
        self.label_45.setGeometry(QtCore.QRect(10, 20, 71, 20))
        self.label_45.setObjectName("label_45")
        self.input_order_clicked = QtWidgets.QDateTimeEdit(self.tab_7)
        self.input_order_clicked.setGeometry(QtCore.QRect(80, 50, 201, 22))
        self.input_order_clicked.setObjectName("input_order_clicked")
        self.label_49 = QtWidgets.QLabel(self.tab_7)
        self.label_49.setGeometry(QtCore.QRect(20, 90, 54, 12))
        self.label_49.setObjectName("label_49")
        self.label_31 = QtWidgets.QLabel(self.tab_7)
        self.label_31.setGeometry(QtCore.QRect(20, 130, 54, 12))
        self.label_31.setObjectName("label_31")
        self.input_customer = QtWidgets.QLineEdit(self.tab_7)
        self.input_customer.setGeometry(QtCore.QRect(80, 130, 201, 20))
        self.input_customer.setObjectName("input_customer")
        self.label_44 = QtWidgets.QLabel(self.tab_7)
        self.label_44.setGeometry(QtCore.QRect(10, 50, 71, 20))
        self.label_44.setObjectName("label_44")
        self.input_table_no = QtWidgets.QLineEdit(self.tab_7)
        self.input_table_no.setGeometry(QtCore.QRect(80, 90, 201, 20))
        self.input_table_no.setText("")
        self.input_table_no.setObjectName("input_table_no")
        self.input_order_no = QtWidgets.QLineEdit(self.tab_7)
        self.input_order_no.setEnabled(True)
        self.input_order_no.setGeometry(QtCore.QRect(80, 20, 201, 20))
        self.input_order_no.setText("")
        self.input_order_no.setObjectName("input_order_no")
        self.btn_order_check = QtWidgets.QPushButton(self.tab_7)
        self.btn_order_check.setGeometry(QtCore.QRect(300, 20, 101, 31))
        self.btn_order_check.setObjectName("btn_order_check")
        self.checkBox_order_checked = QtWidgets.QCheckBox(self.tab_7)
        self.checkBox_order_checked.setGeometry(QtCore.QRect(300, 70, 71, 16))
        self.checkBox_order_checked.setObjectName("checkBox_order_checked")
        self.widget_order_new.addTab(self.tab_7, "")
        self.tab_8 = QtWidgets.QWidget()
        self.tab_8.setObjectName("tab_8")
        self.input_food_name = QtWidgets.QLineEdit(self.tab_8)
        self.input_food_name.setGeometry(QtCore.QRect(60, 20, 201, 20))
        self.input_food_name.setObjectName("input_food_name")
        self.label_38 = QtWidgets.QLabel(self.tab_8)
        self.label_38.setGeometry(QtCore.QRect(10, 20, 54, 12))
        self.label_38.setObjectName("label_38")
        self.btn_food_query = QtWidgets.QPushButton(self.tab_8)
        self.btn_food_query.setGeometry(QtCore.QRect(274, 20, 61, 23))
        self.btn_food_query.setObjectName("btn_food_query")
        self.table_food_query = QtWidgets.QTableView(self.tab_8)
        self.table_food_query.setGeometry(QtCore.QRect(10, 70, 401, 531))
        self.table_food_query.setObjectName("table_food_query")
        self.btn_food_check = QtWidgets.QPushButton(self.tab_8)
        self.btn_food_check.setGeometry(QtCore.QRect(354, 20, 61, 23))
        self.btn_food_check.setObjectName("btn_food_check")
        self.widget_order_new.addTab(self.tab_8, "")
        self.widget_order_list = QtWidgets.QWidget(self.centralwidget)
        self.widget_order_list.setGeometry(QtCore.QRect(500, 20, 451, 651))
        self.widget_order_list.setObjectName("widget_order_list")
        self.label_47 = QtWidgets.QLabel(self.widget_order_list)
        self.label_47.setGeometry(QtCore.QRect(20, 30, 71, 20))
        self.label_47.setObjectName("label_47")
        self.input_order_no_account = QtWidgets.QLineEdit(self.widget_order_list)
        self.input_order_no_account.setGeometry(QtCore.QRect(90, 30, 201, 20))
        self.input_order_no_account.setText("")
        self.input_order_no_account.setObjectName("input_order_no_account")
        self.input_table_no_account = QtWidgets.QLineEdit(self.widget_order_list)
        self.input_table_no_account.setGeometry(QtCore.QRect(90, 70, 201, 20))
        self.input_table_no_account.setText("")
        self.input_table_no_account.setObjectName("input_table_no_account")
        self.label_50 = QtWidgets.QLabel(self.widget_order_list)
        self.label_50.setGeometry(QtCore.QRect(20, 70, 54, 12))
        self.label_50.setObjectName("label_50")
        self.table_order_food_list_account = QtWidgets.QTableView(self.widget_order_list)
        self.table_order_food_list_account.setGeometry(QtCore.QRect(10, 110, 421, 291))
        self.table_order_food_list_account.setObjectName("table_order_food_list_account")
        self.input_should_money_account = QtWidgets.QLineEdit(self.widget_order_list)
        self.input_should_money_account.setGeometry(QtCore.QRect(80, 420, 201, 20))
        self.input_should_money_account.setText("")
        self.input_should_money_account.setObjectName("input_should_money_account")
        self.label_51 = QtWidgets.QLabel(self.widget_order_list)
        self.label_51.setGeometry(QtCore.QRect(20, 420, 54, 12))
        self.label_51.setObjectName("label_51")
        self.label_52 = QtWidgets.QLabel(self.widget_order_list)
        self.label_52.setGeometry(QtCore.QRect(20, 470, 54, 12))
        self.label_52.setObjectName("label_52")
        self.input_real_money_account = QtWidgets.QLineEdit(self.widget_order_list)
        self.input_real_money_account.setGeometry(QtCore.QRect(80, 470, 201, 20))
        self.input_real_money_account.setText("")
        self.input_real_money_account.setObjectName("input_real_money_account")
        self.label_53 = QtWidgets.QLabel(self.widget_order_list)
        self.label_53.setGeometry(QtCore.QRect(20, 510, 54, 12))
        self.label_53.setObjectName("label_53")
        self.input_combox_money_type_account = QtWidgets.QComboBox(self.widget_order_list)
        self.input_combox_money_type_account.setGeometry(QtCore.QRect(80, 510, 201, 22))
        self.input_combox_money_type_account.setObjectName("input_combox_money_type_account")
        self.input_combox_money_type_account.addItem("")
        self.input_combox_money_type_account.addItem("")
        self.input_combox_money_type_account.addItem("")
        self.input_combox_money_type_account.addItem("")
        self.btn_order_save_account = QtWidgets.QPushButton(self.widget_order_list)
        self.btn_order_save_account.setGeometry(QtCore.QRect(70, 600, 301, 31))
        self.btn_order_save_account.setObjectName("btn_order_save_account")
        self.btn_order_query_account = QtWidgets.QPushButton(self.widget_order_list)
        self.btn_order_query_account.setGeometry(QtCore.QRect(300, 30, 131, 31))
        self.btn_order_query_account.setObjectName("btn_order_query_account")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 989, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_4 = QtWidgets.QMenu(self.menubar)
        self.menu_4.setObjectName("menu_4")
        self.menu_5 = QtWidgets.QMenu(self.menubar)
        self.menu_5.setObjectName("menu_5")
        self.menu_6 = QtWidgets.QMenu(self.menubar)
        self.menu_6.setObjectName("menu_6")
        MainWindow.setMenuBar(self.menubar)
        self.actionSchedule = QtWidgets.QAction(MainWindow)
        self.actionSchedule.setObjectName("actionSchedule")
        self.actionTable = QtWidgets.QAction(MainWindow)
        self.actionTable.setObjectName("actionTable")
        self.actionOrderNew = QtWidgets.QAction(MainWindow)
        self.actionOrderNew.setObjectName("actionOrderNew")
        self.actionOrderList = QtWidgets.QAction(MainWindow)
        self.actionOrderList.setObjectName("actionOrderList")
        self.actionOrderQuery = QtWidgets.QAction(MainWindow)
        self.actionOrderQuery.setObjectName("actionOrderQuery")
        self.actionAccountReport = QtWidgets.QAction(MainWindow)
        self.actionAccountReport.setObjectName("actionAccountReport")
        self.actionUserList = QtWidgets.QAction(MainWindow)
        self.actionUserList.setObjectName("actionUserList")
        self.actionTableList = QtWidgets.QAction(MainWindow)
        self.actionTableList.setObjectName("actionTableList")
        self.actionFoodList = QtWidgets.QAction(MainWindow)
        self.actionFoodList.setObjectName("actionFoodList")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionHelp = QtWidgets.QAction(MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.menu.addAction(self.actionSchedule)
        self.menu.addAction(self.actionTable)
        self.menu_2.addAction(self.actionOrderNew)
        self.menu_2.addAction(self.actionOrderList)
        self.menu_4.addAction(self.actionOrderQuery)
        self.menu_4.addAction(self.actionAccountReport)
        self.menu_5.addAction(self.actionUserList)
        self.menu_5.addAction(self.actionTableList)
        self.menu_5.addAction(self.actionFoodList)
        self.menu_6.addAction(self.actionExit)
        self.menu_6.addAction(self.actionHelp)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())
        self.menubar.addAction(self.menu_5.menuAction())
        self.menubar.addAction(self.menu_6.menuAction())

        self.retranslateUi(MainWindow)
        self.widget_order_new.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "宾馆餐饮管理系统"))
        self.label_45.setText(_translate("MainWindow", "订单号"))
        self.input_order_clicked.setDisplayFormat(_translate("MainWindow", "yyyy-MM-dd H:mm"))
        self.label_49.setText(_translate("MainWindow", "桌台号"))
        self.label_31.setText(_translate("MainWindow", "顾客"))
        self.label_44.setText(_translate("MainWindow", "点菜时间"))
        self.btn_order_check.setText(_translate("MainWindow", "订单确定"))
        self.checkBox_order_checked.setText(_translate("MainWindow", "有效订单"))
        self.widget_order_new.setTabText(self.widget_order_new.indexOf(self.tab_7), _translate("MainWindow", "点单"))
        self.label_38.setText(_translate("MainWindow", "菜名"))
        self.btn_food_query.setText(_translate("MainWindow", "查询"))
        self.btn_food_check.setText(_translate("MainWindow", "选中"))
        self.widget_order_new.setTabText(self.widget_order_new.indexOf(self.tab_8), _translate("MainWindow", "菜单"))
        self.label_47.setText(_translate("MainWindow", "订单号"))
        self.label_50.setText(_translate("MainWindow", "桌台号"))
        self.label_51.setText(_translate("MainWindow", "应付金额"))
        self.label_52.setText(_translate("MainWindow", "实付金额"))
        self.label_53.setText(_translate("MainWindow", "付款方式"))
        self.input_combox_money_type_account.setItemText(0, _translate("MainWindow", "支付宝"))
        self.input_combox_money_type_account.setItemText(1, _translate("MainWindow", "微信"))
        self.input_combox_money_type_account.setItemText(2, _translate("MainWindow", "现金"))
        self.input_combox_money_type_account.setItemText(3, _translate("MainWindow", "其他"))
        self.btn_order_save_account.setText(_translate("MainWindow", "订单结算"))
        self.btn_order_query_account.setText(_translate("MainWindow", "订单查询"))
        self.menu.setTitle(_translate("MainWindow", "订餐"))
        self.menu_2.setTitle(_translate("MainWindow", "帐单"))
        self.menu_4.setTitle(_translate("MainWindow", "报表与统计"))
        self.menu_5.setTitle(_translate("MainWindow", "设置"))
        self.menu_6.setTitle(_translate("MainWindow", "系统"))
        self.actionSchedule.setText(_translate("MainWindow", "预定"))
        self.actionTable.setText(_translate("MainWindow", "桌台"))
        self.actionOrderNew.setText(_translate("MainWindow", "点单"))
        self.actionOrderList.setText(_translate("MainWindow", "结算"))
        self.actionOrderQuery.setText(_translate("MainWindow", "高级查询"))
        self.actionAccountReport.setText(_translate("MainWindow", "报表"))
        self.actionUserList.setText(_translate("MainWindow", "员工管理"))
        self.actionTableList.setText(_translate("MainWindow", "桌台管理"))
        self.actionFoodList.setText(_translate("MainWindow", "菜单管理"))
        self.actionExit.setText(_translate("MainWindow", "退出"))
        self.actionHelp.setText(_translate("MainWindow", "帮助"))
