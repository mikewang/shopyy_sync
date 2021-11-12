# -*- coding: utf-8 -*-
import sys
import datetime
import os
import configparser
import pymysql
import pyodbc
import logging
import Scheduler as Scheduler
import requests
import json
import traceback


def test_mysql_connect():
    config = configparser.ConfigParser()
    config_file = os.path.normpath(os.path.join(os.curdir, "config.ini"))
    config.read(config_file)
    mysql_host = config.get("mysql_db", "host")
    mysql_user = config.get("mysql_db", "user")
    mysql_password = config.get("mysql_db", "password")
    mysql_db = config.get("mysql_db", "db")
    mysql_port = int(config.get("mysql_db", "port"))
    conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, database=mysql_db, port=mysql_port)
    cur = conn.cursor()
    cur.execute("select @@version")
    output = cur.fetchone()
    print(output)
    conn.close()


def test_sqlserver_connect():
    config = configparser.ConfigParser()
    config_file = os.path.normpath(os.path.join(os.curdir, "config.ini"))
    config.read(config_file)
    sqlserver_conn_str = config.get("sqlserver_db", "conn_str")
    conn = pyodbc.connect(sqlserver_conn_str)
    cur = conn.cursor()
    cur.execute("select @@version")
    output = cur.fetchone()
    print(output)
    conn.close()


def conn_mysql():
    try:
        config = configparser.ConfigParser()
        config_file = os.path.normpath(os.path.join(os.curdir, "config.ini"))
        config.read(config_file)
        mysql_host = config.get("mysql_db", "host")
        mysql_user = config.get("mysql_db", "user")
        mysql_password = config.get("mysql_db", "password")
        mysql_db = config.get("mysql_db", "db")
        mysql_port = int(config.get("mysql_db", "port"))
        conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, database=mysql_db, port=mysql_port)
    except:
        print("*"*30)
        print("mysql数据库连接异常，请检查")
    else:
        return conn


def conn_sqlserver():
    try:
        config = configparser.ConfigParser()
        config_file = os.path.normpath(os.path.join(os.curdir, "config.ini"))
        config.read(config_file)
        sqlserver_conn_str = config.get("sqlserver_db", "conn_str")
        conn = pyodbc.connect(sqlserver_conn_str)
    except:
        print("*"*30)
        print("sqlserver数据库连接异常，请检查")
    else:
        return conn


def get_name_sex(Sex, Birt):
    sex = '先生'
    if Sex is not None:
        if Sex == '女':
            sex = '女士'
    if Birt is not None:
        birthday = Birt[6:10]
        nowday = datetime.datetime.now().strftime('%m-%d')
        if birthday == nowday:
            sex = sex + ' 生日快乐'
    return sex


def get_guest_list(json_dict):
    try:
        room_client_list = []
        code = json_dict.get("Code")
        if code == 1000:
            result = json_dict.get("Result")
            for row in result:
                GuestName = row.get("GuestName")
                Sex = row.get("Sex")
                RoomNo = row.get("RoomNo")
                Birt = row.get("Birt")
                name_sex = GuestName + " " + get_name_sex(Sex, Birt)
                room_client = {"room": RoomNo, "name": name_sex}
                room_client_list.append(room_client)
        else:
            print(json_dict)
        return room_client_list
    except Exception as e:
        print('str(Exception):\t', str(Exception))
        print('str(e):\t\t', str(e))
        print('repr(e):\t', repr(e))
        # Get information about the exception that is currently being handled
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print('e.message:\t', exc_value)
        print("Note, object e and exc of Class %s is %s the same." %
              (type(exc_value), ('not', '')[exc_value is e]))
        print('traceback.print_exc(): ', traceback.print_exc())
        print('traceback.format_exc():\n%s' % traceback.format_exc())
        print('#' * 60)
        return None


def home_days_api():
    try:
        room_client_list = []
        json_dict = {}
        config = configparser.ConfigParser()
        config_file = os.path.normpath(os.path.join(os.curdir, "config.ini"))
        config.read(config_file)
        api = config.get("sync", "api")
        url = api
        time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(url, time_str)
        response = requests.session().get(url)
        response_text = ""
        if response.status_code == 200:
            response_text = response.text
            json_dict = json.loads(response_text)
            print(json_dict)
            room_client_list = get_guest_list(json_dict)
            # self.signal.emit({"message": str(json_dict)})
        else:
            print("response.status_code=" + str(response.status_code))
        print(url, "访问完成", time_str)
    except Exception as e:
        print('str(Exception):\t', str(Exception))
        print('str(e):\t\t', str(e))
        print('repr(e):\t', repr(e))
        # Get information about the exception that is currently being handled
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print('e.message:\t', exc_value)
        print("Note, object e and exc of Class %s is %s the same." %
              (type(exc_value), ('not', '')[exc_value is e]))
        print('traceback.print_exc(): ', traceback.print_exc())
        print('traceback.format_exc():\n%s' % traceback.format_exc())
        print('#' * 60)
    else:
        return room_client_list


def getCredInfo(cred_no):
    sex = '先生'
    if len(cred_no) == 18:
        sexno = cred_no[16:17]
        # print(sexno)
        if int(sexno) % 2 == 0:
            sex = '女士'
        birthday = cred_no[10:14]
        # print(birthday)
        nowday = datetime.datetime.now().strftime('%m%d')
        if birthday == nowday:
            sex = sex + ' 生日快乐'
    return sex


