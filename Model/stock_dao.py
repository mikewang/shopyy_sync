# -*- coding: utf-8 -*-
import configparser
import traceback
import sys
import os
import pyodbc
import datetime
import base64
from Model.user import UserInfo
from Model.product import ProductInfo, ProductEnquiryPrice


class StockDao(object):

    def __init__(self):
        super(StockDao, self).__init__()
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

    def select_stock_product_list(self, page_no, filter_stock):
        try:
            product_list = []
            cnxn = pyodbc.connect(self._conn_str)
            cursor = cnxn.cursor()
            topN = " top " + str(page_no*10)
            # 采购人	StockProductID	ProductID	SignDate	GoodsCode	SpecNo	GoodsSpec	GoodsUnit	_ImageID	ImageGuid	ImageFmt	ModuleID	FileDate	ThumbImage	其它.供应商名称	其它.允采购量	其它.应采购价	其它.商品品牌
            # 数据源
            v_sql = "select " + topN + " "
            v_sql = v_sql + "e.[采购人], a.StockProductID,a.ProductID,CONVERT(varchar, d.SignDate, 120 ) as SignDate," \
                            "a.GoodsCode,a.SpecNo,f.GoodsCDesc, a.GoodsUnit, b._ImageID,c.ImageGuid,c.ImageFmt," \
                            "c.ModuleID,CONVERT(varchar, c.FileDate, 120 ) as FileDate,c.ThumbImage,b.[其它.供应商名称]," \
                            "b.[其它.允采购量],b.[其它.应采购价],b.[其它.商品品牌], " \
                            "coalesce(g.ordernum,0) as ordernum, coalesce(h.id,0) as priceEnquiredID  " \
                            "FROM [csidbo].[Stock_Product_Info] as a " \
                            "join  csidbo.FTPart_Stock_Product_Property_1 as b on a.StockProductID=b.MainID " \
                            "join csidbo.Product_Image as c on b._ImageID=c.ProductImageID " \
                            "join csidbo.stock_info d on d.ID=a.StockID " \
                            "join csidbo.[FTPart_Stock_Property_1] e on e.[MainID] = d.ID " \
                            "left join csidbo.[Stock_Product_Info_Desc] f on a.StockProductID=f.StockProductID " \
                            "left join (select [StockProductID], sum([OrderNum]*[OrderStat]) as ordernum from [csidbo].[Stock_Product_Order_App] group by [StockProductID]) g on a.StockProductID=g.StockProductID  " \
                            "left join (select max(id) as id, StockProductID from csidbo.[Stock_Product_EnquiryPrice_App] group by StockProductID ) h on  a.StockProductID=h.StockProductID "
            v_sql = v_sql + "  where b.[其它.允采购量] > coalesce(g.ordernum,0) "

            filter_brand = filter_stock["brand"]
            if filter_brand is not None:
                filter_sql = ''
                for b in filter_brand:
                    filter_sql = filter_sql + "'" + b + "',"
                filter_sql = filter_sql.rstrip(',')
                v_sql = v_sql + " and b.[其它.商品品牌] in (" + filter_sql + ")"
            filter_enquriy = filter_stock["enquiry"]
            if filter_enquriy is not None:
                if filter_enquriy == '未询价':
                    v_sql = v_sql + " and  coalesce(h.id,0) = 0 "
                elif filter_enquriy == '已询价':
                    v_sql = v_sql + " and  coalesce(h.id,0) > 0 "
            filter_begin = filter_stock["begin"]
            if filter_begin is not None:
                v_sql = v_sql + " and d.SignDate >= '" + filter_begin + "'"
            filter_end = filter_stock["end"]
            if filter_end is not None:
                v_sql = v_sql + " and d.SignDate <= '" + filter_end + " 23:59:59'"
            v_sql = v_sql + " order by d.signdate desc,a.stockproductid desc"
            v_sql = "select  top 10 * from (" + v_sql + " ) as v1 order by v1.SignDate asc,v1.StockProductID asc"

            print("select_stock_product_list sql is ", v_sql)
            cursor.execute(v_sql)
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
                product.orderNum = row[18]
                product.priceEnquiredID = row[19]
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

    def add_stock_product_enquiry_price(self, prod_dict_list):
        try:
            cnxn = pyodbc.connect(self._conn_str)
            cursor = cnxn.cursor()
            # {\"stockProductID\":10705,\"ID\":0,\"opCode\":\"delong\",\"createTime\":\"2020-11-23 14:21:54\"
            for prod in prod_dict_list:
                print("enquiried product is ", prod["stockProductID"], prod)
                stockProductID = prod["stockProductID"]
                opCode = prod["opCode"]
                sql = "insert into Stock_Product_EnquiryPrice_App(stockProductID,opCode) values(?,?)"
                cursor.execute(sql, stockProductID, opCode)
                cursor.commit()
            cursor.close
            cnxn.close
            return "1"
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

    def select_order_product_list(self, page_no, filter_stock, ptype):
        # 检索 所有的 订货商品
        try:
            product_list = []
            cnxn = pyodbc.connect(self._conn_str)
            cursor = cnxn.cursor()
            topN = " top " + str(page_no * 10)
            # 采购人	StockProductID	ProductID	SignDate	GoodsCode	SpecNo	GoodsSpec	GoodsUnit	_ImageID	ImageGuid	ImageFmt	ModuleID	FileDate	ThumbImage	其它.供应商名称	其它.允采购量	其它.应采购价	其它.商品品牌
            # 数据源
            v_sql = "select " + topN + " "
            v_sql = v_sql + "e.[采购人], a.StockProductID,a.ProductID,CONVERT(varchar, d.SignDate, 120 ) as SignDate," \
                            "a.GoodsCode,a.SpecNo,f.GoodsCDesc, a.GoodsUnit, b._ImageID,c.ImageGuid,c.ImageFmt," \
                            "c.ModuleID,CONVERT(varchar, c.FileDate, 120 ) as FileDate,c.ThumbImage,g.supplier as supplier," \
                            "b.[其它.允采购量],b.[其它.应采购价],b.[其它.商品品牌],coalesce(g.[OrderNum]*g.[OrderStat],0) as ordernum," \
                            "g.orderprice, g.orderStat, g.settlement,g.opcode as order_opcode, g.orderID, " \
                            "coalesce(h.id,0) as priceEnquiredID, CONVERT(varchar, g.CreateTime, 120 ) as CreateTime," \
                            "g.sourceOrderID, CONVERT(varchar, g.ensureTime, 120 ) as ensureTime, g.ensureOpCode, " \
                            "CONVERT(varchar, g.receiveGoodsTime, 120 ) as receiveGoodsTime, g.receiveOpCode " \
                            "FROM [csidbo].[Stock_Product_Info] as a " \
                            "join  csidbo.FTPart_Stock_Product_Property_1 as b on a.StockProductID=b.MainID " \
                            "join csidbo.Product_Image as c on b._ImageID=c.ProductImageID " \
                            "join csidbo.stock_info d on d.ID=a.StockID " \
                            "join csidbo.[FTPart_Stock_Property_1] e on e.[MainID] = d.ID " \
                            "left join csidbo.[Stock_Product_Info_Desc] f on a.StockProductID=f.StockProductID " \
                            "join [csidbo].[Stock_Product_Order_App] as g on a.StockProductID=g.StockProductID " \
                            "left join (select max(id) as id, StockProductID from csidbo.[Stock_Product_EnquiryPrice_App] group by StockProductID ) h on  a.StockProductID=h.StockProductID  "
            if ptype == "order":
                #去掉订货，订货，订货完成三个状态的查询
                v_sql = v_sql + "  where 1=1 and g.settlement <=1 "
            elif ptype == "receive":
                # 收货， 退货 两个状态的查询
                v_sql = v_sql + "  where 1=1 and g.settlement >1 "
            else:
                v_sql = v_sql + "  where 1=1 "

            filter_brand = filter_stock["brand"]
            if filter_brand is not None:
                filter_sql = ''
                for b in filter_brand:
                    filter_sql = filter_sql + "'" + b + "',"
                filter_sql = filter_sql.rstrip(',')
                v_sql = v_sql + " and b.[其它.商品品牌] in (" + filter_sql + ")"
            filter_enquriy = filter_stock["enquiry"]
            if filter_enquriy == '未询价':
                v_sql = v_sql + " and  coalesce(h.id,0) = 0 "
            elif filter_enquriy == '已询价':
                v_sql = v_sql + " and  coalesce(h.id,0) > 0 "
            filter_begin = filter_stock["begin"]
            if filter_begin is not None:
                v_sql = v_sql + " and g.CreateTime >= '" + filter_begin + "'"
            filter_end = filter_stock["end"]
            if filter_end is not None:
                v_sql = v_sql + " and g.CreateTime <= '" + filter_end + " 23:59:59'"
            filter_supplier = filter_stock["supplier"]
            if filter_supplier is not None:
                filter_sql = ''
                for b in filter_supplier:
                    filter_sql = filter_sql + "'" + b + "',"
                filter_sql = filter_sql.rstrip(',')
                v_sql = v_sql + " and g.supplier in (" + filter_sql + ")"
            v_sql = v_sql + " order by g.CreateTime desc,a.stockproductid desc, g.orderID desc"
            sql = "select  top 10 * from (" + v_sql + " ) as v1 order by v1.CreateTime asc,v1.StockProductID asc, v1.order_id asc"
            print("sql is ", sql)
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
                product.orderNum = row[18]
                product.orderPrice = row[19]
                # orderStat = 1, 订货， -1 ，退货，但退货记录要保存。
                product.orderStat = row[20]
                # settlement = 1， 确认订货成功，并没有现实收货，0，默认值，未确认订货成功。
                product.settlement = row[21]
                product.orderOpCode = row[21]
                product.orderID = row[23]
                product.priceEnquiredID = row[24]
                product.createTime = row[25]
                product.sourceOrderID = row[26]
                product.ensureTime = row[27]
                product.ensureOpCode = row[28]
                product.receiveGoodsTime = row[29]
                product.receiveOpCode = row[30]

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

    def add_stock_product_order(self, prod_dict_list):
        try:
            cnxn = pyodbc.connect(self._conn_str)
            cursor = cnxn.cursor()
            for prod in prod_dict_list:
                print("enquiried product is ", prod["stockProductID"], prod)
                stockProductID = prod["stockProductID"]
                opCode = prod["opCode"]
                purchaseNum = prod["purchaseNum"]
                purchasePrice = prod["purchasePrice"]
                orderStat = prod["orderStat"]
                supplier = prod["supplier"]
                settlement = prod["settlement"]
                sql = "insert into Stock_Product_Order_App(stockProductID,opCode, OrderNum, OrderPrice,orderStat," \
                      "supplier, settlement) " \
                      " values(?,?,?,?,?,?,?,0)"
                print("insert Stock_Product_Order_App sql is ", sql)
                cursor.execute(sql, stockProductID, opCode, purchaseNum, purchasePrice, orderStat, supplier, settlement)
                myTableId = cursor.fetchone()[0]
                print("Stock_Product_Order_App id is ", myTableId)
                cursor.commit()
            cursor.close
            cnxn.close
            return "1"
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

    def update_stock_product_order(self, prod_dict_list, operate_type):
        try:
            cnxn = pyodbc.connect(self._conn_str)
            cursor = cnxn.cursor()
            for prod in prod_dict_list:
                print("order product is ", prod["id"], prod["stockProductID"], prod)
                id = prod["id"]
                stockProductID = prod["stockProductID"]
                opCode = prod["opCode"]
                if operate_type == "cancel":
                    sql = "update Stock_Product_Order_App " \
                          "set  orderStat=-1 , opCode = ?" \
                          "where id = ? and stockProductID = ? and orderStat != -1"
                    print("update Stock_Product_Order_App sql is ", sql)
                    cursor.execute(sql, opCode, id, stockProductID)
                elif operate_type == "complete":
                    purchaseNum = prod["purchaseNum"]
                    purchasePrice = prod["purchasePrice"]
                    # 订货 或者 退货
                    orderStat = prod["orderStat"]
                    supplier = prod["supplier"]
                    settlement = prod["settlement"]
                    sql = "update Stock_Product_Order_App " \
                          "set opCode = ?, OrderNum = ? , OrderPrice=?, supplier=? , settlement=1 " \
                          "where id = ? and stockProductID = ? and settlement <> 1 "
                    print("update Stock_Product_Order_App sql is ", sql)
                    cursor.execute(sql, opCode, purchaseNum, purchasePrice, supplier, settlement, id, stockProductID)
                cursor.commit()
            cursor.close
            cnxn.close
            return "1"
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

    def select_dict_item_list(self, item_type):
        # select ID, DictValue from [csidbo].CustomDict where DictType=501027 and status = 0
        try:
            item_list = []
            cnxn = pyodbc.connect(self._conn_str)
            cursor = cnxn.cursor()
            if item_type == "brand":
                sql = "select ID, DictValue from [csidbo].CustomDict where DictType=501027 and status=0"
            else:
                sql = "Select ID, custname from [csidbo].Cust_Info where grouptype=9 and status=0"
            cursor.execute(sql)
            for row in cursor:
                item = dict()
                item["code"] = row[0]
                item["name"] = row[1]
                item_list.append(item)
            cursor.close()
            cnxn.close()
            return item_list
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
