class Product(object):

    def __init__(self):
        super(Product, self).__init__()
        print("initial class", self)
        self.__setup_product()

    def __del__(self):
        pass

    def __setup_product(self):
        self.ID = 0
        self.name = ''
        self.CreateTime = ''

    def desc(self):
        product_dict = self.__dict__
        #product_dict["shouldPrice"] = str(self.shouldPrice)
        # product_dict["CreateDate"] = self.CreateDate.strftime('%Y-%m-%d %H:%M:%S')
        # print(product_dict)
        return product_dict