def home_days_sqlserver():
    try:
        room_client_list = []
        conn = conn_sqlserver()
        cur = conn.cursor()
        v_sql = "SELECT       [room_no]      ,[name]	,  [cred_no] FROM [t_u_order] "
        cur.execute(v_sql)
        for row in cur:
            room = row[0]
            name = row[1]
            cred_no = row[2]
            sex = getCredInfo(cred_no)
            leave_flag = 0
            name_sex = name + " " + sex
            if leave_flag == 1:
                name_sex = ''
            room_client = {"room": room, "name": name_sex}
            room_client_list.append(room_client)
        cur.close()
        conn.close()
    except:
        print("-" * 30)
        print("home_days_sqlserver异常，请检查")
    else:
        return room_client_list


def client_mysql():
    try:
        config = configparser.ConfigParser()
        config_file = os.path.normpath(os.path.join(os.curdir, "config.ini"))
        config.read(config_file)
        hotelid = int(config.get("mysql_db", "hotelid"))
        room_client_list = []
        conn = conn_mysql()
        cur = conn.cursor()
        values = [hotelid]
        cur.execute("select room,clientname from client where hotelid=%s", values)
        for row in cur:
            room = row[0]
            if room is None:
                room = ''
            name = row[1]
            if name is None:
                name = ''
            room_client = {"room": room, "name": name}
            room_client_list.append(room_client)
        cur.close()
        conn.close()
    except:
        print("-" * 30)
        print("client_mysql异常，请检查")
    else:
        return room_client_list


def update_client_mysql(room_client):
    try:
        config = configparser.ConfigParser()
        config_file = os.path.normpath(os.path.join(os.curdir, "config.ini"))
        config.read(config_file)
        hotelid = int(config.get("mysql_db", "hotelid"))
        conn = conn_mysql()
        cur = conn.cursor()
        values = [room_client["name"], room_client["room"], hotelid]
        if room_client["name"] == '':
            cur.execute("update client set clientname = %s ,status = 1 where room = %s and hotelid=%s", values)
        else:
            cur.execute("update client set clientname = %s ,status = 0 where room = %s and hotelid=%s", values)
        if cur.rowcount == 1:
            print("更新成功", room_client)
        else:
            print("更新失败", room_client)
        conn.commit()
        cur.close()
        conn.close()
    except:
        print("-" * 30)
        print("update_client_mysql异常，请检查")


def sync_romm_client():
    try:
        run_time = datetime.datetime.now()
        run_time_str = run_time.strftime('%Y-%m-%d %H:%M:%S')
        print("数据同步开始", run_time_str)
        rows_updated = 0
        source_list = home_days_api()
        target_list = client_mysql()
        for room_client_1 in source_list:
            for room_client_2 in target_list:
                if room_client_1["room"] == room_client_2["room"] and room_client_1["name"] != room_client_2["name"]:
                    print("更新数据", room_client_1["room"], room_client_1["name"])
                    logging.warning("更新数据" + ' ' + room_client_1["room"] + ' ' + room_client_1["name"])
                    update_client_mysql(room_client_1)
                    rows_updated = rows_updated + 1
        rows_clear = 0
        for room_client_2 in target_list:
            clear_enable = True
            if room_client_2["name"] == '':
                clear_enable = False
            else:
                for room_client_1 in source_list:
                    if room_client_1["room"] == room_client_2["room"]:
                        clear_enable = False
                        break
            if clear_enable:
                room_client = {"room": room_client_2["room"], "name": ''}
                print("清理数据", room_client_2["room"], room_client_2["name"])
                logging.warning("清理数据" + ' ' + room_client_2["room"] + ' ' + room_client_2["name"])
                update_client_mysql(room_client)
                rows_clear = rows_clear + 1
        run_time = datetime.datetime.now()
        run_time_str = run_time.strftime('%Y-%m-%d %H:%M:%S')
        print("数据同步完成", run_time_str, "更新记录数", rows_updated, "条", "清理记录数", rows_clear, "条")
        logging.warning("数据同步完成" + "更新记录数 " + str(rows_updated) + "条" + "; 清理记录数 " + str(rows_clear)+"条")
        print("-"*60)
    except:
        print("-" * 80)
        print("sync_romm_client异常，请检查")

if __name__ == '__main__':
    # cred_no = '320101198807154820'
    # ss = cred_no[16:17]
    # print(ss)
    # ss = cred_no[10:14]
    # print(ss)
    #
    # sex = getCredInfo(cred_no)
    # list = home_days_api()
    # print(list)
    # exit()
    logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                        level=logging.WARNING,
                        filename=os.path.join('log', 'hotel_sync.log'),
                        filemode='a')
    run_time = datetime.datetime.now()
    run_time_str = run_time.strftime('%Y-%m-%d %H:%M:%S')
    print("同步程序启动", run_time_str)
    logging.warning("同步程序启动")
    config = configparser.ConfigParser()
    config_file = os.path.normpath(os.path.join(os.curdir, "config.ini"))
    config.read(config_file)
    interval = int(config.get("sync", "interval"))
    default_scheduler = Scheduler.Scheduler()
    default_scheduler.every(interval).seconds.do(sync_romm_client)
    default_scheduler.run_continuously(1)

    # the end