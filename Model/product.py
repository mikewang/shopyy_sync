# -*- coding: utf-8 -*-
import datetime
import base64

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
        self.GoodsSpec = ''
        self.GoodsUnit = ''
        self.ImageID = 0
        self.ImageGuid = ''
        self.ImageFmt = ''
        self.ModuleID = 0
        self.FileDate = ''
        self.imageBase64 = ''


        self.CreateDate = datetime.datetime.now()
        self.OrganizeID = 0
        self.Position = 0
        self.PositionName = ''

    def decode_password(self):
        base64_password = self.Password
        base64_bytes = base64_password.encode("utf8")
        password_bytes = base64.b64decode(base64_bytes)
        password = password_bytes.decode('utf8')
        return password

    def encode_password(self, password):
        password_bytes = password.encode('utf8')
        base64_bytes = base64.b64encode(password_bytes)
        base64_password = base64_bytes.decode("utf8")
        return base64_password

    def desc(self):
        user_dict = self.__dict__
        user_dict["CreateDate"] = self.CreateDate.strftime('%Y-%m-%d %H:%M:%S')
        user_dict["realPassword"] = self.decode_password()
        print(user_dict)
        return user_dict



