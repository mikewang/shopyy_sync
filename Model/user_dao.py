# -*- coding: utf-8 -*-
import configparser
import traceback
import sys
import os
import pyodbc
import datetime
import base64
from Model.user import UserInfo
from Model.product import ProductInfo


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
            self.disk_path = config.get("db", "disk_path")
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

    def select_stock_product_list(self, page_no):
        try:
            product_list = []
            cnxn = pyodbc.connect(self._conn_str)
            cursor = cnxn.cursor()
            topN = page_no*10
            sql = "select top 10 v2.* from (select top " + str(topN) + " v1.* from (select a.ProductID,b.SpecNo, a.GoodsEName,c.ImageGuid,c.ImageFmt,c.ModuleID,CONVERT(varchar, c.FileDate, 120 ) as FileDate,c.ThumbImage from product_info as a join product_spec as b on a.ProductID=b.ProductID join Product_Image as c on b.RecGUID = c.RecGuid) as v1 order by productID desc, SpecNo desc)  as v2 order by productID asc,SpecNO asc"
            # 采购人	StockProductID	ProductID	SignDate	GoodsCode	SpecNo	GoodsSpec	GoodsUnit	_ImageID	ImageGuid	ImageFmt	ModuleID	FileDate	ThumbImage	其它.供应商名称	其它.允采购量	其它.应采购价	其它.商品品牌
            sql = "select  top 10 * from (select top " + str(topN) + " e.[采购人], a.StockProductID,a.ProductID,CONVERT(varchar, d.SignDate, 120 ) as SignDate,a.GoodsCode,a.SpecNo,f.GoodsCDesc, a.GoodsUnit, b._ImageID,c.ImageGuid,c.ImageFmt,c.ModuleID,CONVERT(varchar, c.FileDate, 120 ) as FileDate,c.ThumbImage,b.[其它.供应商名称],b.[其它.允采购量],b.[其它.应采购价],b.[其它.商品品牌]   FROM [FTTXRUN].[csidbo].[Stock_Product_Info] as a join  FTTXRUN.csidbo.FTPart_Stock_Product_Property_1 as b on a.StockProductID=b.MainID join csidbo.Product_Image as c on b._ImageID=c.ProductImageID join csidbo.stock_info d on d.ID=a.StockID join csidbo.[FTPart_Stock_Property_1] e on e.[MainID] = d.ID lef join csidbo.[Stock_Product_Info_Desc] f on a.StockProductID=f.StockProductID order by d.signdate desc,a.stockproductid desc) as v1 order by v1.SignDate asc,v1.StockProductID asc"
            cursor.execute(sql)
            for row in cursor:
                product = ProductInfo()
                product.OpCode = row[0]
                product.StockProductID = row[1]
                product.ProductID = row[2]
                product.SignDate = row[3]
                product.GoodsCode = row[4]
                product.SpecNo = row[5]
                product.GoodsCDesc = row[6]
                product.GoodsUnit = row[7]
                ImageID = row[8]
                product.ImageGuid = row[9]
                product.ImageFmt = row[10]
                product.ModuleID = row[11]
                product.FileDate = row[12]
                thumbImage = row[13]
                base64_bytes = base64.b64encode(thumbImage)
                base64_image = base64_bytes.decode("utf8")
                product.imageBase64 = base64_image
                product.supplier = row[14]
                product.permittedNum = row[15]
                product.shouldPrice = row[16]
                product.brand = row[17]
                product_list.append(product)
            cursor.close()
            cnxn.close()
            return product_list
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

    def select_brand_list(self):
        # SELECT *--[DictValue] 商品品牌
        # FROM [FTTXRUN].[csidbo].[CustomDict] where DictType=501027 and status=0
        pass

    def select_supplier_list(self):
        pass