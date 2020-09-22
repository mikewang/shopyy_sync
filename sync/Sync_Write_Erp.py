# -*- coding: utf-8 -*-
from PyQt5.QtCore import QObject, pyqtSignal
import os
import time
import requests
from sync.Sync_Dao import SyncDao as Dao
from sync import global_v as gl


class SyncWriteErp(QObject):
    signal = pyqtSignal(dict)
    sync_sleep_time = 0

    def __init__(self):
        super(SyncWriteErp, self).__init__()

    def __del__(self):
       print("auto del", self)

    def callback_dao(self, signal_message):
        # print("request callback", signal_message)
        self.signal.emit(signal_message)
    
    def write_product_type(self, domain_name, product_type_list):
        dao = Dao()
        dao.signal.connect(self.callback_dao)
        dao.merge_product_type_list(domain_name, product_type_list)
    
    def write_product_image(self, product_info, product_image, dao):
        filepath = product_image["ImageFilePath"]
        download_file_again = False
        if gl.force_download_file == True:
            download_file_again = gl.force_download_file
        download_times = 0
        while True:
            if not os.path.exists(filepath) or download_file_again == True:
                download_time_str = self.download_file(product_image["url"], filepath)
                message = "产品:" + product_info["GoodsCode"] + " 下载" + product_image["url"] + " " + download_time_str + "秒"
                self.signal.emit({"message": message})
                #
            merge_result = dao.merge_product_image(product_image)
            if merge_result == True:
                break
            else:
                download_file_again = True
            download_times = download_times + 1
            if download_times > 3:
                break

    def write_product_info(self, domain_name, product_info_list):
        dao = Dao()
        dao.signal.connect(self.callback_dao)
        for product_info in product_info_list:
            if gl.worker_thread_isRunning == False:
                break;
            stock_nums = product_info["stock_nums"]
            # stock_nums = 0 , 则不同步到erp中，在erp反向操作时，将erp中的产品下架，因为已经是库存为1
            if int(stock_nums) > 0:
                dao.merge_product_info(domain_name, product_info)
                self.signal.emit({"product": product_info})
                # write product image
                if domain_name == gl.pf_domain:
                    product_image = dao.generate_product_image(product_info, None)
                    if product_image is not None:
                        self.write_product_image(product_info, product_image, dao)
                    else:
                        message = "产品:" + product_info["GoodsCode"] + " 主图为空，请检查网站"
                        self.signal.emit({"message": message})
                        print(message, product_info)
                elif domain_name == gl.ls_domain:
                    prod_list = dao.select_product_info(domain_name, product_info["GoodsCode"])
                    if len(prod_list) > 0:
                        product_image = dao.generate_product_image(product_info, None)
                        if product_image is not None:
                            self.write_product_image(product_info, product_image, dao)
                        else:
                            message = "产品:" + product_info["GoodsCode"] + " 主图为空，请检查网站"
                            self.signal.emit({"message": message})
                # write spec
                for product_spec in product_info["product_spec"]:
                    # print("product_spec",product_spec)
                    dao.merge_product_spec(domain_name, product_spec)
                    dao.merge_Product_Material_Info(product_info, product_spec)
                # offline spec
                spec_list = dao.select_product_spec(product_info)
                offline_spec_list = []
                for spec in spec_list:
                    offline_spec_list.append(spec)
                    for spec2 in product_info["product_spec"]:
                        SpecNo = spec2["SpecNo"]
                        offline_spec_list.remove(spec)
                        break
                for spec in offline_spec_list:
                    ProductID = spec["ProductID"]
                    SpecNo = spec["SpecNo"]
                    dao.offline_product_spec(ProductID, SpecNo)
                # write spec image
                for spec_image in product_info["product_image"]:
                    # print("spec_image", spec_image)
                    if domain_name == gl.pf_domain:
                        product_image = dao.generate_product_image(product_info, spec_image)
                        if product_image is not None:
                            self.write_product_image(product_info, product_image, dao)
                        else:
                            message = "产品:" + product_info["GoodsCode"] + "  规格" + spec_image["sku_value"] + "的图为空，请检查网站"
                            self.signal.emit({"message": message})
                    elif domain_name == gl.ls_domain:
                        prod_list = dao.select_product_info(domain_name, product_info["GoodsCode"])
                        if len(prod_list) > 0:
                            product_image = dao.generate_product_image(product_info, spec_image)
                            if product_image is not None:
                                self.write_product_image(product_info, product_image, dao)
                            else:
                                message =  "产品:" + product_info["GoodsCode"] + "  规格" + spec_image["sku_value"] + "的图为空，请检查网站"
                                self.signal.emit({"message": message})
                # 单规格产品的规格图没有，需要从主图上复制一份。
                spec_mode = (product_info["body_product_spec"])["spec_mode"]
                if spec_mode != "1":
                    if len(product_info["product_spec"]) == 1:
                        product_spec = product_info["product_spec"][0]
                        RecGuid = product_spec["RecGuid"]
                        dao.merge_product_single_spec_image(product_info)
                    else:
                        print("非多规格产品", product_info["GoodsCode"], "修改规格图失败")
                # GoodsCode
                GoodsCode = product_info["GoodsCode"]
                product_image = dao.select_product_image(GoodsCode)
                self.signal.emit({"product_image": product_image})
                # 同步下架的规格
                time.sleep(self.sync_sleep_time)
            else:
                message =  "产品:" + product_info["GoodsCode"] + "库存为0"
                self.signal.emit({"message": message})

    def download_file(self, url, filepath):
        beg_time = time.time()
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(filepath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    # If you have chunk encoded response uncomment if
                    # and set chunk_size parameter to None.
                    # if chunk:
                    f.write(chunk)
                    # the end download to disk.
        print("下载图片：" + filepath + " 完成", str(round(time.time() - beg_time, 4)) + "秒")
        return str(round(time.time() - beg_time, 4))

    def offline_product_info(self, domain_name, api_product_info_list, offline_product_info_list):
        dao = Dao()
        dao.signal.connect(self.callback_dao)
        
        if api_product_info_list is not None and offline_product_info_list is None:
            erp_prod_list = dao.select_product_info(domain_name, None)
            erp_set = set()
            for product_info in erp_prod_list:
                if product_info["ProductActive"] == "0":
                    erp_set.add(product_info["ProductID"])
            api_set = set()
            for product_info in api_product_info_list:
                api_set.add(product_info["ProductID"])
            erp_set.difference_update(api_set)
            print("网站" + domain_name + "下架的产品ID", erp_set)
            erp_prod_list_offline = []
            for productID in erp_set:
                for product_info in erp_prod_list:
                    if productID == product_info["ProductID"]:
                        erp_prod_list_offline.append(product_info)
            cc = len(erp_set)
            if cc > 100:
                message = "网站" + domain_name + "下架的产品" + str(cc) + "，数量异常，操作中止"
                self.signal.emit({"message": message})
            else:
                message = "网站" + domain_name + "下架的产品数" + str(cc) + "个"
                self.signal.emit({"message": message})
                for product_info in erp_prod_list_offline:
                    self.signal.emit({"product": product_info})
                    productID = product_info["ProductID"]
                    dao.offline_product_info(productID, domain_name)
                    # GoodsCode
                    GoodsCode = product_info["GoodsCode"]
                    product_image = dao.select_product_image(GoodsCode)
                    self.signal.emit({"product_image": product_image})
                    time.sleep(self.sync_sleep_time)
        elif api_product_info_list is None and offline_product_info_list is not None:
            offline_cc = 0
            for product_info in offline_product_info_list:
                if product_info["ProductActive"] == "1":
                    self.signal.emit({"product": product_info})
                    productID = product_info["ProductID"]
                    dao.offline_product_info(productID, domain_name)
                    # GoodsCode
                    GoodsCode = product_info["GoodsCode"]
                    product_image = dao.select_product_image(GoodsCode)
                    self.signal.emit({"product_image": product_image})
                    time.sleep(self.sync_sleep_time)
                    offline_cc = offline_cc + 1
            message = "网站" + domain_name + "下架的产品数" + str(offline_cc)+ "个"
            self.signal.emit({"message": message})

    def query_product_info(self, GoodsCode):
        dao = Dao()
        dao.signal.connect(self.callback_dao)
        prod_list = dao.select_product_info(None, GoodsCode)
        product_info = None
        if len(prod_list) > 0:
            product_info = prod_list[0]
            product_image = dao.select_product_image(GoodsCode)
            product_info["product_image"] = product_image
            ProductID = product_info["ProductID"]
            rowno = 1
            product_spec = dao.select_product_spec_image(ProductID, rowno)
            product_info["product_spec_first"] = product_spec
        return product_info


