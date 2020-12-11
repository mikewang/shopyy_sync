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

            v_sql_columns = "e.[采购人], a.StockProductID,a.ProductID,CONVERT(varchar, d.SignDate, 120 ) as SignDate," \
                            "a.GoodsCode,a.SpecNo,f.GoodsCDesc, a.GoodsUnit, b._ImageID,c.ImageGuid,c.ImageFmt," \
                            "c.ModuleID,CONVERT(varchar, c.FileDate, 120 ) as FileDate,c.ThumbImage,b.[其它.供应商名称]," \
                            "b.[其它.允采购量],b.[其它.应采购价],b.[其它.商品品牌], " \
                            "coalesce(g.ordernum,0) as ordernum, coalesce(h.id,0) as priceEnquiredID  "
            v_sql_fromtab = "FROM [Stock_Product_Info] as a " \
                            "join FTPart_Stock_Product_Property_1 as b on a.StockProductID=b.MainID " \
                            "join Product_Image as c on b._ImageID=c.ProductImageID " \
                            "join stock_info d on d.ID=a.StockID " \
                            "join [FTPart_Stock_Property_1] e on e.[MainID] = d.ID " \
                            "left join [Stock_Product_Info_Desc] f on a.StockProductID=f.StockProductID " \
                            "left join (select [StockProductID], sum([OrderNum]*[OrderStat]) as ordernum from [Stock_Product_Order_App] group by [StockProductID]) g on a.StockProductID=g.StockProductID  " \
                            "left join (select max(id) as id, StockProductID from [Stock_Product_EnquiryPrice_App] group by StockProductID ) h on  a.StockProductID=h.StockProductID "
            v_sql = "select " + topN + " " + v_sql_columns + v_sql_fromtab + "  where b.[其它.允采购量] > coalesce(g.ordernum,0) "
            v_sql_cc = "select count(*) as cc " + v_sql_fromtab + "  where b.[其它.允采购量] > coalesce(g.ordernum,0) "

            filter_brand = filter_stock["brand"]
            if filter_brand is not None:
                filter_sql = ''
                for b in filter_brand:
                    filter_sql = filter_sql + "'" + b + "',"
                filter_sql = filter_sql.rstrip(',')
                v_sql = v_sql + " and b.[其它.商品品牌] in (" + filter_sql + ")"
                v_sql_cc = v_sql_cc + " and b.[其它.商品品牌] in (" + filter_sql + ")"
            filter_enquriy = filter_stock["enquiry"]
            if filter_enquriy is not None:
                if filter_enquriy == '未询价':
                    v_sql = v_sql + " and  coalesce(h.id,0) = 0 "
                    v_sql_cc = v_sql_cc + " and  coalesce(h.id,0) = 0 "
                elif filter_enquriy == '已询价':
                    v_sql_cc = v_sql_cc + " and  coalesce(h.id,0) > 0 "
                    v_sql_cc = v_sql_cc + " and  coalesce(h.id,0) > 0 "
            filter_begin = filter_stock["begin"]
            if filter_begin is not None:
                v_sql = v_sql + " and d.SignDate >= '" + filter_begin + "'"
                v_sql_cc = v_sql_cc + " and d.SignDate >= '" + filter_begin + "'"
            filter_end = filter_stock["end"]
            if filter_end is not None:
                v_sql = v_sql + " and d.SignDate <= '" + filter_end + " 23:59:59'"
                v_sql_cc = v_sql_cc + " and d.SignDate <= '" + filter_end + " 23:59:59'"

            v_sql = v_sql + " order by d.signdate desc,a.stockproductid desc"
            v_sql = "select  top 10 * from (" + v_sql + " ) as v1 order by v1.SignDate asc,v1.StockProductID asc"

            print("select_stock_product_list page sql is \n", v_sql)
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
            # 总数统计
            print("select_stock_product_list count sql is \n", v_sql_cc)
            cursor.execute(v_sql_cc)
            product_count_row = cursor.fetchone()
            product_count = product_count_row[0]
            cursor.close()
            cnxn.close()
            return product_list, product_count
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
            if ptype == "return":
                v_sql_tab_g = "(SELECT * FROM [Stock_Product_Order_App] AS T1 " \
                              "WHERE OrderStat = -1 and settlement > 0)"
            else:
                v_sql_tab_g = "(SELECT * FROM [Stock_Product_Order_App] AS T1 " \
                              "WHERE NOT EXISTS( SELECT 1 FROM [Stock_Product_Order_App] AS T2 " \
                              "WHERE T1.orderID=T2.sourceOrderId and OrderStat = -1) and t1.sourceOrderId is null)  "

            v_sql_tab_h = "(select max(id) as id, StockProductID " \
                          "from [Stock_Product_EnquiryPrice_App] group by StockProductID) "

            v_sql = v_sql + "e.[采购人], a.StockProductID,a.ProductID,CONVERT(varchar, d.SignDate, 120 ) as SignDate," \
                            "a.GoodsCode,a.SpecNo,f.GoodsCDesc, a.GoodsUnit, b._ImageID,c.ImageGuid,c.ImageFmt," \
                            "c.ModuleID,CONVERT(varchar, c.FileDate, 120 ) as FileDate,c.ThumbImage," \
                            "g.supplier as supplier," \
                            "b.[其它.允采购量],b.[其它.应采购价],b.[其它.商品品牌]," \
                            "coalesce(g.[OrderNum],0) as ordernum," \
                            "g.orderprice, g.orderStat, g.settlement,g.opcode as order_opcode," \
                            "g.orderID as product_order_id, " \
                            "coalesce(h.id,0) as priceEnquiredID, " \
                            "CONVERT(varchar, g.CreateTime, 120 ) as CreateTime," \
                            "g.sourceOrderID, CONVERT(varchar, g.ensureTime, 120 ) as ensureTime, g.ensureOpCode, " \
                            "CONVERT(varchar, g.receiveGoodsTime, 120 ) as receiveGoodsTime, g.receiveOpCode," \
                            "CONVERT(varchar, g.settlementTime, 120 ) as settlementTime, g.settlementOpCode " \
                            "FROM [Stock_Product_Info] as a " \
                            "join  FTPart_Stock_Product_Property_1 as b on a.StockProductID=b.MainID " \
                            "join Product_Image as c on b._ImageID=c.ProductImageID " \
                            "join stock_info d on d.ID=a.StockID " \
                            "join [FTPart_Stock_Property_1] e on e.[MainID] = d.ID " \
                            "left join [Stock_Product_Info_Desc] f on a.StockProductID=f.StockProductID "
            v_sql = v_sql + "join " + v_sql_tab_g + "as g on a.StockProductID=g.StockProductID "
            v_sql = v_sql + "left join " + v_sql_tab_h + " h on  a.StockProductID=h.StockProductID  "

            if ptype == "order":
                # 去掉订货，订货，订货完成三个状态的查询
                v_sql = v_sql + "  where 1=1 and g.settlement <=1 "
            elif ptype == "receive":
                # 收货，状态的查询
                v_sql = v_sql + "  where 1=1 and g.settlement >=1 and g.settlement <=2"
            elif ptype == "return":
                # 退货, 状态的查询
                v_sql = v_sql + "  where 1=1 and g.settlement >=1 and g.settlement <=2"
            elif ptype == "settlement":
                # 结算, 状态的查询
                v_sql = v_sql + "  where 1=1 and g.settlement >=2"
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
            sql = "select  top 10 * from (" + v_sql + " ) as v1 order by v1.CreateTime asc,v1.StockProductID asc, v1.product_order_id asc"
            print(ptype, "sql is ", sql)
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
                product.orderOpCode = row[22]
                product.orderID = row[23]
                product.priceEnquiredID = row[24]
                product.createTime = row[25]
                product.sourceOrderID = row[26]
                product.ensureTime = row[27]
                product.ensureOpCode = row[28]
                product.receiveGoodsTime = row[29]
                product.receiveOpCode = row[30]
                product.settlementTime = row[31]
                product.settlementOpCode = row[32]

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
                opCode = prod["orderOpCode"]
                purchaseNum = prod["purchaseNum"]
                purchasePrice = prod["purchasePrice"]
                orderStat = prod["orderStat"]
                supplier = prod["supplier"]
                settlement = prod["settlement"]
                settlement = 0
                sql = "insert into Stock_Product_Order_App(stockProductID,opCode, OrderNum, OrderPrice,orderStat," \
                      "supplier, settlement) " \
                      " values(?,?,?,?,?,?,?)"
                print("add order", "insert Stock_Product_Order_App sql is ", sql)
                cursor.execute(sql, stockProductID, opCode, purchaseNum, purchasePrice, orderStat, supplier, settlement)
                # myTableId = cursor.fetchone()[0]
                # print("Stock_Product_Order_App id is ", myTableId)
                #  last row id 不生效。
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
            result = "1"
            cnxn = pyodbc.connect(self._conn_str)
            cursor = cnxn.cursor()
            for prod in prod_dict_list:
                print("order product id=", prod["orderID"], prod["stockProductID"])
                orderID = prod["orderID"]
                stockProductID = prod["stockProductID"]
                if operate_type == "cancel":
                    opCode = prod["orderOpCode"]
                    # 插入一条 取消 订货记录进来，原订货记录保存。
                    orderStat = -1
                    # 取消订货。
                    sql = "select count(*) from Stock_Product_Order_App where sourceOrderID=?"
                    cursor.execute(sql, orderID)
                    row = cursor.fetchone()
                    cc = row[0]
                    if cc == 0:
                        sql = "delete from Stock_Product_Order_App where sourceOrderID=?"
                        print(operate_type, "delete sql --- \n ", sql)
                        cursor.execute(sql, orderID)
                    sql = "insert into Stock_Product_Order_App(stockProductID,opCode, OrderNum, OrderPrice," \
                          "orderStat,supplier, settlement,sourceOrderID,createTime)  " \
                          "select stockProductID,?, OrderNum, OrderPrice,?,supplier, settlement, orderID, getdate() " \
                          "from Stock_Product_Order_App where orderID=?"
                    print(operate_type, "insert sql --- \n ", sql)
                    cursor.execute(sql, opCode, orderStat, orderID)
                    cursor.commit()

                elif operate_type == "complete":
                    ensureOpCode = prod["ensureOpCode"]
                    purchaseNum = prod["purchaseNum"]
                    purchasePrice = prod["purchasePrice"]
                    # 订货 或者 退货
                    orderStat = prod["orderStat"]
                    supplier = prod["supplier"]
                    settlement = prod["settlement"]
                    settlement = 1
                    sql = "update Stock_Product_Order_App " \
                          "set ensureOpCode = ?, OrderNum = ? , OrderPrice=?, supplier=? , settlement=?, ensureTime=getdate() " \
                          "where orderID = ? and stockProductID = ? and settlement <> ? "
                    print(operate_type, "update sql ---\n ", sql)
                    cursor.execute(sql, ensureOpCode, purchaseNum, purchasePrice, supplier, settlement, orderID, stockProductID, settlement)
                    cursor.commit()
                elif operate_type == "return":
                    # 插入一条 退货 记录进来，原订货记录保存。
                    opCode = prod["orderOpCode"]
                    print(operate_type, "product", prod)
                    orderStat = -1
                    purchaseNum = prod["purchaseNum"]
                    purchasePrice = prod["purchasePrice"]
                    settlement = prod["settlement"]
                    # 退货。
                    sql = "select count(*) from Stock_Product_Order_App where sourceOrderID=?"
                    cursor.execute(sql, orderID)
                    row = cursor.fetchone()
                    cc = row[0]
                    if cc > 0:
                        sql = "delete from Stock_Product_Order_App where sourceOrderID=?"
                        print(operate_type, "delete sql --- \n ", sql)
                        cursor.execute(sql, orderID)
                        print(operate_type, stockProductID, " product has been returned, delete it now.")
                    sql = "insert into Stock_Product_Order_App(stockProductID,opCode, OrderNum, OrderPrice," \
                          "orderStat,supplier, settlement,sourceOrderID,createTime)  " \
                          "select stockProductID,?, ?, ?, ? ,supplier, settlement, orderID, getdate() " \
                          "from Stock_Product_Order_App where orderID=?"
                    print(operate_type, "insert sql --- \n ", sql)
                    cursor.execute(sql, opCode, purchaseNum, purchasePrice, orderStat, orderID)
                    if settlement == 2:
                        sql = "update [FTPart_Stock_Product_Property_1] " \
                              "set [其它.采购剩余数量] = [其它.采购剩余数量] + ? " \
                              "where [MainID]=?"
                        cursor.execute(sql, purchaseNum, stockProductID)
                        print(operate_type, "update sql2 ---\n ", sql)
                    cursor.commit()
                elif operate_type == "undoreturn":
                    # 取消 退货。
                    opCode = prod["orderOpCode"]
                    orderStat = 0
                    purchaseNum = prod["purchaseNum"]
                    settlement = prod["settlement"]
                    # 退货。
                    sql = "select count(*) from Stock_Product_Order_App where orderID=? and orderStat = -1"
                    cursor.execute(sql, orderID)
                    row = cursor.fetchone()
                    cc = row[0]
                    if cc == 0:
                        sql = "update Stock_Product_Order_App set orderStat = ? where orderID=?"
                        print(operate_type, "update sql --- \n ", sql)
                        cursor.execute(sql,  orderStat, orderID)
                        if settlement == 2:
                            sql = "update [FTPart_Stock_Product_Property_1] " \
                                  "set [其它.采购剩余数量] = [其它.采购剩余数量] - ? " \
                                  "where [MainID]=?"
                            cursor.execute(sql, purchaseNum, stockProductID)
                            print(operate_type, "update sql2 ---\n ", sql)

                        cursor.commit()
                    else:
                        result = "-1"
                elif operate_type == "receive":
                    receiveOpCode = prod["receiveOpCode"]
                    purchaseNum = prod["purchaseNum"]
                    purchasePrice = prod["purchasePrice"]
                    # 订货 或者 退货
                    orderStat = prod["orderStat"]
                    supplier = prod["supplier"]
                    settlement = prod["settlement"]
                    settlement = 2
                    sql = "update Stock_Product_Order_App " \
                          "set receiveOpCode = ?, settlement=?, receiveGoodsTime=getdate() " \
                          "where orderID = ? and stockProductID = ? and settlement <> ? "
                    print(operate_type, "update sql ---\n ", sql)
                    cursor.execute(sql, receiveOpCode, settlement, orderID, stockProductID, settlement)
                    sql = "update [FTPart_Stock_Product_Property_1] " \
                          "set [其它.采购剩余数量]=[其它.采购剩余数量] + [其它.允采购量] - ?,[其它.供应商名称]=?,[其它.业务员]=? " \
                          "where [MainID]=?"
                    cursor.execute(sql, purchaseNum, supplier, receiveOpCode, stockProductID)
                    print(operate_type, "update sql2 ---\n ", sql)
                    cursor.commit()
                elif operate_type == "settlement":
                    settlementOpCode = prod["settlementOpCode"]
                    # 结算
                    settlement = prod["settlement"]
                    settlement = 3
                    sql = "update Stock_Product_Order_App " \
                          "set settlementOpCode = ?, settlement=?,settlemnetTime=getdate() " \
                          "where orderID = ? and stockProductID = ? and settlement <> ? "
                    print(operate_type, "update sql ---\n ", sql)
                    cursor.execute(sql, settlementOpCode, settlement, orderID, stockProductID, settlement)
                    cursor.commit()
            cursor.close
            cnxn.close
            return result
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
        # select ID, DictValue from CustomDict where DictType=501027 and status = 0
        try:
            item_list = []
            cnxn = pyodbc.connect(self._conn_str)
            cursor = cnxn.cursor()
            if item_type == "brand":
                sql = "select ID, DictValue from CustomDict where DictType=501027 and status=0"
            else:
                sql = "Select ID, custname from Cust_Info where grouptype=9 and status=0"
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
