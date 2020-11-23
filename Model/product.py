# -*- coding: utf-8 -*-
import json
import decimal
# 定义 采购产品 类
# 采购人	StockProductID	ProductID	SignDate	GoodsCode	SpecNo	GoodsSpec	GoodsUnit	_ImageID	ImageGuid	ImageFmt	ModuleID	FileDate	ThumbImage	其它.供应商名称	其它.允采购量	其它.应采购价	其它.商品品牌


class ProductInfo(object):

    def __init__(self):
        super(ProductInfo, self).__init__()
        print("initial class", self)
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
        self.shouldPrice = 0.0
        self.brand = ''

    def desc(self):
        product_dict = self.__dict__
        product_dict["shouldPrice"] = str(self.shouldPrice)
        # product_dict["CreateDate"] = self.CreateDate.strftime('%Y-%m-%d %H:%M:%S')
        print(product_dict)
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
        print(product_dict)
        return product_dict


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            # wanted a simple yield str(o) in the next line,
            # but that would mean a yield on the line with super(...),
            # which wouldn't work (see my comment below), so...
            return (str(o) for o in [o])
        return super(DecimalEncoder, self).default(o)
