import traceback
from PyQt5.QtCore import QThread, QCoreApplication, QObject, pyqtSignal, pyqtSlot, Qt
import datetime
import sys
import time
import requests
import os
import configparser
import json
import logging
import hashlib
import pandas as pd


class Sync_Request_Api(QObject):
    signal = pyqtSignal(dict)

    def __init__(self):
        super(Sync_Request_Api, self).__init__()

    def __del__(self):
        self.wait()

    @pyqtSlot()
    def request_category_list(self, domain_name, token):
        try:
            api = "api-erp-categoryList.html"
            print('请求' + api + ' 开始 ', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            url = domain_name + api
            data = {'token': token}
            response = requests.session().post(url, data=data)
            print(url)
            response_text = ""
            if response.status_code == 200:
                response_text = response.text
                json_dict = json.loads(response_text)
                self.signal.emit({"message": str(json_dict)})
            else:
                print("response.status_code=" + str(response.status_code))
            print('请求' + api + ' 结束 ', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            return json_dict
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




