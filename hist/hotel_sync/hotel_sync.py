# -*- coding: utf-8 -*-

import sys
import datetime
import os
import configparser
import pymysql
import pyodbc
import logging
import Scheduler


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
    config = configparser.ConfigParser()
    config_file = os.path.normpath(os.path.join(os.curdir, "config.ini"))
    config.read(config_file)
    mysql_host = config.get("mysql_db", "host")
    mysql_user = config.get("mysql_db", "user")
    mysql_password = config.get("mysql_db", "password")
    mysql_db = config.get("mysql_db", "db")
    mysql_port = int(config.get("mysql_db", "port"))
    conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, database=mysql_db, port=mysql_port)
    return conn


def conn_sqlserver():
    config = configparser.ConfigParser()
    config_file = os.path.normpath(os.path.join(os.curdir, "config.ini"))
    config.read(config_file)
    sqlserver_conn_str = config.get("sqlserver_db", "conn_str")
    conn = pyodbc.connect(sqlserver_conn_str)
    return conn


def home_days_sqlserver():
    room_client_list = []
    conn = conn_sqlserver()
    cur = conn.cursor()
    cur.execute("select a.roomno,a.the_man.,(select top 1 case sex when '男' then '先生' when '女' then '女士' else '' end as mr from receive where roomno=a.roomno and name = a.the_man) from home_days a")
    for row in cur:
        room = row[0]
        name = row[1] + " " + row[2]
        room_client = {"room": room, "name": name}
        room_client_list.append(room_client)
    cur.close()
    conn.close()
    return room_client_list


def client_mysql():
    room_client_list = []
    conn = conn_mysql()
    cur = conn.cursor()
    cur.execute("select room,clientname from client")
    for row in cur:
        room = row[0]
        name = row[1]
        room_client = {"room": room, "name": name}
        room_client_list.append(room_client)
    cur.close()
    conn.close()
    return room_client_list


def update_client_mysql(room_client):
    conn = conn_mysql()
    cur = conn.cursor()
    values = [room_client["name"], room_client["room"]]
    if room_client["name"] == '':
        cur.execute("update client set clientname = %s ,status = 1 where room = %s", values)
    else:
        cur.execute("update client set clientname = %s ,status = 0 where room = %s", values)
    if cur.rowcount == 1:
        print("更新成功", room_client)
    else:
        print("更新失败", room_client)
    conn.commit()
    cur.close()
    conn.close()


def sync_romm_client():
    run_time = datetime.datetime.now()
    run_time_str = run_time.strftime('%Y-%m-%d %H:%M:%S')
    print("数据同步开始", run_time_str)
    rows_updated = 0
    source_list = home_days_sqlserver()
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


if __name__ == '__main__':
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