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
            v_sql_g = "(select [StockProductID], sum([OrderNum]*[OrderStat]) as ordernum from [Stock_Product_Order_App] group by [StockProductID]) as g"
            v_sql_h = "(select max(id) as id, max(createtime) as enquirydate, StockProductID from [Stock_Product_EnquiryPrice_App] group by StockProductID) as h"
            v_sql_columns = "e.[采购人], a.StockProductID,a.ProductID,CONVERT(varchar, d.SignDate, 120 ) as SignDate," \
                            "a.GoodsCode,a.SpecNo,f.GoodsCDesc, a.GoodsUnit, b._ImageID,c.ImageGuid,c.ImageFmt," \
                            "c.ModuleID,CONVERT(varchar, c.FileDate, 120 ) as FileDate,c.ThumbImage,b.[其它.供应商名称]," \
                            "b.[其它.允采购量],b.[其它.应采购价],b.[其它.商品品牌], " \
                            "coalesce(g.ordernum, 0) as ordernum, coalesce(h.id,0) as priceEnquiredID," \
                            "CONVERT(varchar, h.enquirydate, 120 ) as enquirydate  "
            v_sql_fromtab = "FROM [Stock_Product_Info] as a " \
                            "join FTPart_Stock_Product_Property_1 as b on a.StockProductID=b.MainID " \
                            "join Product_Image as c on b._ImageID=c.ProductImageID " \
                            "join stock_info d on d.ID=a.StockID " \
                            "join [FTPart_Stock_Property_1] e on e.[MainID] = d.ID " \
                            "left join [Stock_Product_Info_Desc] f on a.StockProductID=f.StockProductID " \
                            "left join " + v_sql_g + " on a.StockProductID=g.StockProductID  " \
                            "left join " + v_sql_h + " on a.StockProductID=h.StockProductID "
            v_sql = v_sql_columns + v_sql_fromtab + "  where b.[其它.允采购量] > coalesce(g.ordernum, 0) "
            v_sql_cc = "select count(*) as cc " + v_sql_fromtab + "  where b.[其它.允采购量] > coalesce(g.ordernum, 0) "

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
                    v_sql = v_sql + " and  coalesce(h.id,0) > 0 "
                    v_sql_cc = v_sql_cc + " and  coalesce(h.id,0) > 0 "
            filter_begin = filter_stock["begin"]
            if filter_begin is not None:
                if filter_enquriy is not None and filter_enquriy == '已询价':
                    v_sql = v_sql + " and h.enquirydate >= '" + filter_begin + "'"
                    v_sql_cc = v_sql_cc + " and h.enquirydate >= '" + filter_begin + "'"
                else:
                    # 未询价
                    v_sql = v_sql + " and d.SignDate >= '" + filter_begin + "'"
                    v_sql_cc = v_sql_cc + " and d.SignDate >= '" + filter_begin + "'"
            filter_end = filter_stock["end"]
            if filter_end is not None:
                if filter_enquriy is not None and filter_enquriy == '已询价':
                    v_sql = v_sql + " and h.enquirydate <= '" + filter_end + " 23:59:59'"
                    v_sql_cc = v_sql_cc + " and h.enquirydate <= '" + filter_end + " 23:59:59'"
                else:
                    # 未询价
                    v_sql = v_sql + " and d.SignDate <= '" + filter_end + " 23:59:59'"
                    v_sql_cc = v_sql_cc + " and d.SignDate <= '" + filter_end + " 23:59:59'"
                    # 总数统计
                    print("select_stock_product_list count sql is \n", v_sql_cc)
            cursor.execute(v_sql_cc)
            product_count_row = cursor.fetchone()
            product_count = product_count_row[0]
            topN = page_no * page_prod_count
            # 增加排序功能

            if filter_enquriy is not None and filter_enquriy == '已询价':
                v_sql = "select row_number() over(order by h.enquirydate desc,a.stockproductid desc) as rownumber, " + v_sql + ""
            else:
                # 未询价
                v_sql = "select row_number() over(order by h.enquirydate desc,a.stockproductid desc) as rownumber, " + v_sql + ""
            v_sql = "select  * " + " from (" + v_sql + " ) as v1 where v1.rownumber > " + str(topN - page_prod_count) + " and v1.rownumber <= " + str(topN) + " order by v1.rownumber"
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
                product.orderNum = row[19]
                product.priceEnquiredID = row[20]
                product.enquiryDate = row[21]
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
            v_sql_columns = "e.[采购人], a.StockProductID,a.ProductID,CONVERT(varchar, d.SignDate, 120 ) as SignDate," \
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
                            "CONVERT(varchar, g.settlementTime, 120 ) as settlementTime, g.settlementOpCode, " \
                            "CONVERT(varchar, h.enquirydate, 120 ) as enquirydate "
            v_sql_fromtab = "FROM [Stock_Product_Info] as a " \
                            "join  FTPart_Stock_Product_Property_1 as b on a.StockProductID=b.MainID " \
                            "join Product_Image as c on b._ImageID=c.ProductImageID " \
                            "join stock_info d on d.ID=a.StockID " \
                            "join [FTPart_Stock_Property_1] e on e.[MainID] = d.ID " \
                            "left join [Stock_Product_Info_Desc] f on a.StockProductID=f.StockProductID "
            v_time_column = "g.CreateTime"
            if ptype == cv.order_goods:
                v_sql_tab_g = "(SELECT * FROM [Stock_Product_Order_App] WHERE settlement = 0 and  OrderStat = 1) as g"
                v_time_column = "g.CreateTime"
            elif ptype == cv.complete_order:
                v_sql_tab_g = "(SELECT * FROM [Stock_Product_Order_App] WHERE settlement = 1 and  OrderStat = 1) as g"
                v_time_column = "g.ensureTime"
            elif ptype == cv.return_goods:
                v_sql_tab_g = "(SELECT * FROM [Stock_Product_Order_App] WHERE settlement = 1 and  OrderStat = -1) as g"
                v_time_column = "g.CreateTime"
            elif ptype == cv.settlement_goods:
                v_sql_tab_g = "(SELECT * FROM [Stock_Product_Order_App] WHERE settlement = 2 and  OrderStat = 1) as g"
                v_time_column = "g.settlementTime"
            elif ptype == cv.history_goods:
                v_sql_tab_g = "(SELECT * FROM [Stock_Product_Order_App] AS T1 WHERE settlement >= 0) as g"
            else:
                v_sql_tab_g = "(SELECT * FROM [Stock_Product_Order_App] AS T1 " \
                              "WHERE NOT EXISTS( SELECT 1 FROM [Stock_Product_Order_App] AS T2 " \
                              "WHERE T1.orderID=T2.sourceOrderId and OrderStat = -1) and t1.sourceOrderId is null " \
                              "and T1.settlement < 3) as g"
            v_sql_tab_h = "(select max(id) as id, max(createtime) as enquirydate, StockProductID " \
                          " from [Stock_Product_EnquiryPrice_App] group by StockProductID) as h"

            v_sql_fromtab = v_sql_fromtab + " join " + v_sql_tab_g + " on a.StockProductID=g.StockProductID"
            v_sql_fromtab = v_sql_fromtab + " left join " + v_sql_tab_h + " on a.StockProductID=h.StockProductID"

            v_sql_filter = " where 1=1"
            filter_brand = filter_stock["brand"]
            if filter_brand is not None:
                filter_sql = ''
                for b in filter_brand:
                    filter_sql = filter_sql + "'" + b + "',"
                filter_sql = filter_sql.rstrip(',')
                v_sql_filter = v_sql_filter + " and b.[其它.商品品牌] in (" + filter_sql + ")"
            filter_enquriy = filter_stock["enquiry"]
            if filter_enquriy is not None:
                if filter_enquriy == '未询价':
                    v_sql_filter = v_sql_filter + " and  coalesce(h.id,0) = 0 "
                elif filter_enquriy == '已询价':
                    v_sql_filter = v_sql_filter + " and  coalesce(h.id,0) > 0 "
            # begin date
            filter_begin = filter_stock["begin"]
            if filter_begin is not None:
                v_sql_filter = v_sql_filter + " and " + v_time_column + " >= '" + filter_begin + "'"
            # end data
            filter_end = filter_stock["end"]
            if filter_end is not None:
                v_sql_filter = v_sql_filter + " and " + v_time_column + "<= '" + filter_end + " 23:59:59'"
            filter_supplier = filter_stock["supplier"]
            if filter_supplier is not None:
                filter_sql = ''
                for b in filter_supplier:
                    filter_sql = filter_sql + "'" + b + "',"
                filter_sql = filter_sql.rstrip(',')
                v_sql_filter = v_sql_filter + " and g.supplier in (" + filter_sql + ")"
            filter_specno = filter_stock["specno"]
            if filter_specno is not None:
                v_sql_filter = v_sql_filter + " and a.SpecNo = '" + filter_specno + "'"

            v_sql_cc = "select count(*) " + v_sql_fromtab + v_sql_filter
            print(ptype, "sql count is ", v_sql_cc)
            cursor.execute(v_sql_cc)
            row = cursor.fetchone()
            product_count = row[0]
            topN = page_no*page_prod_count
            # 增加排序功能
            v_sql = "select row_number() over(order by " + v_time_column + " desc,a.stockproductid desc, g.orderID desc) as rownumber, " + v_sql_columns + v_sql_fromtab + v_sql_filter + ""
            v_sql = "select  * " + " from (" + v_sql + " ) as v1 where v1.rownumber > " + str(topN - page_prod_count) + " and v1.rownumber <= " + str(topN) + " order by v1.rownumber"
            print(ptype, "sql page is ", v_sql)
            cursor.execute(v_sql)
            for row in cursor:
                product = self.parse_product_cursor(row)
                product_list.append(product)

            # 二次查询有没有退货的记录
            if ptype == cv.complete_order or ptype == cv.settlement_goods or ptype == cv.history_goods:
                for product in product_list:
                    return_product_list = []
                    if ptype == cv.history_goods:
                        v_sql_filter = " where (g.orderstat=-1 or g.orderstat=0) and a.stockproductid=" + str(product.StockProductID)
                    else:
                        v_sql_filter = " where g.orderstat=-1 and a.stockproductid=" + str(product.StockProductID)
                    v_sql = "select 0 as rownumber, " + v_sql_columns + v_sql_fromtab + v_sql_filter + ""
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
                sql = "select [其它.允采购量] from FTPart_Stock_Product_Property_1 where MainID=?"
                cursor.execute(sql, stockProductID)
                permitNum = cursor.fetchone()[0]
                if permitNum is None:
                    print("*error*"*10, "url is wrong.")
                    permitNum = -1
                sql = "select sum(OrderNum*OrderStat) from Stock_Product_Order_App where StockProductID=?"
                cursor.execute(sql, stockProductID)
                hadPurchasedNum = cursor.fetchone()[0]
                print("hadPurchasedNum is ", hadPurchasedNum)
                if hadPurchasedNum is None:
                    hadPurchasedNum = 0
                permitNum = permitNum - hadPurchasedNum
                if permitNum >= purchaseNum:
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
            result = "1"
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
                        # insert history row
                        sql = "insert INTO Stock_Product_Order_App_hist(StockProductID, OpCode, OrderNum,OrderPrice," \
                              " supplier, OperateType, orderId, note) VALUES(?,?,?,?,?,?,?,?)"
                        print(operate_type, "insert hist sql --- \n ", sql)
                        cursor.execute(sql, stockProductID, opCode, orderNum, purchasePrice,
                                       supplier, cv.cancel_order, orderID, '')
                        cursor.commit()
                        result_product.note = "1:" + operate_type + " ok."

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
                    sql = "update Stock_Product_Order_App " \
                          "set ensureOpCode = ?, OrderNum = ? , OrderPrice=?, supplier=? , settlement=?," \
                          " ensureTime=getdate() " \
                          "where orderID = ? and stockProductID = ? and settlement <> ? "
                    sql = "update Stock_Product_Order_App " \
                          "set ensureOpCode = ?,settlement=?," \
                          " ensureTime=getdate() " \
                          "where orderID = ? and stockProductID = ? and settlement <> ? "
                    print(operate_type, "update sql ---\n ", sql)
                    cursor.execute(sql, ensureOpCode, settlement, orderID, stockProductID, settlement)
                    # insert history row
                    sql = "insert INTO Stock_Product_Order_App_hist(StockProductID, OpCode, OrderNum," \
                          "OrderPrice, supplier, OperateType, orderId, note) " \
                          "VALUES(?,?,?,?,?,?,?,?)"
                    cursor.execute(sql, stockProductID, ensureOpCode, purchaseNum, purchasePrice, supplier,
                                   cv.complete_order, orderID, '')
                    sql = "update [FTPart_Stock_Product_Property_1] " \
                          "set [其它.app采购量] = coalesce([其它.app采购量], 0) + ?,[其它.供应商名称]=coalesce([其它.供应商名称],?),[其它.业务员]=? " \
                          "where [MainID]=?"
                    cursor.execute(sql, purchaseNum, supplier, ensureOpCode, stockProductID)
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
                        unitprice = allprice/goodsnum
                    print("写入erp数据库", stockProductID, unitprice, goodsnum)
                    sql = "select [其它.允采购量] from FTPart_Stock_Product_Property_1 where [MainID]=?"
                    cursor.execute(sql, stockProductID)
                    row = cursor.fetchone()
                    permittedNum = row[0]
                    if goodsnum == 0:
                        goodsnum = permittedNum
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
                    purchaseNum = prod["purchaseNum"]
                    purchasePrice = prod["purchasePrice"]
                    settlement = prod["settlement"]
                    # 退货。

                    sql = "select stockProductID, supplier, settlement,orderNum from Stock_Product_Order_App " \
                          "where orderID=? and orderStat = 1"
                    cursor.execute(sql, orderID)
                    row = cursor.fetchone()
                    if row is not None:
                        stockProductID = row[0]
                        supplier = row[1]
                        settlement = row[2]
                        doneOrderNum = row[3]
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
                        sql = "update [FTPart_Stock_Product_Property_1] set [其它.app采购量] = [其它.app采购量] - ? " \
                              "where [MainID]=?"
                        cursor.execute(sql, purchaseNum, stockProductID)
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
                        sql = "select [其它.允采购量] from FTPart_Stock_Product_Property_1 where [MainID]=?"
                        cursor.execute(sql, stockProductID)
                        row = cursor.fetchone()
                        permittedNum = row[0]
                        if goodsnum == 0:
                            goodsnum = permittedNum
                        sql = "update Stock_Product_InfoBase set unitprice=? where stockProductID = ?"
                        cursor.execute(sql, unitprice, stockProductID)
                        sql = "update Stock_Product_Info set goodsnum=? where stockProductID = ?"
                        cursor.execute(sql, goodsnum, stockProductID)
                        cursor.commit()
                        sql = "select stockProductID, sum(orderNum) from Stock_Product_Order_App " \
                              "where sourceOrderID=? and orderStat = -1 group by stockProductID"
                        cursor.execute(sql, orderID)
                        returnOrderNum = cursor.fetchone()[1]
                        result_product.note = "1:退货成功，采购量 " + str(doneOrderNum) + ", 退货量 "+str(purchaseNum) + ", 共退货 " + str(returnOrderNum)
                    else:
                        result_product.note = "0:退货失败，没有记录."
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
                              "set [其它.app采购量] = [其它.app采购量] + ? " \
                              "where [MainID]=?"
                        cursor.execute(sql, purchaseNum, stockProductID)
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
                        sql = "select [其它.允采购量] from FTPart_Stock_Product_Property_1 where [MainID]=?"
                        cursor.execute(sql, stockProductID)
                        row = cursor.fetchone()
                        permittedNum = row[0]
                        if goodsnum == 0:
                            goodsnum = permittedNum
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
                        result_product.note = "1:" + operate_type + " ok."
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
                    result_product.note = "1:" + operate_type + " ok."
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
