import pyodbc
import configparser
import datetime
import time
import io
import os
import hashlib
from PIL import Image
from pathlib import Path
import logging
import requests
import traceback, sys
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


class EtlDao(object):
    def __init__(self):
        super().__init__()
        self._domain_name = ""
        self._conn_str = ""
        self._disk_path = "/tmp"
        config = configparser.ConfigParser()
        init_file = os.path.normpath(os.path.join(os.curdir, "config", "ymcart.ini"))
        config.read(init_file)
        self._conn_str = config.get("db", "conn_str")
        self._disk_path = config.get("db", "disk_path")
        logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                            level=logging.DEBUG,
                            filename='etlshopyy.log',
                            filemode='a')
        self._domain_name = config.get("api","domain_name")

    def merge_product_type(self, type_list):
        try:
            # Insert into Product_Type(ProductTypeID,ParentID,TypeName,SortID) values()
            cnxn = pyodbc.connect(self._conn_str)
            cursor = cnxn.cursor()
            for prod_type in type_list:
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
                    print("新增", prod_type["TypeName"])
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
                        print("更新", prod_type["TypeName"])
                        cursor.commit()
                    else:
                        print("不需要更新", TypeName)
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

    def select_product_image(self, productID):
        try:
            cnxn = pyodbc.connect(self._conn_str)
            cursor = cnxn.cursor()
            sql = "SELECT top 1 [ProductID],[ImageName],[ImageGuid],CONVERT(varchar, FileDate, 120 ) as [FileDate]," \
                  "[ModuleID], [ThumbImage]" \
                  " FROM [Product_Image] " \
                  "where [ProductID]=? and [RecGuid]='' order by [FileDate] desc"
            cursor.execute(sql, productID)
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

    def select_product_spec_image(self, productID, rowno):
        try:
            cnxn = pyodbc.connect(self._conn_str)
            cursor = cnxn.cursor()
            sql = "select * from (select count(*) over() as cc, ROW_NUMBER()  Over (ORDER BY a.productspecid) as rowno," \
                  " a.ProductID ,a.SpecNo ,a.GoodsSpec, a.RecGUID,b.IMageName,b.ImageGUID," \
                  "CONVERT(varchar, b.FileDate, 120 ) as [FileDate], b.ThumbImage, a.specActive,a.status " \
                  "from product_spec  a join Product_Image   b on a.ProductID=b.ProductID and a.RecGUID=b.RecGUID " \
                  "where a.productid = ? ) as t where  rowno = ?"
            sql_bk2 = "select * from (select count(*) over() as cc, ROW_NUMBER()  Over (ORDER BY a.productspecid) as rowno, a.ProductID ,a.SpecNo ,a.GoodsSpec, a.RecGUID,b.IMageName,b.ImageGUID,CONVERT(varchar, b.FileDate, 120 ) as [FileDate], b.ThumbImage, a.specActive,a.status from product_spec  a left join ( select * from (select pi.*,MAX(filedate) over(partition by RecGuid) max_filedate from FTTXRUN.csidbo.Product_Image pi where ProductID=?) a where FileDate = max_filedate)   b on a.ProductID=b.ProductID and a.RecGUID=b.RecGUID where a.productid = ?) as t where  rowno = ?"
            cursor.execute(sql, productID, productID, rowno)
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
                return spec
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

    def select_product_info(self, domain_name):
        prod_list = []
        try:
            # print(merge_product_info, info)
            cnxn = pyodbc.connect(self._conn_str)
            cursor = cnxn.cursor()
            if domain_name is None or domain_name == "":
                sql = "select ProductID, Status, ProductActive from Product_Info"
            else:
                sql = "select a.ProductID, a.Status, ProductActive " \
                      "from Product_Info as a join [FTPart_Product_Info_property_1] as b" \
                      " on a.ProductID=b.[MainID] where b.[品牌.domain] = ?"
            cursor.execute(sql, domain_name)
            for row in cursor:
                product_id = row.ProductID
                status = row.Status
                ProductActive = row.ProductActive
                prod_list.append({"ProductID": product_id, "Status": status, "ProductActive": ProductActive})
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
        return prod_list

    def offline_product_info(self, productID):
        try:
            cnxn = pyodbc.connect(self._conn_str)
            cursor = cnxn.cursor()
            sql = "update Product_Info set ProductActive = '1' where ProductID=? " \
                  "and ProductID in (SELECT [MainID] FROM [FTPart_Product_Info_property_1] WHERE [品牌.domain] = ?)"
            cursor.execute(sql, productID, self._domain_name)
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

    def select_product_spec(self, product):
        prod_spec_list = []
        try:
            print("ProductID", product["ProductID"])
            cnxn = pyodbc.connect(self._conn_str)
            cursor = cnxn.cursor()
            sql = "select ProductSpecID, ProductID, SpecNo, Status from Product_Spec where ProductID=?"
            cursor.execute(sql, int(product["ProductID"]))
            for row in cursor:
                ProductSpecID = row[0]
                ProductID = row[1]
                SpecNo = row[2]
                Status = row[3]
                prod_spec_list.append(
                    {"ProductSpecID": ProductSpecID, "ProductID": ProductID, "SpecNo": SpecNo, "Status": Status})
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
        return prod_spec_list

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

    def merge_product_info(self, info):
        try:
            # print(merge_product_info, info)
            cnxn = pyodbc.connect(self._conn_str)
            cursor = cnxn.cursor()
            sql = "select TypeID,GoodsCode, GoodsEName,CONVERT(varchar, CreateDate, 120 ) as CreateDate," \
                  "CONVERT(varchar, EditDate, 120 ) as EditDate, Status, ProductActive from Product_Info where ProductID=?"
            # print("ProductID", info["ProductID"])
            cursor.execute(sql, info["ProductID"])
            row = cursor.fetchone()
            if row is None:
                sql = "set identity_insert Product_Info on"
                cursor.execute(sql)
                sql = "Insert into Product_Info(ProductID, TypeID, GoodsCode, GoodsEName, CreateDate, EditDate," \
                      "SchemeID,ShopTypeID,HSCode,GoodsCName,CustGoodsCode,GoodsMemo,ImageNum,IsAutoCode," \
                      "ProductCustID, ProductCustName,ProductActive,Status,EditNum,OpCode,OpName, EditOpCode, EditOpName)" \
                      " values(?,?,?,?,?,?,0,0,'','','','',1,'',0,'','0','0',1,'delong','梁德龙','delong','梁德龙')"
                # print(info)
                # print(sql)
                # cursor.execute(sql, info["ProductID"], info["TypeID"], info["GoodsCode"],
                # info["GoodsEName"], info["CreateDate"], info["EditDate"]),
                # datetime.strptime(info["CreateDate"], '%y-%m-%d %H:%M:%S').fromtimestamp(0)
                cursor.execute(sql, info["ProductID"], info["TypeID"], info["GoodsCode"], info["GoodsEName"],
                               datetime.datetime.strptime(info["CreateDate"], '%Y-%m-%d %H:%M:%S'),
                               datetime.datetime.strptime(info["EditDate"], '%Y-%m-%d %H:%M:%S'))
                print("新增", info["GoodsEName"])
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
                        or CreateDate != info["CreateDate"] or EditDate != info["EditDate"] or ProductActive != '0':
                    # print("更新", info["CreateDate"], info["EditDate"])
                    sql = "update Product_Info set ProductActive='0', TypeID=?, GoodsCode=?, GoodsEName=?, CreateDate=?, EditDate=? " \
                          "where ProductID=?"
                    cursor.execute(sql, info["TypeID"], info["GoodsCode"], info["GoodsEName"],
                                   datetime.datetime.strptime(info["CreateDate"], '%Y-%m-%d %H:%M:%S'),
                                   datetime.datetime.strptime(info["EditDate"], '%Y-%m-%d %H:%M:%S'), info["ProductID"])
                    print("更新", info["GoodsEName"])
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
            if "45915.us01.ymcart.com" in self._domain_name:
                product_source = "批发"
            elif "32676.us01.ymcart.com" in self._domain_name:
                product_source = "临售"
            if record is None:
                sql = "insert into [FTPart_Product_Info_property_1]" \
                      "([MainID], [ExtendID], [_SelfImageType], [_ImageID], [_LineColor],[_PrintNum]," \
                      "[_FaxNum], [_EmailNum], [_CheckResult], [品牌.商品品牌], [品牌.domain],[品牌.来源]) " \
                      "values(?,1,0,0,0,0,0,0,0,?,?,?)"
                cursor.execute(sql, info["ProductID"], body_product_spec["brand_name"], self._domain_name, product_source)
                print("新增 品牌.商品品牌,domain,来源", info["ProductID"])
                cursor.commit()
            else:
                brand_name = record[0]
                domain_name = record[1]
                product_source_name = record[2]
                if brand_name != body_product_spec["brand_name"]:
                    sql = "update [FTPart_Product_Info_property_1] set [品牌.商品品牌]=? " \
                          "where [MainID]=? "
                    cursor.execute(sql, body_product_spec["brand_name"], info["ProductID"])
                    print("更新 品牌.商品品牌", info["ProductID"])
                    cursor.commit()
                else:
                    pass
                if domain_name != self._domain_name:
                    print("#"*100)
                    print("商品", info["ProductID"], "在不同域名重复，请核查")
                    print("#"*100)
                    sql = "update [FTPart_Product_Info_property_1] set [品牌.domain]=? " \
                          "where [MainID]=? "
                    cursor.execute(sql, self._domain_name, info["ProductID"])
                    print("更新 品牌.domain", info["ProductID"])
                    cursor.commit()
                else:
                    pass
                    # print("不需要更新 品牌.商品品牌", info["ProductID"])
                if record[2] != product_source:
                    sql = "update [FTPart_Product_Info_property_1] set [品牌.来源]=? " \
                          "where [MainID]=? "
                    cursor.execute(sql, product_source, info["ProductID"])
                    print("更新 品牌.来源", info["ProductID"])
                    cursor.commit()
                else:
                    pass
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

    def merge_product_spec(self, spec):
        try:
            # print(spec, spec["mxoq"])
            cnxn = pyodbc.connect(self._conn_str)
            cursor = cnxn.cursor()
            sql = "select ProductSpecID,GoodsSpec,OuterBulk,GrossWeight,FOBPrice,MinOrder,Status,RecGuid,SpecActive " \
                  "from Product_Spec where SpecNo=? and ProductID=?"
            # print("ProductID", info["ProductID"])
            cursor.execute(sql, spec["SpecNo"], spec["ProductID"])
            row = cursor.fetchone()
            # print(record)
            logging.info("product_spec:" + spec["sku_value"])
            if row is None:
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
                               spec["FOBPrice"], spec["MinOrder"], spec["RecGuid"], stock_SpecActive)
                # print("新增", spec["ProductID"], spec["SpecNo"], spec["ProductSpecID"])
                sql = "set identity_insert Product_Info off"
                cursor.execute(sql)
                cursor.commit()
                sql = "insert into [FTPart_Product_Spec_property_1]" \
                      "([MainID], [ExtendID], [_SelfImageType], [_ImageID], [_LineColor], [品牌.最大起订量]) " \
                      "values(?,1,0,0,0,?)"
                cursor.execute(sql, spec["ProductSpecID"], spec["mxoq"])
                # print("新增 最大定购量", spec["ProductID"], spec["SpecNo"], spec["ProductSpecID"])
                cursor.commit()
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
                # print(record)
                if ProductSpecID != spec["ProductSpecID"]:
                    sql = "set identity_insert Product_Spec on"
                    cursor.execute(sql)
                    sql = "delete from Product_Spec where ProductSpecID=? "
                    cursor.execute(sql, ProductSpecID)
                    cursor.commit()
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
                                   spec["FOBPrice"], spec["MinOrder"], spec["RecGuid"], stock_SpecActive)
                    # print("更新 ProductSpecID", spec["ProductID"], spec["SpecNo"], spec["ProductSpecID"])
                    sql = "set identity_insert Product_Spec off"
                    cursor.execute(sql)
                    cursor.commit()
                    # 更新 最大定购量
                    sql = "delete from [FTPart_Product_Spec_property_1] where [MainID]=?"
                    cursor.execute(sql, ProductSpecID)
                    cursor.commit()
                    sql = "insert into [FTPart_Product_Spec_property_1]" \
                          "([MainID], [ExtendID], [_SelfImageType], [_ImageID], [_LineColor], [品牌.最大起订量]) " \
                          "values(?,1,0,0,0,?)"
                    cursor.execute(sql, spec["ProductSpecID"], spec["mxoq"])
                    cursor.commit()
                    # print("更新ProductSpecID 最大定购量", spec["ProductID"], spec["SpecNo"])
                else:
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
                              " where SpecNo=? and ProductID=?"
                        cursor.execute(sql, stock_SpecActive, spec["GoodsSpec"].replace('<br />', ' '),
                                       spec["OuterBulk"], spec["GrossWeight"],
                                       spec["FOBPrice"], spec["MinOrder"], spec["RecGuid"], spec["SpecNo"],
                                       spec["ProductID"])
                        # print("更新", spec["SpecNo"], spec["ProductID"])
                        cursor.commit()
                    else:
                        pass
                        # print("不需要更新", spec["ProductID"], spec["SpecNo"], spec["ProductSpecID"])
                    # 更新 最大定购量
                    # sql = "update [FTPart_Product_Spec_property_1] set [品牌.最大起订量]=? where [MainID]=?"
                    # cursor.execute(sql, spec["mxoq"], spec["ProductSpecID"])
                    # cursor.commit()
                    # print("更新 最大定购量", spec["ProductID"], spec["SpecNo"])
                    # 更新 最大定购量
                    sql = "delete from [FTPart_Product_Spec_property_1] where [MainID]=?"
                    cursor.execute(sql, ProductSpecID)
                    cursor.commit()
                    sql = "insert into [FTPart_Product_Spec_property_1]" \
                          "([MainID], [ExtendID], [_SelfImageType], [_ImageID], [_LineColor], [品牌.最大起订量]) " \
                          "values(?,1,0,0,0,?)"
                    cursor.execute(sql, spec["ProductSpecID"], spec["mxoq"])
                    cursor.commit()
                    # print("更新ProductSpecID 最大定购量", spec["ProductID"], spec["SpecNo"])
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

    def merge_Product_Material_Info(self, spec, product):
        try:
            cnxn = pyodbc.connect(self._conn_str)
            cursor = cnxn.cursor()
            sql = "select ProductID,SpecID,GoodsCode,SpecNo,TypeID,Status from Product_Material_Info " \
                  "where SpecNo=? and ProductID=?"
            cursor.execute(sql, spec["SpecNo"], spec["ProductID"])
            row = cursor.fetchone()
            # print(row)
            logging.info("product_spec:" + str(spec["ProductID"]) + ":" + str(spec["SpecNo"]))
            if row is None:
                sql = "insert into Product_Material_Info" \
                      "(ProductID,SpecID,GoodsCode,SpecNo,TypeID,Status) " \
                      "values(?,?,?,?,?,0)"
                cursor.execute(sql, spec["ProductID"], spec["ProductSpecID"], product["GoodsCode"], spec["SpecNo"],
                               product["TypeID"])
                # print("新增 Product_Material_Info", spec["ProductID"], spec["SpecNo"])
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

    def download_file_1(self, url, filepath):
        begTime = time.time()
        resp = requests.get(url)
        with open(filepath, 'wb') as f:
            f.write(resp.content)
        endTime = time.time()
        print("下载完成：", endTime - begTime)

    def download_file(self, url, filepath):
        begTime = time.time()
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(filepath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    # If you have chunk encoded response uncomment if
                    # and set chunk_size parameter to None.
                    # if chunk:
                    f.write(chunk)
                    # the end download to disk.
        endTime = time.time()
        print("下载完成：", endTime - begTime)

    def download_product_image(self, product, spec_image, sync_type):
        try:
            if spec_image is None:
                url = product["image"]
                if url is None:
                    print("产品:" + str(product["ProductID"]) + " image is null")
                    return None
                RecGuid = ''
                CreateDate = product["CreateDate"]
                EditDate = product["EditDate"]
            else:
                url = spec_image['image']
                if url is None:
                    print("产品:" + str(product["ProductID"]) + " 的规格 image is null")
                    return None
                RecGuid = spec_image["RecGuid"]
                CreateDate = spec_image["SysNoTime"]
                EditDate = spec_image["LastEditTime"]
            # print(product["image"])
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
            if not os.path.exists(filepath) or sync_type is not None:
                # print("sync_type", sync_type)
                # NOTE the stream=True parameter below
                if sync_type is None:
                    print(product["ProductID"], "正在下载", filepath)
                else:
                    print(product["ProductID"], "重新下载", filepath)
                self.download_file(url, filepath)
                #
            IsDefault = '1'
            # print("image url", url)
            # Product_Image(ProductID,RecGuid,ImageType,ImageName,ImageGuid,ImageSize,ImageFmt,IsDefault,
            # FileDate,EditDate,ThumbImage,ModuleID)
            #  "CreateDate": goods_create_time_str, "EditDate": goods_modify_time_str,
            Product_Image = {"ProductID": product["ProductID"], "RecGuid": RecGuid, "ImageType": ImageType,
                             "ImageName": ImageName, "ImageGuid": ImageGuid,
                             "ImageFmt": ImageFmt, "IsDefault": IsDefault, "FileDate": CreateDate,
                             "EditDate": EditDate, "ImageFilePath": filepath, "ModuleID": ModuleID}
            # print("Product_Image", Product_Image)
            return Product_Image
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

    def merge_product_image(self, product, spec_image, sync_type):
        try:
            p = self.download_product_image(product, spec_image, sync_type)
            # print("download image", p)
            if p is not None:
                cnxn = pyodbc.connect(self._conn_str)
                cursor = cnxn.cursor()
                sql = "select * from Product_Image where ProductID=? and RecGuid=?"
                # print("ProductID", info["ProductID"])
                cursor.execute(sql, p["ProductID"], p["RecGuid"])
                record = cursor.fetchone()
                if record is None:
                    print("读取图片：", p["ImageFilePath"])
                    try:
                        FileDate = datetime.datetime.strptime(p["FileDate"], '%Y-%m-%d %H:%M:%S')
                        EditDate = datetime.datetime.strptime(p["EditDate"], '%Y-%m-%d %H:%M:%S')
                        file_size = int(os.path.getsize(p["ImageFilePath"]) / 1024)
                        image = Image.open(p["ImageFilePath"], "r")
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
                        sql = "delete from Product_Image where ProductID=? and RecGuid=?"
                        cursor.execute(sql, p["ProductID"], p["RecGuid"])
                        cursor.commit()
                        sql = "insert into Product_Image(ProductID,RecGuid,ImageType,ImageName,ImageGuid,ImageSize,ImageFmt," \
                              "IsDefault,FileDate,EditDate,ThumbImage,ModuleID) values(?,?,?,?,?,?,?,?,?,?,?,?)"
                        cursor.execute(sql, p["ProductID"], p["RecGuid"], p["ImageType"], p["ImageName"],
                                       p["ImageGuid"], file_size, p["ImageFmt"], p["IsDefault"], FileDate,
                                       EditDate, (pyodbc.Binary(byte_im)), p["ModuleID"])
                        print(p)
                        cursor.commit()
                        # f1.close()
                        print("新增图片成功:", product["image"])
                    except Exception as e:
                        print("新增图片失败", e)
                else:
                    pass
                    # print("图片已经保存:", product["image"])
                cursor.close()
                cnxn.close()
            else:
                if spec_image is None:
                    print("产品主图下载失败", product, product["image"])
                else:
                    print("规格图下载失败", product, spec_image["image"])
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

    def update_product_default_image(self, productID):
        try:
            cnxn = pyodbc.connect(self._conn_str)
            cursor = cnxn.cursor()
            sql = "delete from product_image " \
                  "where recguid='' and productid=? and " \
                  "productimageid not in (select MAX(productimageid) from [product_image] where recguid='' and productid=?)"
            cursor.execute(sql, productID, productID)
            cursor.commit()
            sql = "update product_info " \
                  " set defaultimageid=(select max(productimageid) from product_image" \
                  " where product_image.productid=? and recguid='') " \
                  "where productid=? and defaultimageid != (select max(productimageid) from product_image " \
                  "where product_image.productid=? and recguid='')"
            cursor.execute(sql, productID, productID, productID)
            cursor.commit()
            sql = " update [FTPart_Product_Info_property_1]  set [_ImageID]=" \
                  "(select max(productimageid) from product_image where product_image.productid=? and recguid='') " \
                  " where [MainID]=? and [_ImageID] != (select max(productimageid) from product_image " \
                  "where product_image.productid=? and recguid='')"
            cursor.execute(sql, productID, productID, productID)
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

    def merge_product_single_spec_image(self, product_info):
        try:
            spec_mode = (product_info["body_product_spec"])["spec_mode"]
            ProductID = product_info["ProductID"]
            if spec_mode != "1":
                if len(product_info["product_spec"]) == 1:
                    product_spec = product_info["product_spec"][0]
                    RecGuid = product_spec["RecGuid"]
                else:
                    print("非多规格产品", product_info["ProductID"], "修改规格图失败")
                    return
            cnxn = pyodbc.connect(self._conn_str)
            cursor = cnxn.cursor()
            sql = "select * from Product_Image where ProductID=? and RecGuid=?"
            # print(ProductID,RecGuid)
            # print("ProductID", info["ProductID"])
            cursor.execute(sql, ProductID, RecGuid)
            record = cursor.fetchone()
            # print(record)
            if record is None:
                sql = "insert into Product_Image(ProductID,RecGuid,ImageType,ImageName,ImageGuid,ImageSize,ImageFmt," \
                      "IsDefault,FileDate,EditDate,ThumbImage,ModuleID) " \
                      " select ProductID,'" + RecGuid + "' as RecGuid,ImageType,ImageName,ImageGuid,ImageSize,ImageFmt," \
                                                        "IsDefault,FileDate,EditDate,ThumbImage,ModuleID from Product_Image " \
                                                        "where ProductID=? and RecGuid =''"
                # print(sql)
                cursor.execute(sql, ProductID)
                cursor.commit()
                print("新增单规格图片成功:", product_info["image"])
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

    def download_image(self, url):
        try:
            local_filename = url.split('/')[-1]
            # NOTE the stream=True parameter below
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(local_filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        # If you have chunk encoded response uncomment if
                        # and set chunk_size parameter to None.
                        # if chunk:
                        f.write(chunk)
            return local_filename
        except requests.RequestException:
            return ""

    def save_image(self, imgname):
        try:
            # 读取图片，二进制格式，注意是rb
            f1 = open(imgname, "rb", )
            data = f1.read()
            # data = urllib2.urlopen(url).read()
            cnxn = pyodbc.connect(self._conn_str)
            cursor = cnxn.cursor()
            sql = "INSERT INTO testing(myimage) VALUES(?)"
            cursor.execute(sql, (pyodbc.Binary(data),))
            cursor.commit()
            cursor.close()
            cnxn.close()
            f1.close()
            print("保存成功:" + imgname)
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

    def read_image(self):
        try:
            # 读取图片，二进制格式，注意是rb
            # data = urllib2.urlopen(url).read()
            cnxn = pyodbc.connect(self._conn_str)
            cursor = cnxn.cursor()
            cursor.execute("select  * from testing")
            for row in cursor:
                data = row.myimage  # 对应数据库中的photo字段
                img_id = row.id
                image = Image.open(io.BytesIO(data))
                path = "photo" + str(img_id) + ".png"
                image.save(path)
                print('done')
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
