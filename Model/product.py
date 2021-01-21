# -*- coding: utf-8 -*-
import json
import decimal
# 定义 采购产品 类
# 采购人	StockProductID	ProductID	SignDate	GoodsCode	SpecNo	GoodsSpec	GoodsUnit	_ImageID	ImageGuid	ImageFmt	ModuleID	FileDate	ThumbImage	其它.供应商名称	其它.允采购量	其它.应采购价	其它.商品品牌


class ProductInfo(object):

    def __init__(self):
        super(ProductInfo, self).__init__()
        #print("initial class", self)
        self.__setup_product()

    def __del__(self):
        pass

    def __setup_product(self):
        self.OpCode = ''
        self.StockProductID = 0
        self.ProductID = 0
        self.SignDate = ''
        self.GoodsCode = ''
        self.SpecNo = ''
        self.GoodsCDesc = ''
        self.GoodsUnit = ''
        self.ImageID = 0
        self.ImageGuid = ''
        self.ImageFmt = ''
        self.ModuleID = 0
        self.FileDate = ''
        self.imageBase64 = ''
        # 其它.供应商名称	其它.允采购量	其它.应采购价	其它.商品品牌
        self.supplier = ''
        self.permittedNum = 0
        self.appPermittedNum = 0
        # appPermittedNum 在没有完成订货时，和permittedNum的数值 是不一致的。app中操作需要用到它判断是否继续采购。
        self.shouldPrice = 0.0
        self.brand = ''
        self.priceEnquiredID = 0
        self.orderNum = 0
        self.orderPrice = 0.0
        # orderStat = 1 ，订货，-1 退货。和ordernum 组合使用，决定允许采购量, 0 为 取消退货
        self.orderStat = 1
        # settlement = 0，默认值，訂貨， 未确认订货成功。1， 订货成功，寫入ERP 2，结算。
        self.settlement = -1
        self.orderID = 0
        # 订货时间/取消订货时间
        self.createTime = ''
        self.orderOpCode = ''
        self.sourceOrderID = 0
        # 确认订货时间
        self.ensureTime = ''
        self.ensureOpCode = ''
        self.receiveGoodsTime = ''
        self.receiveOpCode = ''
        self.settlementTime = ''
        self.settlementOpCode = ''
        self.note = ''
        #对账商品数量
        self.accountNum = 0

    def desc(self):
        product_dict = self.__dict__
        product_dict["shouldPrice"] = str(self.shouldPrice)
        product_dict["orderPrice"] = str(self.orderPrice)
        # product_dict["CreateDate"] = self.CreateDate.strftime('%Y-%m-%d %H:%M:%S')
        print("product is ", self.StockProductID, self.ProductID, "price enquried is ", self.priceEnquiredID, self.GoodsCDesc, self.permittedNum,self.orderNum,self.shouldPrice,self.orderPrice)
        return product_dict

# SELECT [accountID]
#       ,[orderID]
#       ,[StockProductID]
#       ,[OpCode]
#       ,[OrderNum]
#       ,[OrderPrice]
#       ,[Settlement]
#       ,[supplier]
#       ,[CreateTime]
#       ,[accountNum]
#       ,[accountStat]

class AccountProductInfo(object):

    def __init__(self):
        super(AccountProductInfo, self).__init__()
        self.__setup_product()

    def __del__(self):
        pass

    def __setup_product(self):
        self.accountID = 0
        self.batchNo = ''
        self.orderID = 0
        self.StockProductID = 0
        self.accountOpCode = ''
        self.orderNum = 0
        self.orderPrice = 0.0
        self.settlement = -1
        self.supplier = ''
        self.createTime = ''
        self.accountNum = 0
        self.accountStat = 1
        self.note = ''

    def desc(self):
        product_dict = self.__dict__
        product_dict["orderPrice"] = str(self.orderPrice)
        # product_dict["CreateDate"] = self.CreateDate.strftime('%Y-%m-%d %H:%M:%S')
        return product_dict

class ProductEnquiryPrice(object):

    def __init__(self):
        super(ProductEnquiryPrice, self).__init__()
        print("initial class", self)
        self.__setup_product()

    def __del__(self):
        pass

    def __setup_product(self):
        self.ID = 0
        self.OpCode = ''
        self.StockProductID = 0
        self.ActivityType = ''
        self.What = ''
        self.CreateTime = ''

    def desc(self):
        product_dict = self.__dict__
        #product_dict["shouldPrice"] = str(self.shouldPrice)
        # product_dict["CreateDate"] = self.CreateDate.strftime('%Y-%m-%d %H:%M:%S')
        # print(product_dict)
        return product_dict


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            # wanted a simple yield str(o) in the next line,
            # but that would mean a yield on the line with super(...),
            # which wouldn't work (see my comment below), so...
            return (str(o) for o in [o])
        return super(DecimalEncoder, self).default(o)
