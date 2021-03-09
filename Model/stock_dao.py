# -*- coding: utf-8 -*-
import configparser
import traceback
import sys
import os
import pyodbc
import datetime
import base64
from Model.user import UserInfo
from Model.product import ProductInfo, AccountProductInfo, AccountBatchNo, ProductEnquiryPrice, OrderpriceInfo
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

            # 过滤条件，销售合同号
            filter_contractNo = filter_stock["contractNo"]
            if filter_contractNo is not None:
                v_sql = v_sql + " and contractNo like '%" + filter_contractNo + "%'"
            # 过滤条件，商品规格
            filter_specNo = filter_stock["specNo"]
            if filter_specNo is not None:
                v_sql = v_sql + " and specNo like '%" + filter_specNo + "%'"
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
                product.stockProductID = row[2]
                product.ProductID = row[3]
                product.SignDate = row[4]
                product.GoodsCode = row[5]
                product.specNo = row[6]
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
                # 销售合同号
                product.contractNo = row[23]
                # 采购价格历史记录
                product.orderpriceList = []
                # 总数
                product_count = row[24]
                product_list.append(product)
            for product in product_list:
                stockProductID = product.stockProductID
                orderpriceProds = []
                # 数据源
                v_sql_basic = "SELECT orderID,stockProductID,OpCode,OrderNum,OrderPrice,supplier,CONVERT(varchar, CreateTime, 120) as CreateTime, CONVERT(varchar, ensureTime, 120) as ensureTime,ensureOpCode " \
                              " FROM Stock_Product_Order_App  where  OrderStat = 1 and Settlement > 0 "
                v_sql_basic = v_sql_basic + "and stockProductID = " + str(stockProductID)
                v_sql = "select top 1 1 as rowno, v.* from (" + v_sql_basic + ") as v order by ensureTime desc"
                cursor.execute(v_sql)
                for row in cursor:
                    orderprice = self.parse_orderprice_product_cursor(row)
                    orderprice.ptype = cv.orderprice_top1_time
                    orderpriceProds.append(orderprice.desc())
                v_sql = "select top 1 1 as rowno, v.* from (" + v_sql_basic + ") as v order by OrderPrice asc"
                cursor.execute(v_sql)
                for row in cursor:
                    orderprice = self.parse_orderprice_product_cursor(row)
                    orderprice.ptype = cv.orderprice_top1_price
                    orderpriceProds.append(orderprice.desc())
                product.orderpriceList = orderpriceProds
                print("orderpriceProds is ", stockProductID, orderpriceProds)
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
        product.stockProductID = row[2]
        product.ProductID = row[3]
        product.SignDate = row[4]
        product.GoodsCode = row[5]
        product.specNo = row[6]
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
        # 主键，商品采购记录ID
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
        product.returnNum = row[37]
        product.contractNo = row[38]
        product.orderPriceAccpt = row[39]
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
                v_sql = v_sql + "and settlement = 1 and OrderStat = 1 and orderNum > accountNum + returnNum"
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
            elif ptype == cv.fullred_goods:
                v_sql = v_sql + "and settlement = 2 and OrderStat = 1 and exists(select 1 from Stock_Product_Order_Account_fullred_App a where a.orderID = v_app_stock_order.product_order_id)"
                v_time_column = "CreateTime"
            elif ptype == cv.history_goods:
                v_sql = v_sql + " and settlement >= 0 and OrderStat = 1"
            else:
                v_sql = v_sql + " and settlement = 0 and OrderStat = 1"

            # 过滤条件，是否已经对账过部分，
            filter_will_account = filter_stock["willAccount"]
            if filter_will_account is not None:
                # 没有对账过 为 1
                if filter_will_account == '1':
                    v_sql = v_sql + " and not exists(select 1 from Stock_Product_Order_Account_App a where a.orderID = v_app_stock_order.product_order_id and a.accountStat = 1)"
                elif filter_will_account == '2':
                    v_sql = v_sql + " and exists(select 1 from Stock_Product_Order_Account_App a where a.orderID = v_app_stock_order.product_order_id and a.accountStat = 1)"
            # 过滤条件，销售合同号
            filter_contractNo = filter_stock["contractNo"]
            if filter_contractNo is not None:
                v_sql = v_sql + " and contractNo like '%" + filter_contractNo + "%'"
            # 过滤条件，商品规格
            filter_specNo = filter_stock["specNo"]
            if filter_specNo is not None:
                v_sql = v_sql + " and specNo like '%" + filter_specNo + "%'"
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
                    if product.returnNum == 0:
                        continue
                    v_sql = ""
                    if ptype == cv.history_goods:
                        v_sql = "select * from v_app_stock_order  where (orderstat=-1 or orderstat=0) and sourceOrderID=" + str(product.orderID)
                    else:
                        v_sql = "select * from v_app_stock_order  where orderstat=-1 and sourceOrderID=" + str(product.orderID)
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
            elif ptype == cv.fullred_goods:
                for product in product_list:
                    v_sql = "select fullredNum from Stock_Product_Order_Account_fullred_App  where orderid = ? "
                    print(ptype, "sql fullred is ", v_sql)
                    cursor.execute(v_sql, product.orderID)
                    row = cursor.fetchone()
                    if row is not None:
                        product.orderNum = row[0]
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
                orderPriceAccpt = prod["orderPriceAccpt"]
                # 訂貨
                settlement = 0

                result_product = ProductInfo()
                result_product.stockProductID = stockProductID

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
                          "supplier, settlement, orderPriceAccpt) " \
                          " values(?,?,?,?,?,?,?,?)"
                    print("add order", "insert Stock_Product_Order_App sql is ", sql)
                    cursor.execute(sql, stockProductID, opCode, purchaseNum, purchasePrice, orderStat, supplier, settlement, orderPriceAccpt)
                    sql = "select @@IDENTITY"
                    cursor.execute(sql)
                    lastOrderID = cursor.fetchone()[0] # 生成的主键字段值。
                    sql = "insert INTO Stock_Product_Order_App_hist(stockProductID, OpCode, OrderNum," \
                          "OrderPrice, supplier, OperateType, orderId, note, orderPriceAccpt) " \
                          "VALUES(?,?,?,?,?,?,?,?,?)"
                    cursor.execute(sql, stockProductID, opCode, purchaseNum, purchasePrice, supplier, 'order', lastOrderID, '', orderPriceAccpt)
                    cursor.commit()
                    result_product.note = "1:采购成功"
                else:
                    result_product.note = "0:采购失败, 允购量 " + str(permitNum) + ", 采购量 " + str(purchaseNum)
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
                result_product.stockProductID = stockProductID
                result_product.orderID = orderID
                result_product.note = "0:" + operate_type + " failure."

                if operate_type == cv.cancel_order:

                    # 取消订货
                    opCode = prod["orderOpCode"]
                    # 退货数量，不是全退，可以退货一部分，最大不超过原来的购买量。
                    purchaseNum = prod["purchaseNum"]
                    # 更新状态码为0，然后 写入历史表。
                    orderStat = 0

                    sql = "select stockProductID, OrderNum, OrderPrice,supplier, settlement, orderPriceAccpt " \
                          "from Stock_Product_Order_App where orderID=?"
                    cursor.execute(sql, orderID)
                    row = cursor.fetchone()
                    if row is not None:
                        stockProductID = row[0]
                        orderNum = row[1]
                        purchasePrice = row[2]
                        supplier = row[3]
                        settlement = row[4]
                        orderPriceAccpt = row[5]
                        if orderNum >= purchaseNum:
                            # 退货量的判断。
                            if orderNum == purchaseNum:
                                # 全退
                                # 取消订货。
                                sql = "update Stock_Product_Order_App set orderStat= ? where orderID=?"
                                cursor.execute(sql, orderStat, orderID)
                            elif orderNum > purchaseNum:
                                # 退部分
                                # 取消订货，更新剩余量。
                                sql = "update Stock_Product_Order_App set  orderNum= ? where orderID=?"
                                cursor.execute(sql,  orderNum - purchaseNum, orderID)
                            # 修改 app允采购量
                            sql = "update [FTPart_Stock_Product_Property_1] " \
                                  "set [其它.app允采购量] = [其它.app允采购量] + ?, " \
                                  "[其它.app采购量] = [其它.app采购量] - ?" \
                                  " where [MainID] = ?"
                            cursor.execute(sql, purchaseNum, purchaseNum, stockProductID)
                            # insert history row
                            sql = "insert INTO Stock_Product_Order_App_hist(stockProductID, OpCode, OrderNum,OrderPrice," \
                                  " supplier, OperateType, orderId, note, orderPriceAccpt) VALUES(?,?,?,?,?,?,?,?,?)"
                            print(operate_type, "insert hist sql --- \n ", sql)
                            cursor.execute(sql, stockProductID, opCode, purchaseNum, purchasePrice,
                                           supplier, cv.cancel_order, orderID, '',orderPriceAccpt)
                            cursor.commit()
                            result_product.note = "1:取消订货成功" + ":" + str(orderNum - purchaseNum)
                    else:
                        result_product.note = "0:取消订货数量异常" + ":" + str(orderNum)
                elif operate_type == cv.complete_order:
                    # 确认订货，完成采购
                    ensureOpCode = prod["ensureOpCode"]
                    purchaseNum = prod["purchaseNum"]
                    purchasePrice = prod["purchasePrice"]
                    # 订货 或者 退货
                    orderStat = prod["orderStat"]
                    supplier = prod["supplier"]
                    settlement = prod["settlement"]
                    orderPriceAccpt = prod["orderPriceAccpt"]
                    # 订货确认。
                    settlement = 1
                    sql = "select stockProductID,OpCode, orderNum,OrderPrice,supplier,orderPriceAccpt  from Stock_Product_Order_App where orderID = ? and stockProductID = ? and settlement <> ?"
                    cursor.execute(sql, orderID, stockProductID, settlement)
                    row = cursor.fetchone()
                    orderNum = purchaseNum
                    if row is not None:
                        orderNum = row[2]
                        if orderNum >= purchaseNum:
                            if orderNum > purchaseNum:
                                sql = "insert into Stock_Product_Order_App(stockProductID,OpCode, orderNum,OrderPrice,supplier,orderPriceAccpt, createtime, ensuretime, settlement) select stockProductID,?, ?, ?, supplier,orderPriceAccpt,createtime, getdate(), ? from Stock_Product_Order_App where orderID = ? "
                                cursor.execute(sql, ensureOpCode, purchaseNum, purchasePrice, settlement, orderID)
                                sql = "update Stock_Product_Order_App " \
                                      "set orderNum = ?, OrderPrice = ?, orderPriceAccpt=? " \
                                      ",ensureTime=getdate() " \
                                      "where orderID = ? and stockProductID = ? and settlement <> ? "
                                print(operate_type, "update sql ---\n ", sql, "other ordernum is ",orderNum - purchaseNum)
                                cursor.execute(sql, orderNum - purchaseNum, purchasePrice,orderPriceAccpt, orderID, stockProductID, settlement)
                            elif orderNum == purchaseNum:
                                sql = "update Stock_Product_Order_App " \
                                      "set ensureOpCode = ?,settlement=?, orderNum = ?, OrderPrice = ?, orderPriceAccpt=? " \
                                      ",ensureTime=getdate() " \
                                      "where orderID = ? and stockProductID = ? and settlement <> ? "
                                print(operate_type, "update sql ---\n ", sql, "ordernum is ", purchaseNum)
                                cursor.execute(sql, ensureOpCode, settlement, purchaseNum, purchasePrice,
                                               orderPriceAccpt, orderID, stockProductID, settlement)
                            # insert history row
                            sql = "insert INTO Stock_Product_Order_App_hist(stockProductID, OpCode, OrderNum," \
                                  "OrderPrice, supplier, OperateType, orderId, note, orderPriceAccpt) " \
                                  "VALUES(?,?,?,?,?,?,?,?,?)"
                            cursor.execute(sql, stockProductID, ensureOpCode, purchaseNum, purchasePrice, supplier,
                                           cv.complete_order, orderID, '', orderPriceAccpt)
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
                                unitprice = allprice / goodsnum
                            print("写入erp数据库", stockProductID, unitprice, goodsnum)
                            sql = "update Stock_Product_InfoBase set unitprice=? where stockProductID = ?"
                            cursor.execute(sql, unitprice, stockProductID)
                            sql = "update Stock_Product_Info set goodsnum=? where stockProductID = ?"
                            cursor.execute(sql, goodsnum, stockProductID)
                            cursor.commit()
                            result_product.note = "1:订货完成成功" + ":" + str(orderNum - purchaseNum)
                        else:
                            result_product.note = "0:订货完成数量异常" + ":" + str(orderNum)
                elif operate_type == cv.return_goods:
                    # 插入一条 退货 记录进来，原订货记录保存。
                    # 退货，有可能是 钱已经预付款了，特例，后面再考虑。
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
                            sql = "insert INTO Stock_Product_Order_App_hist(stockProductID, OpCode, OrderNum,OrderPrice," \
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

                            result_product.note = "1:退货成功，采购量 " + str(doneOrderNum) + ", 退货量 "+str(purchaseNum) + ", 共退货 "+ str(returnOrderNum+purchaseNum) + ":" + str(returnOrderNum+purchaseNum) + ":" + str(doneOrderNum-returnOrderNum-purchaseNum)
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
                        sql = "insert INTO Stock_Product_Order_App_hist(stockProductID, OpCode, OrderNum,OrderPrice," \
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
                    orderPriceAccpt = 1
                    settlement = 2
                    # 增加更新对账记录
                    accountID = prod["accountID"]
                    batchNo = prod["batchNo"]

                    sql = "select orderNum from Stock_Product_Order_App  where orderstat =  1 and orderid = ? "
                    cursor.execute(sql, orderID)
                    row = cursor.fetchone()
                    orderNum = row[0]
                    sql = "select sum(orderNum) from Stock_Product_Order_App  where orderstat =  -1 and sourceOrderId = ? "
                    cursor.execute(sql, orderID)
                    row = cursor.fetchone()
                    if row is not None:
                        returnNum = row[0]
                        if returnNum is None:
                            returnNum = 0
                    else:
                        returnNum = 0
                    sql = "select sum(accountNum) from Stock_Product_Order_Account_App  where orderid = ? and accountStat = 1"
                    cursor.execute(sql, orderID)
                    print("select accountNum sum is ", sql, orderID)
                    row = cursor.fetchone()
                    if row is not None:
                        accountNum = row[0]
                        if accountNum is None:
                            accountNum = 0
                    else:
                        accountNum = 0
                    print("orderNum is ", orderNum, "returnNum is ", returnNum, "accountNum is ", accountNum)
                    fullredNum = 0
                    # orderNum = returnNum + accountNum 则正常，否则需要充红。
                    fullredNum = orderNum - returnNum - accountNum
                    note = "结算成功, " + "已采购:" + str(orderNum) + " = 结算:" + str(accountNum) + ' + 退货:' + str(returnNum)
                    if fullredNum > 0:
                        note = note + "+ 充红:" + str(fullredNum)
                    elif fullredNum < 0:
                        note = "结算异常, " + "已采购:" + str(orderNum) + " != 结算:" + str(accountNum) + ' + 退货:' + str(returnNum)

                    sql = "UPDATE [Stock_Product_Order_Account_App] SET [Settlement] = 2  WHERE accountID = ? "
                    print(operate_type, "update Stock_Product_Order_Account_App sql ---\n ", sql, settlement, accountID)
                    cursor.execute(sql, accountID)

                    sql = "update Stock_Product_Order_App " \
                          "set settlementOpCode = ?, settlement=?,settlementTime=getdate() " \
                          "where orderID = ? and stockProductID = ? and settlement <> ? "
                    print(operate_type, "update sql ---\n ", sql, settlement, orderID, stockProductID )
                    cursor.execute(sql, settlementOpCode, settlement, orderID, stockProductID, settlement)

                    if fullredNum > 0:
                        sql = "select fullredNum from Stock_Product_Order_Account_fullred_App  where orderid = ? "
                        cursor.execute(sql, orderID)
                        row = cursor.fetchone()
                        if row is None:
                            sql = "INSERT INTO [Stock_Product_Order_Account_fullred_App]([accountID],[batchNo],[orderID],[stockProductID],[OpCode],[CreateTime],[fullredNum],[fullredStat],[note]) VALUES(?,?,?,?,?,getdate(),?,0,'')"
                            print("fullred sql --- \n", sql)
                            cursor.execute(sql, accountID, batchNo, orderID, stockProductID, settlementOpCode, fullredNum)
                    # insert history row
                    sql = "insert INTO Stock_Product_Order_App_hist(stockProductID, OpCode, OrderNum,OrderPrice," \
                          " supplier, OperateType, orderId, note, orderPriceAccpt) VALUES(?,?,?,?,?,?,?,?,?)"
                    print(operate_type, "insert hist sql --- \n ", sql)
                    cursor.execute(sql, stockProductID, settlementOpCode, purchaseNum, purchasePrice, supplier,
                                   cv.settlement_goods, orderID, note, orderPriceAccpt)

                    cursor.commit()
                    result_product.batchNo = batchNo
                    result_product.note = "1:" + note + " （结算,退货,采购,充红）:" + str(accountNum) + ":" + str(returnNum) + ":" + str(orderNum) + ":" + str(fullredNum)
                    result_product.settlement = 2
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

    def update_product_orderprice(self, prod_dict_list, operate_type):
        try:
            result_product_list = []
            cnxn = pyodbc.connect(self._conn_str)
            cursor = cnxn.cursor()
            for prod in prod_dict_list:
                print("orderprice product id=", prod["orderID"], prod["stockProductID"], "orderPriceAccpt is ", prod["orderPriceAccpt"], prod["purchasePrice"] )
                # 全局数据, 传入的参数值。
                orderID = prod["orderID"]
                stockProductID = prod["stockProductID"]
                orderPriceAccpt = prod["orderPriceAccpt"]
                purchasePrice = prod["purchasePrice"]
                opCode = prod["opCode"]

                # 返回结果集
                result_product = ProductInfo()
                result_product.stockProductID = stockProductID
                result_product.orderID = orderID
                result_product.note = "0:" + operate_type + " 价格状态修改为" + str(orderPriceAccpt) + " 失败"

                if operate_type == cv.order_price:
                    # 价格确认
                    sql = "update Stock_Product_Order_App set orderPriceAccpt = ?, OrderPrice = ?  where orderID=?"
                    cursor.execute(sql, orderPriceAccpt, purchasePrice, orderID)
                    print(sql, orderPriceAccpt, purchasePrice, orderID)
                    sql = "select stockProductID, OrderNum, OrderPrice,supplier, settlement, orderPriceAccpt " \
                          "from Stock_Product_Order_App where orderID=?"
                    cursor.execute(sql, orderID)
                    row = cursor.fetchone()
                    if row is not None:
                        stockProductID = row[0]
                        orderNum = row[1]
                        orderPrice = row[2]
                        supplier = row[3]
                        settlement = row[4]
                        orderPriceAccpt = row[5]
                        # insert history row
                        sql = "insert INTO Stock_Product_Order_App_hist(stockProductID, OpCode, OrderNum,OrderPrice," \
                              " supplier, OperateType, orderId, note, orderPriceAccpt) VALUES(?,?,?,?,?,?,?,?,?)"
                        print(operate_type, "insert hist sql --- \n ", sql)
                        cursor.execute(sql, stockProductID, opCode, orderNum, orderPrice,
                                       supplier, cv.cancel_order, orderID, '', orderPriceAccpt)
                        # [Stock_Product_InfoBase].unitprice 更新单价
                        # [Stock_Product_Info].goodsnum 更新采购量，为0是要设置为允采购量，因为系统不能设置为0。
                        sql = "select sum(ordernum*orderStat) as goodsnum,sum(ordernum*orderprice*orderStat) as allprice " \
                              "from Stock_Product_Order_App " \
                              "where stockProductID = ? and (orderStat = -1 or orderStat = 1) and settlement >= 1"
                        cursor.execute(sql, stockProductID)
                        row = cursor.fetchone()
                        if row is not None and row[0] is not None and row[1] is not None:
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
                        result_product.orderPrice = orderPrice
                        result_product.orderPriceAccpt = orderPriceAccpt
                        result_product.note = "1:价格状态修改为" + str(orderPriceAccpt) + " 成功"
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
        product = AccountProductInfo()
        product.accountID = row[1]
        product.batchNo = row[2]
        product.orderID = row[3]
        product.stockProductID = row[4]
        product.accountOpCode = row[5]
        product.orderNum = row[6]
        product.orderPrice = row[7]
        product.settlement = row[8]
        product.supplier = row[9]
        product.createTime = row[10]
        product.accountNum = row[11]
        product.accountStat = row[12]
        product.returnNum = row[13]
        return product

    def select_presettlement_product(self, page_no, query_params, ptype):
        # 检索 所有的 对账 数据异常（已采购量 != 退货 + 对账 ），需要取消对账或者充红的商品
        # 批号 batchNo
        #
        #
        try:
            account_product_list = []
            page_prod_count = 10
            cnxn = pyodbc.connect(self._conn_str)
            cursor = cnxn.cursor()
            # 数据源
            v_sql = "SELECT a.accountID, a.batchNo, a.orderID, a.stockProductID, a.OpCode, a.OrderNum, a.OrderPrice, a.Settlement, a.supplier,CONVERT(varchar, CreateTime, 120) AS CreateTime, a.accountNum, a.accountStat ,coalesce(b.OrderNum,0) as returnNum " \
                    " FROM Stock_Product_Order_Account_App as a left join (select sourceOrderId, ordernum from Stock_Product_Order_App where orderstat = -1) b on a.orderID = b.sourceOrderId " \
                    " where a.accountStat = 1 and a.OrderNum != a.accountNum + coalesce(b.OrderNum,0) "
            v_time_column = "CreateTime"

            filter_batchNo = query_params["batchNo"]
            if filter_batchNo is not None:
                v_sql = v_sql + " and a.batchNo = '" + filter_batchNo + "'"

            # 过滤条件，商品描述

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
            orderID_list_str = "0"
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

    def select_account_product(self, page_no, query_params, ptype):
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
            v_sql = "SELECT [accountID], [batchNo], [orderID], [stockProductID], [OpCode], [OrderNum], [OrderPrice], [Settlement], [supplier],CONVERT(varchar, CreateTime, 120) AS CreateTime, [accountNum], [accountStat] FROM [Stock_Product_Order_Account_App] where accountStat = 1"
            v_sql = "select * from (SELECT a.accountID, a.batchNo, a.orderID, a.stockProductID, a.OpCode, a.OrderNum, a.OrderPrice, a.Settlement, a.supplier,CONVERT(varchar, CreateTime, 120) AS CreateTime, a.accountNum, a.accountStat ,coalesce(b.OrderNum,0) as returnNum " \
                    " FROM Stock_Product_Order_Account_App as a left join (select sourceOrderId, ordernum from Stock_Product_Order_App where orderstat = -1) b on a.orderID = b.sourceOrderId " \
                    " where a.accountStat = 1) as v where 1=1"
            v_time_column = "CreateTime"

            filter_orderID = query_params["orderID"]
            if filter_orderID is not None:
                v_sql = v_sql + " and orderID =" + filter_orderID + ""
            filter_batchNo = query_params["batchNo"]
            if filter_batchNo is not None:
                v_sql = v_sql + " and batchNo = '" + filter_batchNo + "'"

            # 过滤条件，商品描述
            filter_GoodsCDesc = query_params["goodsDesc"]
            if filter_GoodsCDesc is not None:
                v_sql = v_sql + " and orderID in (select product_order_id from v_app_stock_order  where GoodsCDesc like '%" + filter_GoodsCDesc + "%')"
            filter_brand = query_params["brand"]
            if filter_brand is not None:
                filter_sql = ''
                for b in filter_brand:
                    filter_sql = filter_sql + "'" + b + "',"
                filter_sql = filter_sql.rstrip(',')
                v_sql = v_sql + " and orderID in (select product_order_id from v_app_stock_order  where [其它.商品品牌] in (" + filter_sql + "))"
            # begin date
            filter_begin = query_params["begin"]
            if filter_begin is not None:
                v_sql = v_sql + "  and orderID in (select product_order_id from v_app_stock_order  where " + v_time_column + " >= '" + filter_begin + "')"
            # end data
            filter_end = query_params["end"]
            if filter_end is not None:
                v_sql = v_sql + "  and orderID in (select product_order_id from v_app_stock_order  where " + v_time_column + "<= '" + filter_end + " 23:59:59')"
            filter_supplier = query_params["supplier"]
            if filter_supplier is not None:
                filter_sql = ''
                for b in filter_supplier:
                    filter_sql = filter_sql + "'" + b + "',"
                filter_sql = filter_sql.rstrip(',')
                v_sql = v_sql + "  and orderID in (select product_order_id from v_app_stock_order  where supplier in (" + filter_sql + "))"
            filter_specNo = query_params["specNo"]
            if filter_specNo is not None:
                v_sql = v_sql + "  and orderID in (select product_order_id from v_app_stock_order  where specNo = '" + filter_specNo + "')"

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

    def select_account_batchno(self, page_no, query_params, ptype):
        # 检索 所有的 对账批号
        # 批号 batchNo
        #
        try:
            print("query_params is ", query_params)
            account_batchNo_list = []
            page_prod_count = 10000
            cnxn = pyodbc.connect(self._conn_str)
            cursor = cnxn.cursor()
            # 数据源

            v_sql = "SELECT distinct [batchNo], CONVERT(varchar, min(CreateTime) over(partition by [batchNo]), 120) AS CreateTime, count(*) over(partition by [batchNo]) as batchProdCount, note,settlement  FROM [Stock_Product_Order_Account_App] where accountStat = 1"

            if ptype == cv.batchno_list:
                v_sql = v_sql + " and settlement != 2"
                # 只搜 已对账的商品，已结算的不算。
            elif ptype == cv.account_goods:
                v_sql = v_sql + " and settlement != 2"
            elif ptype == cv.settlement_goods:
                v_sql = v_sql + " and settlement = 2 and batchNo not in (select batchNo from [Stock_Product_Order_Account_App] where  accountStat = 1 and settlement = 1)"

            filter_batchNo = query_params["batchNo"]
            if filter_batchNo is not None:
                v_sql = v_sql + " and batchNo = '" + filter_batchNo + "'"
            filter_note = query_params["note"]
            if filter_note is not None:
                v_sql = v_sql + " and note like '%" + filter_note + "%'"
            # begin date
            filter_begin = query_params["begin"]
            if filter_begin is not None:
                v_sql = v_sql + " and CreateTime >= '" + filter_begin + "'"
            # end data
            filter_end = query_params["end"]
            if filter_end is not None:
                v_sql = v_sql + " and CreateTime <= '" + filter_end + " 23:59:59'"

            # 先总数
            product_count = 0
            topN = page_no*page_prod_count
            # 再分页，需要增加排序功能
            v_sql = "select row_number() over(order by v.CreateTime desc) as rownumber,  v.* ,count(*) over() as product_count from (" + v_sql + ") as v"
            v_sql = "select * from (" + v_sql + ") as v1 where v1.rownumber > " + str(topN - page_prod_count) + " and v1.rownumber <= " + str(topN) + " order by v1.rownumber"
            print(ptype, "sql page is ", v_sql)
            cursor.execute(v_sql)
            for row in cursor:
                product = AccountBatchNo()
                product.batchNo = row[1]
                product.createTime = row[2]
                product.batchProdCount = row[3]
                product.note = row[4]
                product.settlement = row[5]
                product_count = row[len(row)-1]
                account_batchNo_list.append(product)
            cursor.close()
            cnxn.close()
            return account_batchNo_list, product_count
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

    def select_account_note(self, query_params):
        try:
            result_product_list = []
            cnxn = pyodbc.connect(self._conn_str)
            cursor = cnxn.cursor()
            sql = "select distinct note,batchNo from Stock_Product_Order_Account_App where accountStat =1 and note=?"
            filter_note = query_params["note"]
            cursor.execute(sql, filter_note)
            print("select_account_note sql is " , sql , filter_note)
            for row in cursor:
                prod = dict()
                prod["note"] = row[0]
                prod["batchNo"] = row[1]
                result_product_list.append(prod)
            return result_product_list, len(result_product_list)
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


    def create_account_product(self, account_prod_dict_list, operate_type):
        try:
            result_product_list = []
            cnxn = pyodbc.connect(self._conn_str)
            cursor = cnxn.cursor()
            for prod in account_prod_dict_list:
                # 全局数据
                batchNo = None
                if prod.__contains__("batchNo"):
                    batchNo = prod["batchNo"]
                accountID = prod["accountID"]
                orderID = prod["orderID"]
                stockProductID = prod["stockProductID"]
                accountNum = prod["purchaseNum"]
                purchasePrice = prod["purchasePrice"]
                accountOpCode = prod["accountOpCode"]
                print("account product batchNo =", batchNo, prod["accountID"], prod["orderID"],
                      prod["stockProductID"])

                # 返回结果集
                result_product = AccountProductInfo()
                result_product.accountID = accountID
                result_product.orderID = orderID
                result_product.stockProductID = stockProductID
                result_product.orderPrice = purchasePrice
                result_product.accountNum = accountNum
                result_product.note = "0:" + operate_type + " failure."

                if operate_type == cv.account_goods:
                    accountStat = 1  # 对账状态 正常
                    note = None
                    if prod.__contains__("note"):
                        note = prod["note"]
                    sql = "select batchNo, note, accountID from Stock_Product_Order_Account_App where accountStat = 1 and orderID = ?"
                    cursor.execute(sql, orderID)
                    row = cursor.fetchone()
                    if row is not None:
                        batchNo = row[0]
                        note = row[1]
                        accountID = row[2]
                        print("补充对账单", note, stockProductID)
                        sql = "update Stock_Product_Order_Account_App set accountNum = accountNum + ? where orderID =? and accountID = ?"
                        print(operate_type, "update sql ---\n ", sql)
                        cursor.execute(sql, accountNum, orderID, accountID)
                    else:
                        if batchNo is None:
                            continue
                            # 没有获取就不能操作
                        print("新增对账单", note, stockProductID)
                        sql = "INSERT INTO [Stock_Product_Order_Account_App](batchNo,[orderID], [stockProductID], [OpCode], [OrderNum], [OrderPrice], [Settlement], [supplier], [CreateTime], [accountNum], [accountStat], [note])" \
                              " SELECT ?, [orderID], [stockProductID], ?, [OrderNum], ? , [Settlement], [supplier], getdate(), ?, ?, ? as nn FROM [Stock_Product_Order_App] WHERE [orderID] = ?"
                        print(operate_type, "insert sql ---\n ", sql)
                        cursor.execute(sql, batchNo, accountOpCode, purchasePrice, accountNum, accountStat, note,
                                       orderID)

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
                    sql = "insert INTO Stock_Product_Order_App_hist(stockProductID, OpCode, OrderNum,OrderPrice," \
                          " supplier, OperateType, orderId, note) VALUES(?,?,?,?,null,?,?,?)"
                    print(operate_type, "insert hist sql --- \n ", sql)
                    cursor.execute(sql, stockProductID, accountOpCode, accountNum, purchasePrice, cv.account_goods, orderID, '')
                    cursor.commit()
                    result_product.note = "1:对账成功, 已对账数:" + str(accountNum)
                elif operate_type == cv.undo_account:
                    accountStat = 0  # 对账状态 取消
                    sql = "update [Stock_Product_Order_Account_App] set [accountStat] = ?  WHERE [accountID] = ? and [accountStat] = 1"
                    print(operate_type, "update sql ---\n ", sql)
                    cursor.execute(sql, accountStat, accountID)
                    # insert history row
                    sql = "insert INTO Stock_Product_Order_App_hist(stockProductID, OpCode, OrderNum,OrderPrice," \
                          " supplier, OperateType, orderId, note) VALUES(?,?,?,?,?,?,?,?)"
                    print(operate_type, "insert hist sql --- \n ", sql)
                    cursor.execute(sql, stockProductID, accountOpCode, 0, 0.0, '', cv.undo_account, orderID, 'accountID=' + str(accountID))
                    cursor.commit()
                    result_product.note = "1:对账取消成功"
                elif operate_type == cv.fullred_goods:
                    settlementOpCode = prod["settlementOpCode"]
                    # 充红 ，代码未开发，需要修改。
                    # purchaseNum = prod["purchaseNum"]
                    # purchasePrice = prod["purchasePrice"]
                    # supplier = prod["supplier"]
                    # settlement = prod["settlement"]
                    # settlement = 2
                    # sql = "update Stock_Product_Order_App " \
                    #       "set settlementOpCode = ?, settlement=?,settlementTime=getdate() " \
                    #       "where orderID = ? and stockProductID = ? and settlement <> ? "
                    # print(operate_type, "update sql ---\n ", sql)
                    # cursor.execute(sql, settlementOpCode, settlement, orderID, stockProductID, settlement)
                    # # insert history row
                    # sql = "insert INTO Stock_Product_Order_App_hist(stockProductID, OpCode, OrderNum,OrderPrice," \
                    #       " supplier, OperateType, orderId, note) VALUES(?,?,?,null,null,?,?,?)"
                    # print(operate_type, "insert hist sql --- \n ", sql)
                    # cursor.execute(sql, stockProductID, settlementOpCode, supplier, cv.settlement_goods, orderID, '')
                    # cursor.commit()
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

    def select_order_account_product_list_by_batchNo(self, batchNo):
        # 检索 所有的 对账记录
        # 订单号 orderID
        # 批号 batchNo
        # 状态 取消，或正常
        #
        try:
            account_product_list = []
            page_no = 1
            page_prod_count = 10000
            cnxn = pyodbc.connect(self._conn_str)
            cursor = cnxn.cursor()
            # 数据源
            v_sql = "SELECT [accountID], [batchNo], [orderID], [stockProductID], [OpCode], [OrderNum], [OrderPrice], [Settlement], [supplier],CONVERT(varchar, CreateTime, 120) AS CreateTime, [accountNum], [accountStat] FROM [Stock_Product_Order_Account_App] where accountStat = 1"
            v_time_column = "CreateTime"
            v_sql = v_sql + " and batchNo = '" + batchNo + "'"

            # 先总数
            product_count = 0
            topN = page_no*page_prod_count
            # 再分页，需要增加排序功能
            v_sql = "select row_number() over(order by v." + v_time_column + " desc,v.accountid desc) as rownumber,  v.* ,count(*) over() as product_count from (" + v_sql + ") as v"
            v_sql = "select * from (" + v_sql + ") as v1 where v1.rownumber > " + str(topN - page_prod_count) + " and v1.rownumber <= " + str(topN) + " order by v1.rownumber"
            print("sql page is ", v_sql, batchNo)
            cursor.execute(v_sql)
            for row in cursor:
                product = self.parse_account_product_cursor(row)
                account_product_list.append(product)
            cursor.close()
            cnxn.close()
            return account_product_list
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

    def batch_update_order_product_settlement(self, batchNo_dict_list, opCode):
        for batch_prod in batchNo_dict_list:
            print("settlement product batchNo =", batch_prod["batchNo"])
            batchNo = batch_prod["batchNo"]
            acct_prod_list = self.select_order_account_product_list_by_batchNo(batchNo)
            account_product_list = []
            for acct_prod in acct_prod_list:
                prod = dict()
                prod["orderID"] = acct_prod.orderID
                prod["stockProductID"] = acct_prod.stockProductID
                prod["settlementOpCode"] = opCode
                prod["purchaseNum"] = acct_prod.accountNum
                prod["purchasePrice"] = acct_prod.orderPrice
                prod["supplier"] = acct_prod.supplier
                prod["settlement"] = acct_prod.settlement
                prod["accountID"] = acct_prod.accountID
                prod["batchNo"] = batchNo
                account_product_list.append(prod)
            print("批量结算，", batchNo, "数量为", len(account_product_list))
            result_list = self.update_stock_product_order(account_product_list, cv.settlement_goods)
            return result_list

    def parse_orderprice_product_cursor(self, row):
        product = OrderpriceInfo()
        product.orderID = row[1]
        product.stockProductID = row[2]
        product.orderOpCode = row[3]
        product.orderNum = row[4]
        product.orderPrice = row[5]
        product.supplier = row[6]
        product.createTime = row[7]
        product.ensureTime = row[8]
        product.ensureOpCode = row[9]
        return product

    def select_product_orderprice_list(self, page_no, query_params, ptypes):
        # 检索 所有的采购商品的询价记录。
        #
        try:
            orderprice_product_list = []
            page_prod_count = 10
            cnxn = pyodbc.connect(self._conn_str)
            cursor = cnxn.cursor()
            # 数据源， 只取 对账过的商品
            v_sql_basic = "SELECT orderID,stockProductID,OpCode,OrderNum,OrderPrice,supplier,CONVERT(varchar, CreateTime, 120) as CreateTime, CONVERT(varchar, ensureTime, 120) as ensureTime,ensureOpCode " \
                    " FROM Stock_Product_Order_App  where  OrderStat = 1 and Settlement > 1 "
            filter_stockProductIDs = query_params["stockProductIDs"]
            if filter_stockProductIDs is not None:
                str_arr = filter_stockProductIDs.split(';')
                filter_id = '(' + ','.join(str_arr) + ')'
                v_sql_basic = v_sql_basic + " and stockProductID in " + filter_id + ""
            filter_specNos = query_params["specNos"]
            if filter_specNos is not None:
                str_arr = filter_specNos.split(';')
                filter_id = '(' + ','.join(str_arr) + ')'
                v_sql_basic = v_sql_basic + " and stockProductID in (select stockProductID from Stock_Product_Info where specNo in " + filter_id + ")"
            # print("v_sql", v_sql)
            # 先总数
            product_count = 0
            topN = page_no * page_prod_count

            ptype_arr = ptypes.split(';')
            for ptype in ptype_arr:
                if ptype == cv.orderprice_top1_time:
                    topN = 1
                    orderby_column = "ensureTime desc"
                    # 再分页，需要增加排序功能
                    v_sql = "select row_number() over(order by v." + orderby_column + " ,v.orderID desc) as rownumber,  v.* ,count(*) over() as product_count from (" + v_sql_basic + ") as v"
                    v_sql = "select * from ( " + v_sql + " ) as v1 where v1.rownumber > 0 and v1.rownumber <=" + str(topN) +  " order by v1.rownumber"
                elif ptype == cv.orderprice_top1_price:
                    topN = 1
                    orderby_column = "OrderPrice asc"
                    # 再分页，需要增加排序功能
                    v_sql = "select row_number() over(order by v." + orderby_column + " ,v.orderID desc) as rownumber,  v.* ,count(*) over() as product_count from (" + v_sql_basic + ") as v"
                    v_sql = "select * from ( " + v_sql + " ) as v1 where v1.rownumber > 0 and v1.rownumber <= " + str(topN) + " order by v1.rownumber"
                elif ptype == cv.orderprice_list_price:
                    orderby_column = "OrderPrice asc"
                    # 再分页，需要增加排序功能
                    v_sql = "select row_number() over(order by v." + orderby_column + " ,v.orderID desc) as rownumber,  v.* ,count(*) over() as product_count from (" + v_sql_basic + ") as v"
                    v_sql = "select * from (" + v_sql + ") as v1 where v1.rownumber > " + str(
                        topN - page_prod_count) + " and v1.rownumber <= " + str(topN) + " order by v1.rownumber"
                elif ptype == cv.orderprice_list_time:
                    orderby_column = "ensureTime desc"
                    # 再分页，需要增加排序功能
                    v_sql = "select row_number() over(order by v." + orderby_column + " ,v.orderID desc) as rownumber,  v.* ,count(*) over() as product_count from (" + v_sql_basic + ") as v"
                    v_sql = "select * from (" + v_sql + ") as v1 where v1.rownumber > " + str(
                        topN - page_prod_count) + " and v1.rownumber <= " + str(topN) + " order by v1.rownumber"

                print(ptypes, "sql page is ", v_sql)
                cursor.execute(v_sql)
                for row in cursor:
                    orderprice_product = self.parse_orderprice_product_cursor(row)
                    orderprice_product.ptype = ptype
                    orderprice_product_list.append(orderprice_product)

            cursor.close()
            cnxn.close()
            return orderprice_product_list, product_count
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
