import datetime
import json
import re
import threading
import time
import urllib.request as urllib2
import pyodbc
import requests
from PIL import Image
import os
import io
import platform
from pathlib import Path
import tkinter as tk
import tkinter.ttk as ttk
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton

from PyQt5.QtGui import QPixmap


def sync_image(diskpath):
    try:
        diskpath = diskpath.strip()
        conn = pyodbc.connect('DSN=mydsn;UID=sa;PWD=sa;Database=smj')
        #conn = pyodbc.connect('DRIVER={SQL Server Native Client 10.0};SERVER=127.0.0.1;DATABASE=smj;UID=sa;PWD=sa')
        cursor = conn.cursor()
        cursor.execute("select recnumgather, imagedescid, imageid, imagefile from v_photo order by recnumgather,imagedescid, disporeder")
        for row in cursor:
            filedir = str(row.recnumgather)
            dirpath = os.path.normpath(os.path.join(diskpath, 'photos', filedir))
            #print(dirpath)
            isDirExists = os.path.exists(dirpath)
            filename = str(row.imageid) + '.png'
            filepath = os.path.normpath(os.path.join(dirpath, filename))
            #print(filepath)
            isFileExists = os.path.exists(filepath)

            if not isDirExists:
                print(dirpath + ' create')
                Path(dirpath).mkdir(parents=True, exist_ok=True)
            else:
                if not os.path.isdir(dirpath):
                    os.remove(dirpath)
                    Path(dirpath).mkdir(parents=True, exist_ok=True)
            if not isFileExists:
                # 读取图片，二进制格式，注意是rb
                # data = urllib2.urlopen(url).read()
                data = row.imagefile
                image = Image.open(io.BytesIO(data))
                image.save(filepath)
                t1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(filepath + ' 保存：' + t1)
            else:
                t1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(filepath + ' 已存在：' + t1)
        cursor.close()
        conn.close()
        print("导出完成。")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = QWidget()
    w.resize(800,600)
    w.move(300,300)
    w.setWindowTitle('sync_shopyy photo')
    w.show()
    sys.exit(app.exec_())

    sysstr = platform.system()
    print(sysstr)
    print('请输入磁盘符，例如 D:\\')
    diskpath = input()
    t1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print( '开始运行：' + t1)
    sync_image(diskpath)
    print('运行结束：' + t1)
    path = input()