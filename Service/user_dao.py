# -*- coding: utf-8 -*-
import configparser
import traceback
import sys
import os
import pyodbc
import datetime
from Model.user import UserInfo


class UserDao(object):

    def __init__(self):
        super(UserDao, self).__init__()
        try:
            config = configparser.ConfigParser()
            configure_file = 'OrderApi.ini'
            configure_filepath = os.path.join(os.curdir, 'config', configure_file)
            config.read(configure_filepath, encoding='UTF-8')
            file_existed = os.path.exists(configure_filepath)
            if file_existed == False:
                print("config file path is ", os.path.abspath(configure_filepath))
            for each_section in config.sections():
                for (each_key, each_val) in config.items(each_section):
                    # print(each_key, each_val)
                    pass
            self._conn_str = config.get("db", "conn_str")
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
            print('-' * 60)

    def select_user(self, OpCode):
        try:
            user_info = None
            cnxn = pyodbc.connect(self._conn_str)
            cursor = cnxn.cursor()
            sql = "SELECT [ID],[OpCode],[OpName],[OpEName],[Password],CONVERT(varchar, [CreateDate], 120 ) as  [CreateDate] ,[OrganizeID],[Position]," \
                  "[PurviewFunc],[OptionEx],[ManageType],[ManageShow],[ManOrganize],[ManPosition],[ManPurModal]," \
                  "[SortID],[Status],[CanFarLogin],[CanBsLogin],[CanMobLogin],[ManPicture],[DingID],[DingName] " \
                  " FROM [User_Info] where OpCode=?"
            sql = "select a.id,opcode,opname,opEname,[Password],CONVERT(varchar, a.[CreateDate], 120 ) as  [CreateDate] ,a.position,b.positionname from User_Info a join Position_Info b on a.Position=b.ID where a.OpCode=?"
            cursor.execute(sql, OpCode)
            row = cursor.fetchone()
            if row is not None:
                user_info = UserInfo()
                user_info.ID = row[0]
                user_info.OpCode = row[1]
                user_info.OpName = row[2]
                user_info.OpEName = row[3]
                user_info.Password = row[4]
                user_info.CreateDate = datetime.datetime.strptime(row[5], '%Y-%m-%d %H:%M:%S')
                user_info.Position = row[6]
                user_info.PositionName = row[7]
            else:
                print("User: " + OpCode + " Not Existed.")
            cursor.close()
            cnxn.close()
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
            print("done", user_info)
        finally:
            return user_info

    def select_product_image(self, GoodsCode):
        try:
            cnxn = pyodbc.connect(self._conn_str)
            cursor = cnxn.cursor()
            sql = "SELECT top 1 [ProductID],[ImageName],[ImageGuid],CONVERT(varchar, FileDate, 120 ) as [FileDate]," \
                  "[ModuleID], [ThumbImage]" \
                  " FROM [Product_Image] " \
                  "where [ProductID] in (select ProductID from product_info where GoodsCode=?) and [RecGuid]=''"
            cursor.execute(sql, GoodsCode)
            row = cursor.fetchone()
            if row is not None:
                product = dict()
                product["ProductID"] = row[0]
                product["ImageName"] = row[1]
                product["FileDate"] = row[3]
                product["ThumbImage"] = row[5]
                cursor.close()
                cnxn.close()
                return product
            else:
                return None
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