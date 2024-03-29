# -*- coding: utf-8 -*-
from PyQt5.QtCore import QObject, pyqtSignal
import configparser
import traceback
import sys
import io
import os
from pathlib import Path
from PIL import Image
import hashlib
import pyodbc
import datetime
from hist.sync_shopyy import global_v as gl


class SyncDao(QObject):
    signal = pyqtSignal(dict)
    _conn_str = ""
    _disk_path = "/tmp"

    def __init__(self):
        super(SyncDao, self).__init__()
        try:
            config = configparser.ConfigParser()
            configure_file = 'ymcart.ini'
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
            self._disk_path = config.get("db", "disk_path")
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

    def __del__(self):
       print("auto del", self)
    
    def merge_product_type_list(self, domain_name, product_type_list):
        try:
            # Insert into Product_Type(ProductTypeID,ParentID,TypeName,SortID) values()
            cnxn = pyodbc.connect(self._conn_str)
            cursor = cnxn.cursor()
            for prod_type in product_type_list:
                # self.signal.emit({"message": str(prod_type)})
                sql = "select ParentID, TypeName, SortID from Product_Type where ProductTypeID=?"
                cursor.execute(sql, prod_type["ProductTypeID"])
                record = cursor.fetchone()
                if record is None:
                    sql = "set identity_insert Product_Type on"
                    cursor.execute(sql)
                    sql = "Insert into Product_Type" \
                          "(ProductTypeID,ParentID,TypeName,SortID,OwnerType,OwnerCust,OwnerOpCode,OwnerName,SchemeID," \
                          "CreateOpCode,CreateDate,EditDate,IsShare,IsChildShare,IsUsePowerRights,Memo,status)" \
                          " values(?,?,?,?,'0',0,'delong','梁德龙',0,'delong',getdate(),getdate(),'0','','0','','0')"
                    cursor.execute(sql, prod_type["ProductTypeID"], prod_type["ParentID"], prod_type["TypeName"],
                                   prod_type["SortID"])
                    sql = "set identity_insert Product_Type off"
                    cursor.execute(sql)
                    cursor.commit()
                else:
                    ParentID = record[0]
                    TypeName = record[1]
                    SortID = record[2]
                    if ParentID != prod_type["ParentID"] or TypeName != prod_type["TypeName"] or SortID != prod_type[
                        "SortID"]:
                        sql = "update Product_Type set ParentID=?, TypeName=?, SortID=? where ProductTypeID=?"
                        cursor.execute(sql, prod_type["ParentID"], prod_type["TypeName"], prod_type["SortID"],
                                       prod_type["ProductTypeID"])
                        cursor.commit()
                    else:
                        pass
                        # print("不需要更新", TypeName)
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

    def merge_product_info(self, domain_name, info):
        try:
            # print(merge_product_info, info)
            cnxn = pyodbc.connect(self._conn_str)
            cursor = cnxn.cursor()
            if domain_name == gl.pf_domain:
                sql = "select TypeID,GoodsCode, GoodsEName,CONVERT(varchar, CreateDate, 120 ) as CreateDate," \
                      "CONVERT(varchar, EditDate, 120 ) as EditDate, Status, ProductActive from Product_Info where ProductID=?"
                # print("ProductID", info["ProductID"])
                cursor.execute(sql, info["ProductID"])
                row = cursor.fetchone()
                if row is None:
                    sql = "select ProductID, TypeID,GoodsCode, GoodsEName,CONVERT(varchar, CreateDate, 120 ) as CreateDate," \
                          "CONVERT(varchar, EditDate, 120 ) as EditDate, Status, ProductActive from Product_Info where GoodsCode=?"
                    # print("ProductID", info["ProductID"], info["GoodsCode"])
                    cursor.execute(sql, info["GoodsCode"])
                    row = cursor.fetchone()
                    if row is not None:
                        sql = "delete from Product_Info where GoodsCode = ?"
                        cursor.execute(sql, info["GoodsCode"])
                        cursor.commit()
                        # 规格等附加记录的删除后面完善
                    sql = "set identity_insert Product_Info on"
                    cursor.execute(sql)
                    sql = "Insert into Product_Info(ProductID, TypeID, GoodsCode, GoodsEName, CreateDate, EditDate," \
                          "SchemeID,ShopTypeID,HSCode,GoodsCName,CustGoodsCode,GoodsMemo,ImageNum,IsAutoCode," \
                          "ProductCustID, ProductCustName,ProductActive,Status,EditNum,OpCode,OpName, EditOpCode, EditOpName)" \
                          " values(?,?,?,?,?,?,0,0,'','','','',1,'',0,'',?,'0',1,'delong','梁德龙','delong','梁德龙')"
                    cursor.execute(sql, info["ProductID"], info["TypeID"], info["GoodsCode"], info["GoodsEName"],
                                   datetime.datetime.strptime(info["CreateDate"], '%Y-%m-%d %H:%M:%S'),
                                   datetime.datetime.strptime(info["EditDate"], '%Y-%m-%d %H:%M:%S'),
                                   info["ProductActive"])
                    print("新增", info["GoodsCode"])
                    sql = "set identity_insert Product_Info off"
                    cursor.execute(sql)
                    cursor.commit()
                else:
                    TypeID = row[0]
                    GoodsCode = row[1]
                    GoodsEName = row[2]
                    CreateDate = row[3]
                    EditDate = row[4]
                    Status = row[5]
                    ProductActive = row[6]
                    if TypeID != info["TypeID"] or GoodsCode != info["GoodsCode"] or GoodsEName != info["GoodsEName"] \
                            or CreateDate != info["CreateDate"] or EditDate != info["EditDate"] \
                            or ProductActive != info["ProductActive"]:
                        # print("更新", info["CreateDate"], info["EditDate"])
                        sql = "update Product_Info " \
                              "set ProductActive=?, TypeID=?, GoodsCode=?, GoodsEName=?, CreateDate=?, EditDate=? " \
                              "where ProductID=?"
                        cursor.execute(sql, info["ProductActive"], info["TypeID"], info["GoodsCode"], info["GoodsEName"],
                                       datetime.datetime.strptime(info["CreateDate"], '%Y-%m-%d %H:%M:%S'),
                                       datetime.datetime.strptime(info["EditDate"], '%Y-%m-%d %H:%M:%S'),
                                       info["ProductID"])
                        print("更新", info["GoodsCode"])
                        cursor.commit()
                    else:
                        pass
                        # print("不需要更新", GoodsEName)
                # 补充字段 品牌.商品品牌 自定义
                body_product_spec = info["body_product_spec"]
                # print("补充字段 品牌.商品品牌", body_product_spec)
                sql = "SELECT [品牌.商品品牌], [品牌.domain], [品牌.来源]" \
                      "FROM [FTPart_Product_Info_property_1] WHERE [MainID] = ?"
                cursor.execute(sql, info["ProductID"])
                record = cursor.fetchone()
                product_source = "批发"
                if record is None:
                    sql = "insert into [FTPart_Product_Info_property_1]" \
                          "([MainID], [ExtendID], [_SelfImageType], [_ImageID], [_LineColor],[_PrintNum]," \
                          "[_FaxNum], [_EmailNum], [_CheckResult], [品牌.商品品牌], [品牌.domain],[品牌.来源]) " \
                          "values(?,1,0,0,0,0,0,0,0,?,?,?)"
                    cursor.execute(sql, info["ProductID"], body_product_spec["brand_name"], domain_name,
                                   product_source)
                    print("新增 品牌.商品品牌,domain,来源", info["GoodsCode"])
                    cursor.commit()
                else:
                    brand_name = record[0]
                    domain_name = record[1]
                    product_source_name = record[2]
                    if brand_name != body_product_spec["brand_name"]:
                        sql = "update [FTPart_Product_Info_property_1] set [品牌.商品品牌]=? " \
                              "where [MainID]=? "
                        cursor.execute(sql, body_product_spec["brand_name"], info["ProductID"])
                        print("更新 品牌.商品品牌", info["GoodsCode"])
                        cursor.commit()
                    else:
                        pass
            elif domain_name == gl.ls_domain:
                sql = "select TypeID,GoodsCode, GoodsEName," \
                      "CONVERT(varchar, CreateDate, 120 ) as CreateDate," \
                      "CONVERT(varchar, EditDate, 120 ) as EditDate, Status, ProductActive, ProductID " \
                      " from Product_Info where GoodsCode=?"
                # print("ProductID", info["ProductID"], info["GoodsCode"])
                cursor.execute(sql, info["GoodsCode"])
                row = cursor.fetchone()
                if row is None:
                    sql = "set identity_insert Product_Info on"
                    cursor.execute(sql)
                    sql = "Insert into Product_Info" \
                          "(ProductID, TypeID, GoodsCode, GoodsEName, CreateDate, EditDate,SchemeID,ShopTypeID," \
                          "HSCode,GoodsCName,CustGoodsCode,GoodsMemo,ImageNum,IsAutoCode,ProductCustID," \
                          " ProductCustName,ProductActive,Status,EditNum,OpCode,OpName, EditOpCode, EditOpName)" \
                          " values(?,?,?,?,?,?,0,0,'','','','',1,'',0,'',?,'0',1,'delong','梁德龙','delong','梁德龙')"
                    # print(info)
                    # print(sql)
                    # cursor.execute(sql, info["ProductID"], info["TypeID"], info["GoodsCode"],
                    # info["GoodsEName"], info["CreateDate"], info["EditDate"]),
                    # datetime.strptime(info["CreateDate"], '%y-%m-%d %H:%M:%S').fromtimestamp(0)
                    cursor.execute(sql, info["ProductID"], info["TypeID"], info["GoodsCode"], info["GoodsEName"],
                                   datetime.datetime.strptime(info["CreateDate"], '%Y-%m-%d %H:%M:%S'),
                                   datetime.datetime.strptime(info["EditDate"], '%Y-%m-%d %H:%M:%S'),
                                   info["ProductActive"])
                    print("新增", info["GoodsCode"])
                    sql = "set identity_insert Product_Info off"
                    cursor.execute(sql)
                    cursor.commit()
                    # 补充字段 品牌.商品品牌 自定义
                    body_product_spec = info["body_product_spec"]
                    # print("补充字段 品牌.商品品牌", body_product_spec)
                    sql = "SELECT [品牌.商品品牌], [品牌.domain], [品牌.来源]" \
                          "FROM [FTPart_Product_Info_property_1] WHERE [MainID] = ?"
                    cursor.execute(sql, info["ProductID"])
                    record = cursor.fetchone()
                    product_source = "零售"
                    if record is None:
                        sql = "insert into [FTPart_Product_Info_property_1]" \
                              "([MainID], [ExtendID], [_SelfImageType], [_ImageID], [_LineColor],[_PrintNum]," \
                              "[_FaxNum], [_EmailNum], [_CheckResult], [品牌.商品品牌], [品牌.domain],[品牌.来源]) " \
                              "values(?,1,0,0,0,0,0,0,0,?,?,?)"
                        cursor.execute(sql, info["ProductID"], body_product_spec["brand_name"], domain_name,
                                       product_source)
                        print("新增 品牌.商品品牌,domain,来源", info["GoodsCode"])
                        cursor.commit()
                    else:
                        brand_name = record[0]
                        domain_name = record[1]
                        product_source_name = record[2]
                        if brand_name != body_product_spec["brand_name"]:
                            sql = "update [FTPart_Product_Info_property_1] set [品牌.商品品牌]=? " \
                                  "where [MainID]=? "
                            cursor.execute(sql, body_product_spec["brand_name"], info["ProductID"])
                            print("更新 品牌.商品品牌", info["GoodsCode"])
                            cursor.commit()
                        else:
                            pass
                else:
                    TypeID = row[0]
                    GoodsCode = row[1]
                    GoodsEName = row[2]
                    CreateDate = row[3]
                    EditDate = row[4]
                    Status = row[5]
                    ProductActive = row[6]
                    ProductID = row[7]
                    # print("不更新 零售", GoodsCode)
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

    def generate_product_image(self, product, spec_image):
        try:
            if spec_image is None:
                url = product["image"]
                if url is None:
                    print("产品:" + str(product["GoodsCode"]) + " 主图为空")
                    return None
                RecGuid = ''
                CreateDate = product["CreateDate"]
                EditDate = product["EditDate"]
            else:
                url = spec_image['image']
                if url is None:
                    print("产品:" + str(product["GoodsCode"]) + " 规格" + spec_image["sku_value"] + "图为空")
                    return None
                RecGuid = spec_image["RecGuid"]
                CreateDate = spec_image["SysNoTime"]
                EditDate = spec_image["LastEditTime"]
            # print(product.py["image"])
            # print("RecGuid", RecGuid)
            year = CreateDate.split('-')[0]
            month = CreateDate.split('-')[1]
            day = CreateDate.split('-')[2].split(" ")[0]
            ModuleID = "501"
            dir_path = os.path.normpath(os.path.join(self._disk_path, year, month, ModuleID))
            if not os.path.exists(dir_path):
                Path(dir_path).mkdir(parents=True, exist_ok=True)
            # try:
            #     if '/' in url:
            #         local_filename = url.split('/')[-1]
            #         if '.' in local_filename:
            #             ImageFmt = '.' + local_filename.split('.')[1]
            #         else:
            #             print("url error:", url)
            #             return None
            #     else:
            #         print("url error:", url)
            #         return None
            # except Exception as e:
            #     print("url", url)
            #     print(e)
            # print(url)
            local_filename = url.split('/')[-1]
            ImageFmt = '.' + local_filename.split('.')[1]
            ImageName = local_filename
            ImageType = 1
            md = hashlib.md5()
            md.update(url.encode('utf-8'))
            ImageGuid = year + month + day + md.hexdigest().upper()
            filepath = os.path.normpath(os.path.join(dir_path, ImageGuid))
            IsDefault = '1'
            # print("image url", url)
            # Product_Image(ProductID,RecGuid,ImageType,ImageName,ImageGuid,ImageSize,ImageFmt,IsDefault,
            # FileDate,EditDate,ThumbImage,ModuleID)
            #  "CreateDate": goods_create_time_str, "EditDate": goods_modify_time_str,
            product_image = {"ProductID": product["ProductID"], "GoodsCode": product["GoodsCode"], "url": url,
                             "RecGuid": RecGuid, "ImageType": ImageType,
                             "ImageName": ImageName, "ImageGuid": ImageGuid,
                             "ImageFmt": ImageFmt, "IsDefault": IsDefault, "FileDate": CreateDate,
                             "EditDate": EditDate, "ImageFilePath": filepath, "ModuleID": ModuleID}
            # print("product_image", product_image)
            return product_image
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

    def write_product_image(self, domain_name, product):
        try:
            if domain_name == gl.pf_domain:
                product_image = self.generate_product_image(product, None)
                if product_image is not None:
                    self.download_file(product_image["url"], product_image["ImageFilePath"])
                    self.merge_product_image(product_image)
                else:
                    message = {"message": "产品:" + product["GoodsCode"] + " 主图为空，请检查网站"}
                    self.signal.emit({"message": message})
            elif domain_name == gl.ls_domain:
                prod_list = self.select_product_info(domain_name, product["GoodsCode"])
                if len(prod_list) > 0:
                    product_image = self.generate_product_image(product, None)
                    if product_image is not None:
                        self.download_file(product_image["url"], product_image["ImageFilePath"])
                        self.merge_product_image(product_image)
                    else:
                        message = {"message": "产品:" + product["GoodsCode"] + " 主图为空，请检查网站"}
                        self.signal.emit({"message": message})
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

    def merge_product_image(self, product_image):
        # print("download image", p)
        merge_result = True
        cnxn = pyodbc.connect(self._conn_str)
        cursor = cnxn.cursor()
        sql = "select * from Product_Image " \
              "where ProductID=(select top 1 ProductID from Product_Info where GoodsCode=?) and RecGuid=?"
        # print("ProductID", info["ProductID"])
        cursor.execute(sql, product_image["GoodsCode"], product_image["RecGuid"])
        record = cursor.fetchone()
        if record is None:
            print("读取图片", product_image["ImageFilePath"])
            try:
                FileDate = datetime.datetime.strptime(product_image["FileDate"], '%Y-%m-%d %H:%M:%S')
                EditDate = datetime.datetime.strptime(product_image["EditDate"], '%Y-%m-%d %H:%M:%S')
                file_size = int(os.path.getsize(product_image["ImageFilePath"]) / 1024)
                image = Image.open(product_image["ImageFilePath"], "r")
                image.thumbnail((320, 340))
                if image.mode in ("RGBA", "P"):
                    image = image.convert("RGB")
                # 先保存文件，再从文件读取到 data
                # filepath = os.path.normpath(os.path.join(self._disk_path, "temp.jpg"))
                # image.save(filepath)
                # f1 = open(filepath, "rb")
                # data = f1.read()
                # 直接保存io缓存,再从io缓存读取data
                buf = io.BytesIO()
                image.save(buf, format='JPEG')
                byte_im = buf.getvalue()
                sql = "delete from Product_Image " \
                      "where ProductID=(select top 1 ProductID from Product_Info where GoodsCode=?) and RecGuid=?"
                cursor.execute(sql, product_image["GoodsCode"], product_image["RecGuid"])
                cursor.commit()
                sql = "insert into Product_Image(ProductID,RecGuid,ImageType,ImageName,ImageGuid,ImageSize,ImageFmt," \
                      "IsDefault,FileDate,EditDate,ThumbImage,ModuleID) values(?,?,?,?,?,?,?,?,?,?,?,?)"
                cursor.execute(sql, product_image["ProductID"], product_image["RecGuid"],
                               product_image["ImageType"], product_image["ImageName"],
                               product_image["ImageGuid"], file_size, product_image["ImageFmt"],
                               product_image["IsDefault"], FileDate,
                               EditDate, (pyodbc.Binary(byte_im)), product_image["ModuleID"])
                # print(product_image)
                cursor.commit()
                # f1.close()
                merge_result = True
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
                merge_result = False
                # the end

        cursor.close()
        cnxn.close()
        return merge_result

    def select_product_info(self, domain_name, GoodsCode):
        try:
            prod_list = []
            # print(merge_product_info, info)
            cnxn = pyodbc.connect(self._conn_str)
            cursor = cnxn.cursor()
            # {'ProductID': 1243813, 'TypeID': 40716, 'GoodsCode': '778828', 'GoodsEName': 'LCD Silicone Laminating Mold For Samsung Galaxy S7 Edge S8 S8 Plus S9 S9 Plus', 'stock_nums': '119999988', 'ProductActive': '0', 'CreateDate': '2019-01-09 10:36:56', 'EditDate': '2020-08-18 09:47:21', 'image': 'http://us02-imgcdn.ymcart.com/32676/2020/08/17/b/6/b6251f1711a0422e.jpg', 'body_product_spec': {'GoodsCode': '778828', 'brand_id': '0', 'brand_name': '', 'goods_type_id': '570', 'category_name': 'Screen repair tools', 'price': '28.9300', 'weight': '0.2000', 'volume': '0.000000', 'spec_mode': '1', 'moq': '1', 'mxoq': '0'}}, {'ProductID': 1243812, 'TypeID': 40716, 'GoodsCode': '779023', 'GoodsEName': '9666 Liquid Clean Glue For Samsung Edge Lcd OCA Polarizer Film Glue Remove Liquid', 'stock_nums': '9999999', 'ProductActive': '0', 'CreateDate': '2019-01-09 12:02:23', 'EditDate': '2020-08-18 09:47:21', 'image': 'http://us02-imgcdn.ymcart.com/32676/2020/08/17/b/a/bacbc4963fffe6a0.jpg', 'body_product_spec': {'GoodsCode': '779023', 'brand_id': '51396', 'brand_name': 'Others', 'goods_type_id': '570', 'category_name': 'Screen repair tools', 'price': '67.2210', 'weight': '2.2000', 'volume': '0.000000', 'spec_mode': '0', 'moq': '1', 'mxoq': '0'}},
            
            if domain_name is None and GoodsCode is None:
                sql = "select ProductID, GoodsCode,GoodsEName,TypeID, Status, ProductActive,CreateDate,EditDate,DefaultImageID from Product_Info"
                cursor.execute(sql)
            elif GoodsCode is None:
                sql = "select a.ProductID, a.GoodsCode, a.GoodsEName,a.TypeID, a.Status, a.ProductActive,a.CreateDate, a.EditDate, a.DefaultImageID " \
                      "from Product_Info as a join [FTPart_Product_Info_property_1] as b" \
                      " on a.ProductID=b.[MainID] where b.[品牌.domain] = ?"
                cursor.execute(sql, domain_name)
            elif domain_name is None:
                sql = "select a.ProductID, a.GoodsCode, a.GoodsEName,a.TypeID, a.Status, a.ProductActive,a.CreateDate, a.EditDate, a.DefaultImageID " \
                      "from Product_Info as a where a.GoodsCode = ?"
                cursor.execute(sql, GoodsCode)
            else:
                sql = "select a.ProductID, a.GoodsCode, a.GoodsEName,a.TypeID, a.Status, a.ProductActive,a.CreateDate, a.EditDate, a.DefaultImageID " \
                      "from Product_Info as a join [FTPart_Product_Info_property_1] as b" \
                      " on a.ProductID=b.[MainID] where b.[品牌.domain] = ? and a.GoodsCode = ?"
                cursor.execute(sql, domain_name, GoodsCode)
            for row in cursor:
                ProductID = row.ProductID
                GoodsCode = row.GoodsCode
                GoodsEName = row.GoodsEName
                TypeID = row.TypeID
                Status = row.Status
                ProductActive = row.ProductActive
                CreateDate = row.CreateDate
                EditDate = row.EditDate
                DefaultImageID = row.DefaultImageID
                prod_list.append({"ProductID": ProductID, "GoodsCode": GoodsCode, "GoodsEName": GoodsEName, "TypeID": TypeID, "Status": Status, 
                                  "ProductActive": ProductActive, "CreateDate": CreateDate, "EditDate": EditDate, "DefaultImageID": DefaultImageID})
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
            print("--"*60)
        finally:
            return prod_list

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
                CreateDate = row[3]
                year = CreateDate.split('-')[0]
                month = CreateDate.split('-')[1]
                day = CreateDate.split('-')[2].split(" ")[0]
                ModuleID = row[4]
                file_path = os.path.normpath(
                    os.path.join(self._disk_path, str(year), str(month), str(ModuleID), row[2]))
                product["ImageFilePath"] = file_path
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

    def select_product_spec(self, product_info):
        try:
            prod_spec_list = []
            cnxn = pyodbc.connect(self._conn_str)
            cursor = cnxn.cursor()
            sql = "select ProductSpecID,GoodsSpec,OuterBulk,GrossWeight," \
                  "FOBPrice,MinOrder,Status,RecGuid,SpecActive,ProductID,SpecNo from Product_Spec where ProductID=?"
            cursor.execute(sql, int(product_info["ProductID"]))
            for row in cursor:
                ProductSpecID = row[0]
                GoodsSpec = row[1]
                OuterBulk = float(row[2])
                GrossWeight = float(row[3])
                FOBPrice = float(row[4])
                MinOrder = row[5]
                Status = row[6]
                RecGuid = row[7]
                SpecActive = row[8]
                ProductID = row[9]
                SpecNo = row[10]
                spec = {"ProductSpecID": ProductSpecID}
                spec["GoodsSpec"] = GoodsSpec
                spec["OuterBulk"] = OuterBulk
                spec["FOBPrice"] = FOBPrice
                spec["MinOrder"] = MinOrder
                spec["Status"] = Status
                spec["RecGuid"] = RecGuid
                spec["SpecActive"] = SpecActive
                spec["ProductID"] = ProductID
                spec["SpecNo"] = SpecNo
                prod_spec_list.append(spec)
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
            pass
        finally:
            return prod_spec_list        

    def merge_product_spec(self, domain_name, spec):
        try:
            # print(spec, spec["mxoq"])
            cnxn = pyodbc.connect(self._conn_str)
            cursor = cnxn.cursor()
            sql = "select ProductSpecID,GoodsSpec,OuterBulk,GrossWeight," \
                  "FOBPrice,MinOrder,Status,RecGuid,SpecActive,ProductID " \
                  "from Product_Spec " \
                  "where SpecNo=? and ProductID in (select ProductID from product_info where GoodsCode=?)"
            # print("ProductID", info["ProductID"])
            cursor.execute(sql, spec["SpecNo"], spec["GoodsCode"])
            row = cursor.fetchone()
            # print(record)
            if row is None:
                self.insert_product_spec(cursor, domain_name, spec)
                print("新增产品规格", spec["GoodsCode"], spec["SpecNo"], spec["ProductSpecID"])
            else:
                ProductSpecID = row[0]
                GoodsSpec = row[1]
                OuterBulk = float(row[2])
                GrossWeight = float(row[3])
                FOBPrice = float(row[4])
                MinOrder = row[5]
                Status = row[6]
                RecGuid = row[7]
                SpecActive = row[8]
                ProductID = row[9]
                if ProductSpecID != spec["ProductSpecID"] and ProductID == spec["ProductID"]:
                    sql = "delete from Product_Spec where ProductSpecID=? "
                    cursor.execute(sql, ProductSpecID)
                    cursor.commit()
                    # 更新 最大定购量
                    sql = "delete from [FTPart_Product_Spec_property_1] where [MainID]=?"
                    cursor.execute(sql, ProductSpecID)
                    cursor.commit()
                    self.insert_product_spec(cursor, domain_name, spec)
                    print("重置产品规格", spec["GoodsCode"], spec["SpecNo"], spec)
                else:
                    if domain_name == gl.pf_domain:
                        sql = "select [MainID], [品牌.最大起订量], [品牌.批发价] " \
                              "from [FTPart_Product_Spec_property_1] where [MainID]=?"
                        cursor.execute(sql, spec["ProductSpecID"])
                        row = cursor.fetchone()
                        if row is not None:
                            FOBPrice = float(row[2])
                        # print(row)
                        if GoodsSpec != spec["GoodsSpec"].replace('<br />', ' ') \
                                or OuterBulk != spec["OuterBulk"] \
                                or GrossWeight != spec["GrossWeight"] \
                                or FOBPrice != spec["FOBPrice"] \
                                or MinOrder != spec["MinOrder"] or SpecActive != '0' or RecGuid != spec["RecGuid"]:
                            if int(spec["stock_nums"]) == 0:
                                stock_SpecActive = '1'
                            else:
                                stock_SpecActive = '0'
                            sql = "update Product_Spec set SpecActive=?, GoodsSpec=?,OuterBulk=?,GrossWeight=?," \
                                  "MinOrder=?,RecGuid=? " \
                                  " where SpecNo=? and ProductID  in (select ProductID from product_info where GoodsCode=?)"
                            cursor.execute(sql, stock_SpecActive, spec["GoodsSpec"].replace('<br />', ' '),
                                           spec["OuterBulk"], spec["GrossWeight"],
                                           spec["MinOrder"], spec["RecGuid"], spec["SpecNo"],
                                           spec["GoodsCode"])
                            # print("更新", spec["SpecNo"], spec["ProductID"])
                            cursor.commit()
                            # 更新 最大定购量, 批发价
                            sql = "update [FTPart_Product_Spec_property_1] set [品牌.最大起订量]=?, [品牌.批发价]=?" \
                                  " where [MainID]=?"
                            cursor.execute(sql, spec["mxoq"], spec["FOBPrice"], ProductSpecID)
                            cursor.commit()
                        else:
                            pass
                    elif domain_name == gl.ls_domain:
                        if GoodsSpec != spec["GoodsSpec"].replace('<br />', ' ') \
                                or OuterBulk != spec["OuterBulk"] \
                                or GrossWeight != spec["GrossWeight"] \
                                or FOBPrice != spec["FOBPrice"] \
                                or MinOrder != spec["MinOrder"] or SpecActive != '0' or RecGuid != spec["RecGuid"]:
                            if int(spec["stock_nums"]) == 0:
                                stock_SpecActive = '1'
                            else:
                                stock_SpecActive = '0'
                            sql = "update Product_Spec set SpecActive=?, GoodsSpec=?,OuterBulk=?,GrossWeight=?," \
                                  "FOBPrice=?,MinOrder=?,RecGuid=? " \
                                  " where SpecNo=? and ProductID in (select ProductID from product_info where GoodsCode=?)"
                            cursor.execute(sql, stock_SpecActive, spec["GoodsSpec"].replace('<br />', ' '),
                                           spec["OuterBulk"], spec["GrossWeight"],
                                           spec["FOBPrice"], spec["MinOrder"], spec["RecGuid"], spec["SpecNo"],
                                           spec["GoodsCode"])
                            print("更新 零售价格", spec["SpecNo"], spec["ProductID"], spec["FOBPrice"])
                            cursor.commit()
                        else:
                            pass
                    #print("更新产品规格", spec["ProductID"], spec["SpecNo"], spec)
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

    def insert_product_spec(self, cursor, domain_name, spec):
        if domain_name == gl.pf_domain:
            pf_price = spec["FOBPrice"]
            ls_price = 0.0
        else:
            pf_price = 0.0
            ls_price = spec["FOBPrice"]
        sql = "set identity_insert Product_Spec on"
        cursor.execute(sql)
        sql = "insert into Product_Spec" \
              "(ProductSpecID,ProductID,SpecNo,GoodsSpec,OuterBulk,GrossWeight,FOBPrice,MinOrder,RecGuid,SpecActive," \
              "IsDefault,BarCode,PositionQty,NetWeight,PackageDesc,GoodsCDesc,GoodsEDesc,GoodsUnit,CostPrice," \
              "FoBMoneyKind,SupplyerId,SortID,SupplyerName,ProfitMargin,AutoBarCode,HSCode,Status,LineColor," \
              "SuppOpCode,SuppOpName,EditOpCode,EditOpName) " \
              "values(?,?,?,?,?,?,?,?,?,?," \
              "'','',0,0,'','','','',0,0,0,0,'',0,'0','','0',0,'delong', '梁德龙', 'delong', '梁德龙')"
        if int(spec["stock_nums"]) == 0:
            stock_SpecActive = '1'
        else:
            stock_SpecActive = '0'
        cursor.execute(sql, spec["ProductSpecID"], spec["ProductID"], spec["SpecNo"],
                       spec["GoodsSpec"].replace('<br />', ' '), spec["OuterBulk"], spec["GrossWeight"],
                       ls_price, spec["MinOrder"], spec["RecGuid"], stock_SpecActive)
        sql = "set identity_insert Product_Info off"
        cursor.execute(sql)
        cursor.commit()
        sql = "insert into [FTPart_Product_Spec_property_1]" \
              "([MainID], [ExtendID], [_SelfImageType], [_ImageID], [_LineColor], [品牌.最大起订量], [品牌.批发价]) " \
              "values(?,1,0,0,0,?,?)"
        cursor.execute(sql, spec["ProductSpecID"], spec["mxoq"], pf_price)
        # print("新增 最大定购量", spec["ProductID"], spec["SpecNo"], spec["ProductSpecID"])
        cursor.commit()

    def merge_Product_Material_Info(self, product, spec):
        try:
            cnxn = pyodbc.connect(self._conn_str)
            cursor = cnxn.cursor()
            sql = "select ProductID,SpecID,GoodsCode,SpecNo,TypeID,Status from Product_Material_Info " \
                  "where SpecNo=? and ProductID=?"
            cursor.execute(sql, spec["SpecNo"], spec["ProductID"])
            row = cursor.fetchone()
            # print(row)
            if row is None:
                sql = "insert into Product_Material_Info" \
                      "(ProductID,SpecID,GoodsCode,SpecNo,TypeID,Status) " \
                      "values(?,?,?,?,?,0)"
                cursor.execute(sql, spec["ProductID"], spec["ProductSpecID"], product["GoodsCode"], spec["SpecNo"],
                               product["TypeID"])
                cursor.commit()
            else:
                ProductID = row[0]
                SpecID = row[1]
                GoodsCode = row[2]
                SpecNo = row[3]
                TypeID = row[4]
                Status = row[5]
                if GoodsCode != product["GoodsCode"] or TypeID != product["TypeID"] \
                        or SpecID != spec["ProductSpecID"] or Status != spec["Status"]:
                    sql = "update Product_Material_Info set GoodsCode=?, SpecID=?,TypeID=?, status=0 " \
                          " where SpecNo=? and ProductID=?"
                    cursor.execute(sql, product["GoodsCode"], spec["ProductSpecID"], product["TypeID"],
                                   spec["SpecNo"], spec["ProductID"])
                    # print("更新 Product_Material_Info", spec["ProductID"], spec["SpecNo"])
                    cursor.commit()
                else:
                    pass
                    # print("不需要更新 Product_Material_Info", spec["ProductID"], spec["SpecNo"])
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

    def merge_product_single_spec_image(self, product_info):
        try:
            spec_mode = (product_info["body_product_spec"])["spec_mode"]
            GoodsCode = product_info["GoodsCode"]
            if spec_mode != "1":
                if len(product_info["product_spec"]) == 1:
                    product_spec = product_info["product_spec"][0]
                    RecGuid = product_spec["RecGuid"]
                else:
                    print("非多规格产品", product_info["GoodsCode"], "修改规格图失败")
                    return
            cnxn = pyodbc.connect(self._conn_str)
            cursor = cnxn.cursor()
            sql = "select * from Product_Image " \
                  " where ProductID=(select top 1 ProductID from Product_Info where GoodsCode=?) and RecGuid=?"
            # print(ProductID,RecGuid)
            # print("ProductID", info["ProductID"])
            cursor.execute(sql, GoodsCode, RecGuid)
            record = cursor.fetchone()
            # print(record)
            if record is None:
                sql = "insert into Product_Image(ProductID,RecGuid,ImageType,ImageName,ImageGuid,ImageSize,ImageFmt," \
                      "IsDefault,FileDate,EditDate,ThumbImage,ModuleID) " \
                      " select ProductID,'" + RecGuid + "' as RecGuid,ImageType,ImageName,ImageGuid,ImageSize,ImageFmt," \
                                                        "IsDefault,FileDate,EditDate,ThumbImage,ModuleID from Product_Image " \
                                                        "where ProductID=" \
                                                        "(select top 1 ProductID from Product_Info where GoodsCode=?) " \
                                                        "and RecGuid =''"
                # print(sql)
                cursor.execute(sql, GoodsCode)
                cursor.commit()
                print("新增单规格图成功:",product_info["GoodsCode"], product_info["image"])
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

    def offline_product_info(self, productID, domain_name):
        try:
            cnxn = pyodbc.connect(self._conn_str)
            cursor = cnxn.cursor()
            sql = "update Product_Info set ProductActive = '1' where ProductID=? " \
                  "and ProductID in (SELECT [MainID] FROM [FTPart_Product_Info_property_1] WHERE [品牌.domain] = ?)"
            cursor.execute(sql, productID, domain_name)
            cursor.commit()
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

    def offline_product_spec(self, productID, SpecNo):
        try:
            cnxn = pyodbc.connect(self._conn_str)
            cursor = cnxn.cursor()
            sql = "update Product_Spec set SpecActive = '1' where ProductID=? and SpecNo=?"
            cursor.execute(sql, productID, SpecNo)
            cursor.commit()
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

    def select_product_spec_image(self, ProductID, rowno):
        try:
            spec = None
            cnxn = pyodbc.connect(self._conn_str)
            cursor = cnxn.cursor()
            # ProductSpecID, GoodsSpec, OuterBulk, GrossWeight, FOBPrice, MinOrder, Status, RecGuid, SpecActive, ProductID, SpecNo
            sql = "select * from (select count(*) over() as cc, ROW_NUMBER()  Over (ORDER BY a.productspecid) as rowno," \
                  " a.ProductID ,a.SpecNo ,a.GoodsSpec, a.RecGUID,b.IMageName,b.ImageGUID," \
                  "CONVERT(varchar, b.FileDate, 120 ) as [FileDate], b.ThumbImage, a.specActive,a.status " \
                  "from product_spec  a join Product_Image   b on a.ProductID=b.ProductID and a.RecGUID=b.RecGUID " \
                  "where a.productid = ? ) as t where  rowno = ?"
            cursor.execute(sql, ProductID, rowno)
            row = cursor.fetchone()
            if row is not None:
                spec = dict()
                spec["cc"] = row[0]
                spec["rowno"] = row[1]
                spec["ProductID"] = row[2]
                spec["SpecNo"] = row[3]
                spec["GoodsSpec"] = row[4]
                spec["ImageGUID"] = row[7]
                spec["FileDate"] = row[8]
                spec["ThumbImage"] = row[9]
                spec["specActive"] = row[10]
                spec["status"] = row[11]
                CreateDate = row[8]
                year = CreateDate.split('-')[0]
                month = CreateDate.split('-')[1]
                day = CreateDate.split('-')[2].split(" ")[0]
                ModuleID = "501"
                file_path = os.path.normpath(
                    os.path.join(self._disk_path, str(year), str(month), str(ModuleID), spec["ImageGUID"]))
                spec["ImageFilePath"] = file_path
                cursor.close()
                cnxn.close()
            else:
                print("spec is none", ProductID)
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
            pass
        finally:
            return spec
