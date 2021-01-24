# -*- coding: utf-8 -*-
import configparser
import traceback
import sys
import os
import pyodbc
import datetime
import base64
from Model.user import UserInfo
from Model.product import ProductInfo, AccountProductInfo, ProductEnquiryPrice
from Model import constant_v as cv


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
            page_prod_count = 10
            cnxn = pyodbc.connect(self._conn_str)
            cursor = cnxn.cursor()
            # 数据源
            v_sql = "  select * from v_app_stock  where 0=0  "

            # 过滤条件，商品描述
            filter_GoodsCDesc = filter_stock["goodsDesc"]
            if filter_GoodsCDesc is not None:
                v_sql = v_sql + " and GoodsCDesc like '%" + filter_GoodsCDesc + "%'"
            filter_brand = filter_stock["brand"]
            if filter_brand is not None:
                filter_sql = ''
                for b in filter_brand:
                    filter_sql = filter_sql + "'" + b + "',"
                filter_sql = filter_sql.rstrip(',')
                v_sql = v_sql + " and [其它.商品品牌] in (" + filter_sql + ")"
            filter_enquriy = filter_stock["enquiry"]
            if filter_enquriy is not None:
                if filter_enquriy == '未询价':
                    v_sql = v_sql + " and  priceEnquiredID = 0 "
                elif filter_enquriy == '已询价':
                    v_sql = v_sql + " and  priceEnquiredID > 0 "
            filter_begin = filter_stock["begin"]
            if filter_begin is not None:
                if filter_enquriy is not None and filter_enquriy == '已询价':
                    v_sql = v_sql + " and enquirydate >= '" + filter_begin + "'"
                else:
                    # 未询价
                    v_sql = v_sql + " and SignDate >= '" + filter_begin + "'"
            filter_end = filter_stock["end"]
            if filter_end is not None:
                if filter_enquriy is not None and filter_enquriy == '已询价':
                    v_sql = v_sql + " and enquirydate <= '" + filter_end + " 23:59:59'"
                else:
                    # 未询价
                    v_sql = v_sql + " and SignDate <= '" + filter_end + " 23:59:59'"
                    # 总数统计
            product_count = 0
            topN = page_no * page_prod_count
            # 增加排序功能

            if filter_enquriy is not None and filter_enquriy == '已询价':
                v_sql = "select row_number() over(order by v.enquirydate desc,v.stockproductid desc) as rownumber,  v.* ,count(*) over() as product_count from (" + v_sql + ") as v"
            else:
                # 未询价
                v_sql = "select row_number() over(order by v.SignDate desc,v.stockproductid desc) as rownumber,  v.* ,count(*) over() as product_count from (" + v_sql + ") as v"

            v_sql = "select * from (" + v_sql + ") as v1 where v1.rownumber > " + str(topN - page_prod_count) + " and v1.rownumber <= " + str(topN) + " order by v1.rownumber"
            print("*"*50)
            print("select_stock_product_list page sql is \n", v_sql)
            cursor.execute(v_sql)
            for row in cursor:
                product = ProductInfo()
                product.OpCode = row[1]
                product.StockProductID = row[2]
                product.ProductID = row[3]
                product.SignDate = row[4]
                product.GoodsCode = row[5]
                product.SpecNo = row[6]
                product.GoodsCDesc = row[7]
                product.GoodsUnit = row[8]
                ImageID = row[9]
                product.ImageGuid = row[10]
                product.ImageFmt = row[11]
                product.ModuleID = row[12]
                product.FileDate = row[13]
                thumbImage = row[14]
                base64_bytes = base64.b64encode(thumbImage)
                base64_image = base64_bytes.decode("utf8")
                product.imageBase64 = base64_image
                product.supplier = row[15]
                product.permittedNum = row[16]
                product.shouldPrice = row[17]
                product.brand = row[18]
                # app采购量
                product.orderNum = row[19]
                product.priceEnquiredID = row[20]
                product.enquiryDate = row[21]
                product.appPermittedNum = row[22]
                product_count = row[23]
                product_list.append(product)

            cursor.close()
            cnxn.close()
            print(product_list, product_count)
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
            return None, 0

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

    def parse_product_cursor(self, row):
        product = ProductInfo()
        product.OpCode = row[1]
        product.StockProductID = row[2]
        product.ProductID = row[3]
        product.SignDate = row[4]
        product.GoodsCode = row[5]
        product.SpecNo = row[6]
        product.GoodsCDesc = row[7]
        product.GoodsUnit = row[8]
        ImageID = row[9]
        product.ImageGuid = row[10]
        product.ImageFmt = row[11]
        product.ModuleID = row[12]
        product.FileDate = row[13]
        thumbImage = row[14]
        base64_bytes = base64.b64encode(thumbImage)
        base64_image = base64_bytes.decode("utf8")
        product.imageBase64 = base64_image
        product.supplier = row[15]
        product.permittedNum = row[16]
        product.shouldPrice = row[17]
        product.brand = row[18]
        product.orderNum = row[19]
        product.orderPrice = row[20]
        # orderStat = 1, 订货， -1 ，退货，但退货记录要保存。
        product.orderStat = row[21]
        # settlement = 1， 确认订货成功，并没有现实收货，0，默认值，未确认订货成功。
        product.settlement = row[22]
        product.orderOpCode = row[23]
        product.orderID = row[24]
        product.priceEnquiredID = row[25]
        product.createTime = row[26]
        product.sourceOrderID = row[27]
        product.ensureTime = row[28]
        product.ensureOpCode = row[29]
        product.receiveGoodsTime = row[30]
        product.receiveOpCode = row[31]
        product.settlementTime = row[32]
        product.settlementOpCode = row[33]
        product.enquiryDate = row[34]
        product.appPermittedNum = row[35]
        product.accountNum = row[36]
        return product

    def select_order_product_list(self, page_no, filter_stock, ptype):
        # 检索 所有的 订货商品
        # 查询的类型: 订货模块，类型有 order(已经订货,附加检索 取消订购的记录)
        # 查询的类型: 退货模块，类型有 complete(完成订货，附加检索 已退货记录) return(已退货)
        # 查询的类型: 结算模块，类型有 complete(完成订货，附加检索 已退货记录) settlement(已结算，附加检索 已退货记录)
        # 查询的类型: 结算模块，类型有 history(所有状态，包括历史表订货，附加检索 已取消订货记录， 已退货记录和退货取消记录) settlement(已结算，附加检索 已退货记录)

        try:
            product_list = []
            page_prod_count = 10
            cnxn = pyodbc.connect(self._conn_str)
            cursor = cnxn.cursor()
            # 数据源
            v_sql = "select * from v_app_stock_order where 0=0 "
            v_time_column = "CreateTime"
            if ptype == cv.order_goods:
                v_sql = v_sql + "and settlement = 0 and OrderStat = 1"
                v_time_column = "CreateTime"
            elif ptype == cv.complete_order:
                v_sql = v_sql + "and settlement = 1 and OrderStat = 1"
                v_time_column = "ensureTime"
            elif ptype == cv.account_goods:
                v_sql = v_sql + "and settlement = 1 and OrderStat = 1 and accountNum > 0"
                v_time_column = "ensureTime"
            elif ptype == cv.return_goods:
                v_sql = v_sql + "and settlement = 1 and OrderStat = -1"
                v_time_column = "CreateTime"
            elif ptype == cv.settlement_goods:
                v_sql = v_sql + "and settlement = 2 and OrderStat = 1"
                v_time_column = "settlementTime"
            elif ptype == cv.history_goods:
                v_sql = v_sql + " and settlement >= 0 and OrderStat = 1"
            else:
                v_sql = v_sql + " and settlement = 0 and OrderStat = 1"

            # 过滤条件，商品描述
            filter_GoodsCDesc = filter_stock["goodsDesc"]
            if filter_GoodsCDesc is not None:
                v_sql = v_sql + " and GoodsCDesc like '%" + filter_GoodsCDesc + "%'"
            filter_brand = filter_stock["brand"]
            if filter_brand is not None:
                filter_sql = ''
                for b in filter_brand:
                    filter_sql = filter_sql + "'" + b + "',"
                filter_sql = filter_sql.rstrip(',')
                v_sql = v_sql + " and [其它.商品品牌] in (" + filter_sql + ")"
            filter_enquriy = filter_stock["enquiry"]
            if filter_enquriy is not None:
                if filter_enquriy == '未询价':
                    v_sql = v_sql + " and  priceEnquiredID = 0 "
                elif filter_enquriy == '已询价':
                    v_sql = v_sql + " and  priceEnquiredID > 0 "
            # begin date
            filter_begin = filter_stock["begin"]
            if filter_begin is not None:
                v_sql = v_sql + " and " + v_time_column + " >= '" + filter_begin + "'"
            # end data
            filter_end = filter_stock["end"]
            if filter_end is not None:
                v_sql = v_sql + " and " + v_time_column + "<= '" + filter_end + " 23:59:59'"
            filter_supplier = filter_stock["supplier"]
            if filter_supplier is not None:
                filter_sql = ''
                for b in filter_supplier:
                    filter_sql = filter_sql + "'" + b + "',"
                filter_sql = filter_sql.rstrip(',')
                v_sql = v_sql + " and supplier in (" + filter_sql + ")"
            filter_specno = filter_stock["specno"]
            if filter_specno is not None:
                v_sql = v_sql + " and SpecNo = '" + filter_specno + "'"

            # 先总数
            product_count = 0
            topN = page_no*page_prod_count
            # 再分页，需要增加排序功能
            v_sql = "select row_number() over(order by v." + v_time_column + " desc,v.stockproductid desc) as rownumber,  v.* ,count(*) over() as product_count from (" + v_sql + ") as v"
            v_sql = "select * from (" + v_sql + ") as v1 where v1.rownumber > " + str(topN - page_prod_count) + " and v1.rownumber <= " + str(topN) + " order by v1.rownumber"
            print(ptype, "sql page is ", v_sql)
            cursor.execute(v_sql)
            for row in cursor:
                product = self.parse_product_cursor(row)
                product_count = row[len(row)-1]
                product_list.append(product)

            # 二次查询有没有退货的记录
            if ptype == cv.complete_order or ptype == cv.settlement_goods or ptype == cv.history_goods:
                return_product_list = []
                for product in product_list:
                    v_sql = ""
                    if ptype == cv.history_goods:
                        v_sql = "select * from v_app_stock_order  where (orderstat=-1 or orderstat=0) and stockproductid=" + str(product.StockProductID)
                    else:
                        v_sql = "select * from v_app_stock_order  where orderstat=-1 and stockproductid=" + str(product.StockProductID)
                    v_sql = "select 0 as rownumber, v.* from (" + v_sql + ") as v "
                    print(ptype, "sql attach is ", v_sql)
                    cursor.execute(v_sql)
                    for row in cursor:
                        return_product = self.parse_product_cursor(row)
                        return_product.product = product
                        return_product_list.append(return_product)
                for return_product in return_product_list:
                    index = product_list.index(return_product.product)
                    return_product.product = None
                    product_list.insert(index+1, return_product)
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
            return None, 0

    def add_stock_product_order(self, prod_dict_list):
        try:
            conn = pyodbc.connect(self._conn_str)
            cursor = conn.cursor()
            result_product_list = []
            for prod in prod_dict_list:
                print("add order product is ", prod["stockProductID"], prod)
                stockProductID = prod["stockProductID"]
                opCode = prod["orderOpCode"]
                purchaseNum = prod["purchaseNum"]
                purchasePrice = prod["purchasePrice"]
                orderStat = prod["orderStat"]
                supplier = prod["supplier"]
                settlement = prod["settlement"]
                # 訂貨
                settlement = 0

                result_product = ProductInfo()
                result_product.StockProductID = stockProductID

                # 校验购买的数量和允购买量的关系，有可能允许购买量已经不够
                sql = "select coalesce([其它.app允采购量], [其它.允采购量]) from FTPart_Stock_Product_Property_1 " \
                      "where MainID=?"
                cursor.execute(sql, stockProductID)
                permitNum = cursor.fetchone()[0]
                if permitNum is None:
                    print("*error*"*10, "url is wrong.")
                    permitNum = -1
                if permitNum >= purchaseNum:
                    sql = "update [FTPart_Stock_Product_Property_1] " \
                          "set [其它.app允采购量] = coalesce([其它.app允采购量], [其它.允采购量]) - ?," \
                          "[其它.app采购量] = coalesce([其它.app采购量], 0) + ?," \
                          "[其它.供应商名称] = ? " \
                          "where [MainID] = ?"
                    cursor.execute(sql, purchaseNum,purchaseNum, supplier, stockProductID)
                    sql = "insert into Stock_Product_Order_App(stockProductID,opCode, OrderNum, OrderPrice,orderStat," \
                          "supplier, settlement) " \
                          " values(?,?,?,?,?,?,?)"
                    print("add order", "insert Stock_Product_Order_App sql is ", sql)
                    cursor.execute(sql, stockProductID, opCode, purchaseNum, purchasePrice, orderStat, supplier, settlement)
                    sql = "select @@IDENTITY"
                    cursor.execute(sql)
                    lastOrderID = cursor.fetchone()[0]
                    sql = "insert INTO Stock_Product_Order_App_hist(StockProductID, OpCode, OrderNum," \
                          "OrderPrice, supplier, OperateType, orderId, note) " \
                          "VALUES(?,?,?,?,?,?,?,?)"
                    cursor.execute(sql, stockProductID, opCode, purchaseNum, purchasePrice, supplier, 'order', lastOrderID, '')
                    # myTableId = cursor.fetchone()[0]
                    # print("Stock_Product_Order_App id is ", myTableId)
                    #  last row id 不生效。
                    cursor.commit()
                    result_product.note = "1:采购成功"
                else:
                    result_product.note = "0:采购失败，允购量 " + str(permitNum) + ", 采购量 " + str(purchaseNum)
                result_product_list.append(result_product)

            cursor.close
            conn.close
            return result_product_list
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
            conn.rollback()
            return result_product_list

    def update_stock_product_order(self, prod_dict_list, operate_type):
        try:
            result_product_list = []
            cnxn = pyodbc.connect(self._conn_str)
            cursor = cnxn.cursor()
            for prod in prod_dict_list:
                print("order product id=", prod["orderID"], prod["stockProductID"])
                # 全局数据
                orderID = prod["orderID"]
                stockProductID = prod["stockProductID"]

                # 返回结果集
                result_product = ProductInfo()
                result_product.StockProductID = stockProductID
                result_product.note = "0:" + operate_type + " failure."

                if operate_type == cv.cancel_order:

                    # 取消订货
                    opCode = prod["orderOpCode"]
                    # 更新状态码为0，然后 写入历史表。
                    orderStat = 0
                    # 取消订货。
                    sql = "update Stock_Product_Order_App set orderStat= ? where orderID=?"
                    cursor.execute(sql, orderStat, orderID)
                    sql = "select stockProductID, OrderNum, OrderPrice,supplier, settlement " \
                          "from Stock_Product_Order_App where orderID=?"
                    cursor.execute(sql, orderID)
                    row = cursor.fetchone()
                    if row is not None:
                        stockProductID = row[0]
                        orderNum = row[1]
                        purchasePrice = row[2]
                        supplier = row[3]
                        settlement = row[4]
                        # 修改 app允采购量
                        sql = "update [FTPart_Stock_Product_Property_1] " \
                              "set [其它.app允采购量] = [其它.app允采购量] + ?, " \
                              "[其它.app采购量] = [其它.app采购量] - ?" \
                              " where [MainID] = ?"
                        cursor.execute(sql, orderNum, orderNum, stockProductID)
                        # insert history row
                        sql = "insert INTO Stock_Product_Order_App_hist(StockProductID, OpCode, OrderNum,OrderPrice," \
                              " supplier, OperateType, orderId, note) VALUES(?,?,?,?,?,?,?,?)"
                        print(operate_type, "insert hist sql --- \n ", sql)
                        cursor.execute(sql, stockProductID, opCode, orderNum, purchasePrice,
                                       supplier, cv.cancel_order, orderID, '')
                        cursor.commit()
                        result_product.note = "1:取消订货成功"

                elif operate_type == cv.complete_order:
                    # 确认订货，完成采购
                    ensureOpCode = prod["ensureOpCode"]
                    purchaseNum = prod["purchaseNum"]
                    purchasePrice = prod["purchasePrice"]
                    # 订货 或者 退货
                    orderStat = prod["orderStat"]
                    supplier = prod["supplier"]
                    settlement = prod["settlement"]
                    # 订货确认。
                    settlement = 1
                    sql = "select orderNum from Stock_Product_Order_App where orderID = ? and stockProductID = ? and settlement <> ?"
                    cursor.execute(sql, orderID, stockProductID, settlement)
                    row = cursor.fetchone()
                    orderNum = purchaseNum
                    if row is not None:
                        orderNum = row[0]

                    sql = "update Stock_Product_Order_App " \
                          "set ensureOpCode = ?,settlement=?, orderNum = ?," \
                          " ensureTime=getdate() " \
                          "where orderID = ? and stockProductID = ? and settlement <> ? "
                    print(operate_type, "update sql ---\n ", sql)
                    cursor.execute(sql, ensureOpCode, settlement, purchaseNum, orderID, stockProductID, settlement)
                    # insert history row
                    sql = "insert INTO Stock_Product_Order_App_hist(StockProductID, OpCode, OrderNum," \
                          "OrderPrice, supplier, OperateType, orderId, note) " \
                          "VALUES(?,?,?,?,?,?,?,?)"
                    cursor.execute(sql, stockProductID, ensureOpCode, purchaseNum, purchasePrice, supplier,
                                   cv.complete_order, orderID, '')
                    sql = "update [FTPart_Stock_Product_Property_1] " \
                          "set [其它.app允采购量] = [其它.app允采购量] + ?,[其它.app采购量] = [其它.app采购量] - ?, " \
                            "[其它.供应商名称] = ? " \
                          "where [MainID]=?"
                    cursor.execute(sql, orderNum-purchaseNum, orderNum-purchaseNum, supplier, stockProductID)
                    print(operate_type, "update sql2 ---\n ", sql)
                    # [Stock_Product_InfoBase].unitprice 更新单价
                    # [Stock_Product_Info].goodsnum 更新采购量，为0是要设置为允采购量，因为系统不能设置为0。
                    sql = "select sum(ordernum*orderStat) as goodsnum,sum(ordernum*orderprice*orderStat) as allprice " \
                          "from Stock_Product_Order_App " \
                          "where stockProductID = ? and (orderStat = -1 or orderStat = 1) and settlement >= 1"
                    cursor.execute(sql, stockProductID)
                    row = cursor.fetchone()
                    goodsnum = row[0]
                    allprice = row[1]
                    if goodsnum == 0:
                        unitprice = 0
                    else:
                        unitprice = allprice/goodsnum
                    print("写入erp数据库", stockProductID, unitprice, goodsnum)
                    sql = "update Stock_Product_InfoBase set unitprice=? where stockProductID = ?"
                    cursor.execute(sql, unitprice, stockProductID)
                    sql = "update Stock_Product_Info set goodsnum=? where stockProductID = ?"
                    cursor.execute(sql, goodsnum, stockProductID)
                    cursor.commit()
                    result_product.note = "1:订购成功"
                elif operate_type == cv.return_goods:
                    # 插入一条 退货 记录进来，原订货记录保存。
                    opCode = prod["orderOpCode"]
                    print(operate_type, "product", prod)
                    orderStat = -1
                    # 本次退货数量
                    purchaseNum = prod["purchaseNum"]
                    purchasePrice = prod["purchasePrice"]
                    settlement = prod["settlement"]
                    # 退货。
                    result_product.orderNum = purchaseNum

                    sql = "select stockProductID, supplier, settlement,orderNum from Stock_Product_Order_App " \
                          "where orderID=? and orderStat = 1"
                    cursor.execute(sql, orderID)
                    row = cursor.fetchone()
                    if row is not None:
                        stockProductID = row[0]
                        supplier = row[1]
                        settlement = row[2]
                        doneOrderNum = row[3]
                        sql = "select stockProductID, sum(orderNum) from Stock_Product_Order_App " \
                              "where sourceOrderID=? and orderStat = -1 group by stockProductID"
                        cursor.execute(sql, orderID)
                        returnOrderNum = 0
                        row = cursor.fetchone()
                        if row is not None:
                            returnOrderNum = row[1]
                        if doneOrderNum < returnOrderNum + purchaseNum:
                            result_product.note = "0:退货失败，采购量 " + str(doneOrderNum) + ", 已退货 " + str(returnOrderNum) + ", 本次退货 " + str(purchaseNum)
                        else:
                            sql = "insert into Stock_Product_Order_App(stockProductID,opCode, OrderNum, OrderPrice," \
                                  "orderStat,supplier, settlement,sourceOrderID,createTime) " \
                                  " values(?,?,?,?,?,?,?,?,getdate()) "
                            print(operate_type, "insert sql --- \n ", sql)
                            cursor.execute(sql, stockProductID, opCode, purchaseNum, purchasePrice, orderStat, supplier, settlement, orderID)
                            # insert history row
                            sql = "insert INTO Stock_Product_Order_App_hist(StockProductID, OpCode, OrderNum,OrderPrice," \
                                  " supplier, OperateType, orderId, note) VALUES(?,?,?,?,?,?,?,?)"
                            print(operate_type, "insert hist sql --- \n ", sql)
                            cursor.execute(sql, stockProductID, opCode, purchaseNum, purchasePrice,
                                           supplier, cv.return_goods, orderID, '')
                            sql = "update [FTPart_Stock_Product_Property_1] " \
                                  "set [其它.app允采购量] = [其它.app允采购量] + ?, " \
                                  "[其它.app采购量] = [其它.app采购量] - ? " \
                                  "where [MainID]=?"
                            cursor.execute(sql, purchaseNum, purchaseNum, stockProductID)
                            print(operate_type, "update sql2 ---\n ", sql)
                            # [Stock_Product_InfoBase].unitprice 更新单价
                            # [Stock_Product_Info].goodsnum 更新采购量，为0是要设置为允采购量，因为系统不能设置为0。
                            sql = "select sum(ordernum*orderStat) as goodsnum,sum(ordernum*orderprice*orderStat) as allprice " \
                                  "from Stock_Product_Order_App " \
                                  "where stockProductID = ? and (orderStat = -1 or orderStat = 1)"
                            cursor.execute(sql, stockProductID)
                            row = cursor.fetchone()
                            goodsnum = row[0]
                            allprice = row[1]
                            if goodsnum == 0:
                                unitprice = 0
                            else:
                                unitprice = allprice / goodsnum
                            print("写入erp数据库", stockProductID, unitprice, goodsnum)
                            sql = "update Stock_Product_InfoBase set unitprice=? where stockProductID = ?"
                            cursor.execute(sql, unitprice, stockProductID)
                            sql = "update Stock_Product_Info set goodsnum=? where stockProductID = ?"
                            cursor.execute(sql, goodsnum, stockProductID)
                            cursor.commit()

                            result_product.note = "1:退货成功，采购量 " + str(doneOrderNum) + ", 退货量 "+str(purchaseNum) + ", 共退货 " + str(returnOrderNum+purchaseNum) + ":" + str(doneOrderNum-returnOrderNum-purchaseNum)
                    else:
                        result_product.note = "0:退货失败，没有记录."
                    print(result_product.note)
                elif operate_type == cv.undo_return:
                    # 取消 退货。
                    opCode = prod["orderOpCode"]
                    orderStat = 0
                    purchaseNum = prod["purchaseNum"]
                    purchasePrice = prod["purchasePrice"]
                    supplier = prod["supplier"]
                    settlement = prod["settlement"]
                    # 退货。
                    sql = "select count(*) from Stock_Product_Order_App where orderID=? and orderStat = -1"
                    cursor.execute(sql, orderID)
                    row = cursor.fetchone()
                    cc = row[0]
                    if cc == 1:
                        sql = "update Stock_Product_Order_App set orderStat=? where orderID=?"
                        print(operate_type, "update sql --- \n ", sql)
                        cursor.execute(sql,  orderStat, orderID)
                        sql = "update [FTPart_Stock_Product_Property_1] " \
                              "set [其它.app允采购量] = [其它.app允采购量] - ?, " \
                              "[其它.app采购量] = [其它.app采购量] + ? " \
                              "where [MainID]=?"
                        cursor.execute(sql, purchaseNum, purchaseNum, stockProductID)
                        print(operate_type, "update sql2 ---\n ", sql)
                        # [Stock_Product_InfoBase].unitprice 更新单价
                        # [Stock_Product_Info].goodsnum 更新采购量，为0是要设置为允采购量，因为系统不能设置为0。
                        sql = "select sum(ordernum*orderStat) as goodsnum,sum(ordernum*orderprice*orderStat) as allprice " \
                              "from Stock_Product_Order_App " \
                              "where stockProductID = ? and (orderStat = -1 or orderStat = 1)"
                        cursor.execute(sql, stockProductID)
                        row = cursor.fetchone()
                        goodsnum = row[0]
                        allprice = row[1]
                        if goodsnum == 0:
                            unitprice = 0
                        else:
                            unitprice = allprice / goodsnum
                        print("写入erp数据库", stockProductID, unitprice, goodsnum)
                        sql = "update Stock_Product_InfoBase set unitprice=? where stockProductID = ?"
                        cursor.execute(sql, unitprice, stockProductID)
                        sql = "update Stock_Product_Info set goodsnum=? where stockProductID = ?"
                        cursor.execute(sql, goodsnum, stockProductID)
                        # insert history row
                        sql = "insert INTO Stock_Product_Order_App_hist(StockProductID, OpCode, OrderNum,OrderPrice," \
                              " supplier, OperateType, orderId, note) VALUES(?,?,?,?,?,?,?,?)"
                        print(operate_type, "insert hist sql --- \n ", sql)
                        cursor.execute(sql, stockProductID, opCode, purchaseNum, 0.0, '', cv.undo_return, orderID, '')
                        cursor.commit()
                        result_product.note = "1:取消退货成功"
                    else:
                        result_product.note = "0:" + operate_type + " 没有记录."
                elif operate_type == cv.settlement_goods:
                    settlementOpCode = prod["settlementOpCode"]
                    # 结算
                    purchaseNum = prod["purchaseNum"]
                    purchasePrice = prod["purchasePrice"]
                    supplier = prod["supplier"]
                    settlement = prod["settlement"]
                    settlement = 2
                    sql = "update Stock_Product_Order_App " \
                          "set settlementOpCode = ?, settlement=?,settlementTime=getdate() " \
                          "where orderID = ? and stockProductID = ? and settlement <> ? "
                    print(operate_type, "update sql ---\n ", sql)
                    cursor.execute(sql, settlementOpCode, settlement, orderID, stockProductID, settlement)
                    # insert history row
                    sql = "insert INTO Stock_Product_Order_App_hist(StockProductID, OpCode, OrderNum,OrderPrice," \
                          " supplier, OperateType, orderId, note) VALUES(?,?,?,?,?,?,?,?)"
                    print(operate_type, "insert hist sql --- \n ", sql)
                    cursor.execute(sql, stockProductID, settlementOpCode, purchaseNum, purchasePrice, supplier,
                                   cv.settlement_goods, orderID, '')
                    cursor.commit()
                    result_product.note = "1:结算成功"
                result_product_list.append(result_product)
            cursor.close
            cnxn.close
            return result_product_list
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
            cnxn.rollback()
            return result_product_list

    def parse_account_product_cursor(self, row):
        # [accountID]
        # , [batchNo]
        # , [orderID]
        # , [StockProductID]
        # , [OpCode]
        # , [OrderNum]
        # , [OrderPrice]
        # , [Settlement]
        # , [supplier]
        # , [CreateTime]
        # , [accountNum]
        # , [accountStat]
        product = AccountProductInfo()
        product.accountID = row[1]
        product.batchNo = row[2]
        product.orderID = row[3]
        product.StockProductID = row[4]
        product.accountOpCode = row[5]
        product.orderNum = row[6]
        product.orderPrice = row[7]
        product.settlement = row[8]
        product.supplier = row[9]
        product.createTime = row[10]
        product.accountNum = row[11]
        product.accountStat = row[12]
        return product

    def select_account_product(self, page_no, filter_account, ptype):
        # 检索 所有的 对账记录
        # 订单号 orderID
        # 批号 batchNo
        # 状态 取消，或正常
        #
        try:
            account_product_list = []
            page_prod_count = 10
            cnxn = pyodbc.connect(self._conn_str)
            cursor = cnxn.cursor()
            # 数据源
            v_sql = "SELECT [accountID], [batchNo], [orderID], [StockProductID], [OpCode], [OrderNum], [OrderPrice], [Settlement], [supplier],CONVERT(varchar, CreateTime, 120) AS CreateTime, [accountNum], [accountStat] FROM [Stock_Product_Order_Account_App] where 0=0 "
            v_time_column = "CreateTime"

            filter_orderID = filter_account["orderID"]
            if filter_orderID is not None:
                v_sql = v_sql + " and orderID =" + filter_orderID + ""
            filter_batchNo = filter_account["batchNo"]
            if filter_batchNo is not None:
                v_sql = v_sql + " and batchNo = '" + filter_batchNo + "'"

            # 过滤条件，商品描述
            filter_GoodsCDesc = filter_account["goodsDesc"]
            if filter_GoodsCDesc is not None:
                v_sql = v_sql + " and orderID in (select product_order_id from v_app_stock_order  where GoodsCDesc like '%" + filter_GoodsCDesc + "%')"
            filter_brand = filter_account["brand"]
            if filter_brand is not None:
                filter_sql = ''
                for b in filter_brand:
                    filter_sql = filter_sql + "'" + b + "',"
                filter_sql = filter_sql.rstrip(',')
                v_sql = v_sql + " and orderID in (select product_order_id from v_app_stock_order  where [其它.商品品牌] in (" + filter_sql + "))"
            # begin date
            filter_begin = filter_account["begin"]
            if filter_begin is not None:
                v_sql = v_sql + "  and orderID in (select product_order_id from v_app_stock_order  where " + v_time_column + " >= '" + filter_begin + "')"
            # end data
            filter_end = filter_account["end"]
            if filter_end is not None:
                v_sql = v_sql + "  and orderID in (select product_order_id from v_app_stock_order  where " + v_time_column + "<= '" + filter_end + " 23:59:59')"
            filter_supplier = filter_account["supplier"]
            if filter_supplier is not None:
                filter_sql = ''
                for b in filter_supplier:
                    filter_sql = filter_sql + "'" + b + "',"
                filter_sql = filter_sql.rstrip(',')
                v_sql = v_sql + "  and orderID in (select product_order_id from v_app_stock_order  where supplier in (" + filter_sql + "))"
            filter_specno = filter_account["specno"]
            if filter_specno is not None:
                v_sql = v_sql + "  and orderID in (select product_order_id from v_app_stock_order  where SpecNo = '" + filter_specno + "')"

            # 先总数
            product_count = 0
            topN = page_no*page_prod_count
            # 再分页，需要增加排序功能
            v_sql = "select row_number() over(order by v." + v_time_column + " desc,v.accountid desc) as rownumber,  v.* ,count(*) over() as product_count from (" + v_sql + ") as v"
            v_sql = "select * from (" + v_sql + ") as v1 where v1.rownumber > " + str(topN - page_prod_count) + " and v1.rownumber <= " + str(topN) + " order by v1.rownumber"
            print(ptype, "sql page is ", v_sql)
            cursor.execute(v_sql)
            orderID_set = set()
            for row in cursor:
                product = self.parse_account_product_cursor(row)
                product_count = row[len(row)-1]
                account_product_list.append(product)
                orderID_set.add(product.orderID)
            orderID_list_str = ""
            for orderID in orderID_set:
                orderID_list_str = orderID_list_str + "," + str(orderID)
            print("orderID_list_str", orderID_list_str.lstrip(","))
            v_sql = "select 0 as rownumber,  v.* ,count(*) over() as product_count from v_app_stock_order as v where v.product_order_id in (" + orderID_list_str.lstrip(",") +")"
            cursor.execute(v_sql)
            product_list = []
            for row in cursor:
                parent_product = self.parse_product_cursor(row)
                product_list.append(parent_product)
            cursor.close()
            cnxn.close()
            return account_product_list, product_count, product_list
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
            return None, 0, None

    def merge_account_product(self, account_prod_dict_list, operate_type):
        try:
            result_product_list = []
            cnxn = pyodbc.connect(self._conn_str)
            cursor = cnxn.cursor()
            for prod in account_prod_dict_list:
                print("account product batchNo =", prod["batchNo"], prod["accountID"], prod["orderID"], prod["stockProductID"])
                # 全局数据
                accountID = prod["accountID"]
                batchNo = prod["batchNo"]
                orderID = prod["orderID"]
                stockProductID = prod["stockProductID"]
                accountNum = prod["purchaseNum"]
                accountOpCode = prod["accountOpCode"]

                # 返回结果集
                result_product = AccountProductInfo()
                result_product.accountID = accountID
                result_product.orderID = orderID
                result_product.StockProductID = stockProductID
                result_product.accountNum = accountNum
                result_product.note = "0:" + operate_type + " failure."

                if operate_type == cv.account_goods:
                    accountStat = 1
                    sql = "INSERT INTO [Stock_Product_Order_Account_App](batchNo,[orderID], [StockProductID], [OpCode], [OrderNum], [OrderPrice], [Settlement], [supplier], [CreateTime], [accountNum], [accountStat]) SELECT ?, [orderID], [StockProductID], ?, [OrderNum], [OrderPrice]	, [Settlement], [supplier], getdate(), ?, ? FROM [Stock_Product_Order_App] WHERE [orderID] = ?"
                    print(operate_type, "insert sql ---\n ", sql)
                    cursor.execute(sql, batchNo, accountOpCode, accountNum, accountStat, orderID)
                    # insert history row
                    sql = "insert INTO Stock_Product_Order_App_hist(StockProductID, OpCode, OrderNum,OrderPrice," \
                          " supplier, OperateType, orderId, note) VALUES(?,?,?,null,null,?,?,?)"
                    print(operate_type, "insert hist sql --- \n ", sql)
                    cursor.execute(sql, stockProductID, accountOpCode, accountNum, cv.account_goods, orderID, '')
                    cursor.commit()
                    result_product.note = "1:对账成功, 已对账数" + str(accountNum)
                elif operate_type == cv.undo_account:
                    accountStat = 0
                    sql = "update [Stock_Product_Order_Account_App] set [accountStat] = ?  WHERE [accountID] = ? and [accountStat] = 1"
                    print(operate_type, "update sql ---\n ", sql)
                    cursor.execute(sql, accountStat, accountID)
                    # insert history row
                    sql = "insert INTO Stock_Product_Order_App_hist(StockProductID, OpCode, OrderNum,OrderPrice," \
                          " supplier, OperateType, orderId, note) VALUES(?,?,?,?,?,?,?,?)"
                    print(operate_type, "insert hist sql --- \n ", sql)
                    cursor.execute(sql, stockProductID, accountOpCode, 0, 0.0, '',cv.undo_account, orderID, 'accountID='+str(accountID))
                    cursor.commit()
                    result_product.note = "1:对账取消成功"
                elif operate_type == cv.fullred_goods:
                    settlementOpCode = prod["settlementOpCode"]
                    # 结算
                    purchaseNum = prod["purchaseNum"]
                    purchasePrice = prod["purchasePrice"]
                    supplier = prod["supplier"]
                    settlement = prod["settlement"]
                    settlement = 2
                    sql = "update Stock_Product_Order_App " \
                          "set settlementOpCode = ?, settlement=?,settlementTime=getdate() " \
                          "where orderID = ? and stockProductID = ? and settlement <> ? "
                    print(operate_type, "update sql ---\n ", sql)
                    cursor.execute(sql, settlementOpCode, settlement, orderID, stockProductID, settlement)
                    # insert history row
                    sql = "insert INTO Stock_Product_Order_App_hist(StockProductID, OpCode, OrderNum,OrderPrice," \
                          " supplier, OperateType, orderId, note) VALUES(?,?,?,null,null,?,?,?)"
                    print(operate_type, "insert hist sql --- \n ", sql)
                    cursor.execute(sql, stockProductID, settlementOpCode, supplier, cv.settlement_goods, orderID, '')
                    cursor.commit()
                    result_product.note = "1:充红成功"
                result_product_list.append(result_product)
            cursor.close
            cnxn.close
            return result_product_list
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
            cnxn.rollback()
            return result_product_list

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
