# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'setting_form.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1014, 1025)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget_user_list = QtWidgets.QTabWidget(self.centralwidget)
        self.widget_user_list.setGeometry(QtCore.QRect(10, 10, 401, 611))
        self.widget_user_list.setObjectName("widget_user_list")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.lineEdit_27 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_27.setGeometry(QtCore.QRect(50, 20, 201, 20))
        self.lineEdit_27.setText("")
        self.lineEdit_27.setObjectName("lineEdit_27")
        self.label_54 = QtWidgets.QLabel(self.tab)
        self.label_54.setGeometry(QtCore.QRect(10, 20, 54, 12))
        self.label_54.setObjectName("label_54")
        self.pushButton_15 = QtWidgets.QPushButton(self.tab)
        self.pushButton_15.setGeometry(QtCore.QRect(270, 20, 101, 31))
        self.pushButton_15.setObjectName("pushButton_15")
        self.tableView = QtWidgets.QTableView(self.tab)
        self.tableView.setGeometry(QtCore.QRect(10, 70, 361, 411))
        self.tableView.setObjectName("tableView")
        self.pushButton_16 = QtWidgets.QPushButton(self.tab)
        self.pushButton_16.setGeometry(QtCore.QRect(20, 520, 101, 31))
        self.pushButton_16.setObjectName("pushButton_16")
        self.pushButton_17 = QtWidgets.QPushButton(self.tab)
        self.pushButton_17.setGeometry(QtCore.QRect(210, 520, 101, 31))
        self.pushButton_17.setObjectName("pushButton_17")
        self.widget_user_list.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.pushButton_14 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_14.setGeometry(QtCore.QRect(250, 320, 101, 31))
        self.pushButton_14.setObjectName("pushButton_14")
        self.lineEdit_26 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_26.setGeometry(QtCore.QRect(90, 60, 201, 20))
        self.lineEdit_26.setText("")
        self.lineEdit_26.setObjectName("lineEdit_26")
        self.label_53 = QtWidgets.QLabel(self.tab_2)
        self.label_53.setGeometry(QtCore.QRect(20, 110, 54, 12))
        self.label_53.setObjectName("label_53")
        self.label_52 = QtWidgets.QLabel(self.tab_2)
        self.label_52.setGeometry(QtCore.QRect(20, 160, 54, 12))
        self.label_52.setObjectName("label_52")
        self.dateEdit = QtWidgets.QDateEdit(self.tab_2)
        self.dateEdit.setGeometry(QtCore.QRect(90, 210, 201, 22))
        self.dateEdit.setObjectName("dateEdit")
        self.lineEdit_25 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_25.setGeometry(QtCore.QRect(90, 20, 201, 20))
        self.lineEdit_25.setText("")
        self.lineEdit_25.setObjectName("lineEdit_25")
        self.pushButton_13 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_13.setGeometry(QtCore.QRect(30, 320, 101, 31))
        self.pushButton_13.setObjectName("pushButton_13")
        self.label_50 = QtWidgets.QLabel(self.tab_2)
        self.label_50.setGeometry(QtCore.QRect(20, 60, 54, 12))
        self.label_50.setObjectName("label_50")
        self.comboBox = QtWidgets.QComboBox(self.tab_2)
        self.comboBox.setGeometry(QtCore.QRect(90, 110, 201, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.label_51 = QtWidgets.QLabel(self.tab_2)
        self.label_51.setGeometry(QtCore.QRect(30, 250, 54, 12))
        self.label_51.setObjectName("label_51")
        self.label_47 = QtWidgets.QLabel(self.tab_2)
        self.label_47.setGeometry(QtCore.QRect(20, 20, 71, 20))
        self.label_47.setObjectName("label_47")
        self.label_48 = QtWidgets.QLabel(self.tab_2)
        self.label_48.setGeometry(QtCore.QRect(10, 210, 71, 20))
        self.label_48.setObjectName("label_48")
        self.lineEdit_28 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_28.setGeometry(QtCore.QRect(90, 250, 201, 20))
        self.lineEdit_28.setText("")
        self.lineEdit_28.setObjectName("lineEdit_28")
        self.lineEdit_29 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_29.setGeometry(QtCore.QRect(90, 160, 201, 20))
        self.lineEdit_29.setText("")
        self.lineEdit_29.setObjectName("lineEdit_29")
        self.widget_user_list.addTab(self.tab_2, "")
        self.widget_table_list = QtWidgets.QTabWidget(self.centralwidget)
        self.widget_table_list.setGeometry(QtCore.QRect(470, 20, 401, 611))
        self.widget_table_list.setObjectName("widget_table_list")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.lineEdit_30 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_30.setGeometry(QtCore.QRect(50, 20, 201, 20))
        self.lineEdit_30.setText("")
        self.lineEdit_30.setObjectName("lineEdit_30")
        self.label_55 = QtWidgets.QLabel(self.tab_3)
        self.label_55.setGeometry(QtCore.QRect(10, 20, 54, 12))
        self.label_55.setObjectName("label_55")
        self.pushButton_18 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_18.setGeometry(QtCore.QRect(270, 20, 101, 31))
        self.pushButton_18.setObjectName("pushButton_18")
        self.tableView_2 = QtWidgets.QTableView(self.tab_3)
        self.tableView_2.setGeometry(QtCore.QRect(10, 70, 361, 411))
        self.tableView_2.setObjectName("tableView_2")
        self.pushButton_19 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_19.setGeometry(QtCore.QRect(20, 520, 101, 31))
        self.pushButton_19.setObjectName("pushButton_19")
        self.pushButton_20 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_20.setGeometry(QtCore.QRect(210, 520, 101, 31))
        self.pushButton_20.setObjectName("pushButton_20")
        self.widget_table_list.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.pushButton_21 = QtWidgets.QPushButton(self.tab_4)
        self.pushButton_21.setGeometry(QtCore.QRect(230, 300, 101, 31))
        self.pushButton_21.setObjectName("pushButton_21")
        self.lineEdit_31 = QtWidgets.QLineEdit(self.tab_4)
        self.lineEdit_31.setGeometry(QtCore.QRect(90, 60, 201, 20))
        self.lineEdit_31.setText("")
        self.lineEdit_31.setObjectName("lineEdit_31")
        self.label_56 = QtWidgets.QLabel(self.tab_4)
        self.label_56.setGeometry(QtCore.QRect(20, 110, 54, 12))
        self.label_56.setObjectName("label_56")
        self.label_57 = QtWidgets.QLabel(self.tab_4)
        self.label_57.setGeometry(QtCore.QRect(20, 160, 54, 12))
        self.label_57.setObjectName("label_57")
        self.lineEdit_32 = QtWidgets.QLineEdit(self.tab_4)
        self.lineEdit_32.setGeometry(QtCore.QRect(90, 20, 201, 20))
        self.lineEdit_32.setText("")
        self.lineEdit_32.setObjectName("lineEdit_32")
        self.pushButton_22 = QtWidgets.QPushButton(self.tab_4)
        self.pushButton_22.setGeometry(QtCore.QRect(30, 300, 101, 31))
        self.pushButton_22.setObjectName("pushButton_22")
        self.label_58 = QtWidgets.QLabel(self.tab_4)
        self.label_58.setGeometry(QtCore.QRect(20, 60, 54, 12))
        self.label_58.setObjectName("label_58")
        self.comboBox_2 = QtWidgets.QComboBox(self.tab_4)
        self.comboBox_2.setGeometry(QtCore.QRect(90, 110, 201, 22))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.label_49 = QtWidgets.QLabel(self.tab_4)
        self.label_49.setGeometry(QtCore.QRect(20, 20, 71, 20))
        self.label_49.setObjectName("label_49")
        self.lineEdit_34 = QtWidgets.QLineEdit(self.tab_4)
        self.lineEdit_34.setGeometry(QtCore.QRect(90, 160, 201, 20))
        self.lineEdit_34.setText("")
        self.lineEdit_34.setObjectName("lineEdit_34")
        self.widget_table_list.addTab(self.tab_4, "")
        self.widget_food_list = QtWidgets.QTabWidget(self.centralwidget)
        self.widget_food_list.setGeometry(QtCore.QRect(40, 650, 401, 611))
        self.widget_food_list.setObjectName("widget_food_list")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.lineEdit_33 = QtWidgets.QLineEdit(self.tab_5)
        self.lineEdit_33.setGeometry(QtCore.QRect(50, 20, 201, 20))
        self.lineEdit_33.setText("")
        self.lineEdit_33.setObjectName("lineEdit_33")
        self.label_59 = QtWidgets.QLabel(self.tab_5)
        self.label_59.setGeometry(QtCore.QRect(10, 20, 54, 12))
        self.label_59.setObjectName("label_59")
        self.pushButton_23 = QtWidgets.QPushButton(self.tab_5)
        self.pushButton_23.setGeometry(QtCore.QRect(270, 20, 101, 31))
        self.pushButton_23.setObjectName("pushButton_23")
        self.tableView_3 = QtWidgets.QTableView(self.tab_5)
        self.tableView_3.setGeometry(QtCore.QRect(10, 70, 361, 411))
        self.tableView_3.setObjectName("tableView_3")
        self.pushButton_24 = QtWidgets.QPushButton(self.tab_5)
        self.pushButton_24.setGeometry(QtCore.QRect(20, 520, 101, 31))
        self.pushButton_24.setObjectName("pushButton_24")
        self.pushButton_25 = QtWidgets.QPushButton(self.tab_5)
        self.pushButton_25.setGeometry(QtCore.QRect(210, 520, 101, 31))
        self.pushButton_25.setObjectName("pushButton_25")
        self.widget_food_list.addTab(self.tab_5, "")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.pushButton_26 = QtWidgets.QPushButton(self.tab_6)
        self.pushButton_26.setGeometry(QtCore.QRect(230, 300, 101, 31))
        self.pushButton_26.setObjectName("pushButton_26")
        self.lineEdit_35 = QtWidgets.QLineEdit(self.tab_6)
        self.lineEdit_35.setGeometry(QtCore.QRect(90, 60, 201, 20))
        self.lineEdit_35.setText("")
        self.lineEdit_35.setObjectName("lineEdit_35")
        self.label_61 = QtWidgets.QLabel(self.tab_6)
        self.label_61.setGeometry(QtCore.QRect(20, 120, 54, 12))
        self.label_61.setObjectName("label_61")
        self.lineEdit_36 = QtWidgets.QLineEdit(self.tab_6)
        self.lineEdit_36.setGeometry(QtCore.QRect(90, 20, 201, 20))
        self.lineEdit_36.setText("")
        self.lineEdit_36.setObjectName("lineEdit_36")
        self.pushButton_27 = QtWidgets.QPushButton(self.tab_6)
        self.pushButton_27.setGeometry(QtCore.QRect(30, 300, 101, 31))
        self.pushButton_27.setObjectName("pushButton_27")
        self.label_62 = QtWidgets.QLabel(self.tab_6)
        self.label_62.setGeometry(QtCore.QRect(20, 60, 54, 12))
        self.label_62.setObjectName("label_62")
        self.label_63 = QtWidgets.QLabel(self.tab_6)
        self.label_63.setGeometry(QtCore.QRect(20, 20, 71, 20))
        self.label_63.setObjectName("label_63")
        self.lineEdit_37 = QtWidgets.QLineEdit(self.tab_6)
        self.lineEdit_37.setGeometry(QtCore.QRect(90, 120, 201, 20))
        self.lineEdit_37.setText("")
        self.lineEdit_37.setObjectName("lineEdit_37")
        self.widget_food_list.addTab(self.tab_6, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1014, 23))
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
        self.widget_user_list.setCurrentIndex(0)
        self.widget_table_list.setCurrentIndex(0)
        self.widget_food_list.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "宾馆餐饮管理系统"))
        self.label_54.setText(_translate("MainWindow", "姓名"))
        self.pushButton_15.setText(_translate("MainWindow", "查询"))
        self.pushButton_16.setText(_translate("MainWindow", "新增"))
        self.pushButton_17.setText(_translate("MainWindow", "修改"))
        self.widget_user_list.setTabText(self.widget_user_list.indexOf(self.tab), _translate("MainWindow", "员工列表"))
        self.pushButton_14.setText(_translate("MainWindow", "确定"))
        self.label_53.setText(_translate("MainWindow", "岗位"))
        self.label_52.setText(_translate("MainWindow", "联系电话"))
        self.dateEdit.setDisplayFormat(_translate("MainWindow", "yyyy-M-d"))
        self.pushButton_13.setText(_translate("MainWindow", "重置"))
        self.label_50.setText(_translate("MainWindow", "姓名"))
        self.comboBox.setItemText(0, _translate("MainWindow", "主管"))
        self.comboBox.setItemText(1, _translate("MainWindow", "员工"))
        self.label_51.setText(_translate("MainWindow", "密码"))
        self.label_47.setText(_translate("MainWindow", "员工号"))
        self.label_48.setText(_translate("MainWindow", "入职日期"))
        self.widget_user_list.setTabText(self.widget_user_list.indexOf(self.tab_2), _translate("MainWindow", "员工编辑"))
        self.label_55.setText(_translate("MainWindow", "桌台号"))
        self.pushButton_18.setText(_translate("MainWindow", "查询"))
        self.pushButton_19.setText(_translate("MainWindow", "新增"))
        self.pushButton_20.setText(_translate("MainWindow", "修改"))
        self.widget_table_list.setTabText(self.widget_table_list.indexOf(self.tab_3), _translate("MainWindow", "桌台列表"))
        self.pushButton_21.setText(_translate("MainWindow", "确定"))
        self.label_56.setText(_translate("MainWindow", "状态"))
        self.label_57.setText(_translate("MainWindow", "规格"))
        self.pushButton_22.setText(_translate("MainWindow", "重置"))
        self.label_58.setText(_translate("MainWindow", "位置"))
        self.comboBox_2.setItemText(0, _translate("MainWindow", "正常"))
        self.comboBox_2.setItemText(1, _translate("MainWindow", "删除"))
        self.label_49.setText(_translate("MainWindow", "桌台号"))
        self.widget_table_list.setTabText(self.widget_table_list.indexOf(self.tab_4), _translate("MainWindow", "桌台编辑"))
        self.label_59.setText(_translate("MainWindow", "菜名"))
        self.pushButton_23.setText(_translate("MainWindow", "查询"))
        self.pushButton_24.setText(_translate("MainWindow", "新增"))
        self.pushButton_25.setText(_translate("MainWindow", "修改"))
        self.widget_food_list.setTabText(self.widget_food_list.indexOf(self.tab_5), _translate("MainWindow", "菜单列表"))
        self.pushButton_26.setText(_translate("MainWindow", "确定"))
        self.label_61.setText(_translate("MainWindow", "价格"))
        self.pushButton_27.setText(_translate("MainWindow", "重置"))
        self.label_62.setText(_translate("MainWindow", "类别"))
        self.label_63.setText(_translate("MainWindow", "名称"))
        self.widget_food_list.setTabText(self.widget_food_list.indexOf(self.tab_6), _translate("MainWindow", "菜单编辑"))
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

    # def showWidget(self, name):
    #     self.widget_user_list.hide()
    #     self.widget_table_list.hide()
    #     self.widget_food_list.hide()
    #     self.widget_table_list.setGeometry(self.widget_user_list.geometry())
    #     self.widget_food_list.setGeometry(self.widget_user_list.geometry())
    #     if name == self.actionUserList.objectName():
    #         self.widget_user_list.show()
    #     elif name == self.actionTableList.objectName():
    #         self.widget_table_list.show()
    #     elif name == self.actionFoodList.objectName():
    #         self.widget_food_list.show()
    #     else:
    #         self.widget_user_list.show()