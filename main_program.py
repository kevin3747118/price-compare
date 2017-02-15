from bs4 import BeautifulSoup
import urllib.request
import random
import re
import json
from payeasy import payeasy
# import time
import requests
from elasticsearch import Elasticsearch



class price_compare():

    def __init__(self, product_name):

        def replace_string():
            replace_string = ['/', ':', '【', '】', '《', '》', '+', '※',
                              '(', ')', '_', '<', '>', '★', '?', '-', '-'
                              '紅', '橙', '黃', '綠', '藍', '紫', '白', '灰', '黑', '銀']
            for i in self.product_name:
                if i in replace_string:
                    self.product_name = self.product_name.replace(i, ' ')
            return self.product_name.replace('福利網獨享', '')

        self.es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        self.product_name = product_name
        self.correct_product_name = replace_string()
        self.encode_pro_name = urllib.parse.quote(self.correct_product_name)
        self.__momo_url = 'http://www.momoshop.com.tw/mosearch/' + self.encode_pro_name + '.html'
        self.__pchome_url = 'http://ecshweb.pchome.com.tw/search/v3.3/all/results?q=' + self.encode_pro_name + '&page=1&sort=rnk/dc'
        self.__yahoo_url = 'https://tw.search.buy.yahoo.com/search/shopping/product?p=' + self.encode_pro_name + '&qt=product&cid=&clv='
        self.__udn_url = 'http://shopping.udn.com/mall/cus/search/SearchAction.do?start=1&keyword=' + self.sencode_pro_name + '&cid=&sort=weight&pickup=&minP=&maxP=&pageSize=20&key=32303137303230f7f25da1a0ab06cd67c0'
        self.__etmall_url = 'http://www.etmall.com.tw/Pages/AllSearchFormResult.aspx'

    def print(self):
        print(self.correct_product_name)
        # self.correct_product_name = self.replace_string()                   ####產品名稱
        # self.encode_pro_name = urllib.parse.quote(self.correct_product_name)  ####url encode

    def get_page(self, url, parameters=None):
        if parameters:
            encode_parameters = urllib.parse.urlencode(parameters).encode('utf-8')
        else:
            encode_parameters = None
        # time.sleep(0.43)
        request = urllib.request.Request(url)

        ####隨機header挑選####
        foo = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',
            'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_7; da-dk) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1'
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2722.0 Safari/537.36'
            'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
        ]
        headers = str(random.choice(foo))
        ####隨機header挑選####

        request.add_header('User-Agent', headers)
        # time.sleep(0.32)
        response = urllib.request.urlopen(request, data=encode_parameters, timeout=180)
        html = BeautifulSoup(response.read().decode('utf-8'), 'lxml')
        response.close()

        return html

    def get_page2(self, url):

        request = urllib.request.Request(url)

        ####隨機header挑選####
        foo = [
            'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_7; da-dk) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1'
        ]
        headers = str(random.choice(foo))
        # headers = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
        # print(headers)
        ####隨機header挑選####

        request.add_header('User-Agent', headers)
        response = urllib.request.urlopen(request, timeout=180)
        html = BeautifulSoup(response.read().decode('big5'), 'lxml')
        response.close()

        return html

    def momo(self):

        result = self.get_page(self.__momo_url)

        momo = list()

        if result.find_all('ul', {'id': 'chessboard'}):
            # print('1')
            for i in result.find_all('ul', {'id': 'chessboard'}):
                for x in i.find_all(['a', 'b']):
                    #                 if x.text != '' and len(momo) != 8:
                    if x.text != '':
                        momo.append(x.text)
        elif result.find_all('script'):
            # print('2')
            for i in result.find_all('script'):
                momo_goods_url = i.text.strip('location.href=').strip(';').strip('\'"').replace(',', '')
                # print(momo_goods_url)
                momo_goods_detail = self.get_page2(momo_goods_url)
                for i in momo_goods_detail.find_all('div', {'class': 'prdnoteArea'}):
                    for product in i.find_all('h1'):
                        momo.append(product.text)
                    for price in i.find_all('li', {'class': 'special'}):
                        momo.append(price.text.replace(',', '').replace('促銷價', '').replace('元', '')
                                    .replace('\r\n', '').replace(' ', '').replace('折扣後價格', ''))
                # for i in momo_goods_detail.find_all('div', {'class': 'prdnoteArea'}):
                #     momo.append(i.find('h1').text)
                # for price in i.find('span'):
                #     momo.append(price.replace(',', ''))

        ####將結果變成list裡面包tuple(產品, 價格)####
        momo_display = list()
        a, b = 0, 2
        x = int(len(momo) / 2)
        while x != 0:
            momo_display.append(tuple(momo[a:b]))
            x -= 1
            a, b = b, b + 2
        ####將結果變成list裡面包tuple(產品, 價格)####

        return momo_display

    def pchome(self):

        import json

        pchome = self.get_page(self.__pchome_url)

        pchome_data = dict()
        for x in pchome.find_all('p'):
            item_data = json.loads(x.text)
            pchome_data = item_data['prods']

        pchome_display = [(i['name'], int(i['price'])) for i in pchome_data]

        return pchome_display

    def payeasy(self):

        terms = self.encode_pro_name + '%20payeasy'
        result = self.get_page('https://www.google.com.tw/search?&q=' + terms + '&oq=' + terms)

        payeasy_EC = list()
        payeasy_PD = list()
        for url in result.find_all('h3', {'class': 'r'}):
            for url2 in url:
                try:
                    if 'EcCategoryV2' in url2['href']:
                        payeasy_EC.append(url2['href'])
                    if 'ProductDetail' in url2['href']:
                        payeasy_PD.append(url2['href'])
                except Exception:
                    pass
                    #         return payeasy_EC, payeasy_PD

        payeasy_EC_result = list()
        payeasy_PD_result = list()
        # ?page=1&sort=2&direction=1#filterTool
        if payeasy_EC:
            payeasy_get_web_page = self.get_page(payeasy_EC[0])
            pages = list()
            for i in payeasy_get_web_page.find_all('div', {'class': 'pagination'}):
                for x in i.find_all('span'):
                    pages = [range(1, int(u) + 1) for u in x if u.isdigit()]
            for page in pages[0]:
                #                 print(payeasy_EC[0] + '?page=' + str(page) + '&sort=2&direction=1#filterTool')
                payeasy_web_content = self.get_page(
                    payeasy_EC[0] + '?page=' + str(page) + '&sort=2&direction=1#filterTool')
                for x in payeasy_web_content.find_all('p', {'class': ['ProductName', 'ProducPrice']}):
                    payeasy_EC_result.append(x.text)
        else:
            payeasy_web_content = self.get_page(payeasy_PD[0])
            for x in payeasy_web_content.find_all('div', {'class': 'product_info_area'}):
                for pro_name in x.find_all('h1', {'class': 'pro_name_cn'}):
                    payeasy_PD_result.append(pro_name.text)
                for price in x.find_all('div', {'class': 'price_001'}):
                    payeasy_PD_result.append(price.find_next('b').text)

                    #         if payeasy_PD:
                    #             payeasy_web_content = self.get_page(payeasy_PD[0])
                    #             for x in payeasy_web_content.find_all('div', {'class':'product_info_area'}):
                    #                 for pro_name in x.find_all('h1', {'class':'pro_name_cn'}):
                    #                     payeasy_PD_result.append(pro_name.text)
                    #                 for price in x.find_all('div', {'class':'price_001'}):
                    #                     payeasy_PD_result.append(price.find_next('b').text)

        payeasy_display = list()
        if payeasy_EC_result:
            payeasy_display = [
                x.strip('\r\n').strip(' ').strip('NT$').rstrip('購買').replace(',', '').strip('購買\n福登入享福利獨享價') for x in
                payeasy_EC_result]
        if payeasy_PD_result:
            payeasy_display = [x.replace(',', '') for x in payeasy_PD_result]

        ####將結果變成list裡面包tuple(產品, 價格)####
        payeasy_display2 = list()
        a, b = 0, 2
        x = int(len(payeasy_display) / 2)
        while x != 0:
            payeasy_display2.append(tuple(payeasy_display[a:b]))
            x -= 1
            a, b = b, b + 2
        ####將結果變成list裡面包tuple(產品, 價格)####

        return payeasy_display2


    def gohappy(self):

        # def gohappy_pro_pages(search):  #### 取得商品頁數
        #
        #     gohappy_pro_url = 'http://www.gohappy.com.tw/ec2/search?sid=&hotNum=1&search=' + search
        #     gohappy_url_html = self.get_page(gohappy_pro_url)
        #
        #     parse_time = None
        #     for pages in gohappy_url_html.find_all('ul', {'class': 'pagenum'}):
        #         gohappy_page = pages.text.replace('\n', '')
        #         page_index = gohappy_page.find('共')
        #         parse_time = int(gohappy_page[page_index + 1:].replace('頁', ''))
        #
        #     return parse_time
        #
        # gohappy_url = 'http://www.gohappy.com.tw/ec2/searchCate'
        #
        # # pages = gohappy_pro_pages(self.encode_pro_name)
        #
        # gohappy_list = list()
        # parameters = {'searchs': self.product_name, 'pageno': '1', 'pagesize': '20', 'orderby': 'close',
        #               'cateLvs': '-1', 'watchtype': '1'}
        # r = requests.post(gohappy_url, params=parameters)
        # r_json = json.loads(r.text)
        # r_bs = BeautifulSoup(r_json.get('data').get('form'), 'lxml')
        #
        # for elements in r_bs.find_all('ol', {'class': 'proddata-list'}):
        #     for product in elements.find_all('li', {'class': 'prodname'}):
        #         gohappy_list.append(product.text.replace('\n', ''))
        #     for price_tag in elements.find_all('li', {'class': 'price-txt'}):
        #         for price in price_tag.find_all('strong'):
        #             gohappy_list.append(price.text)
        # for page in range(0, pages):
        #     parameters = {'searchs': self.product_name, 'pageno': str(page), 'pagesize': '20', 'orderby': 'close',
        #                   'cateLvs': '-1', 'watchtype': '1'}
        #     r = requests.post(gohappy_url, params=parameters)
        #     r_json = json.loads(r.text)
        #     r_bs = BeautifulSoup(r_json.get('data').get('form'), 'lxml')
        #
        #     for elements in r_bs.find_all('ol', {'class': 'proddata-list'}):
        #         for product in elements.find_all('li', {'class': 'prodname'}):
        #             gohappy_list.append(product.text.replace('\n', ''))
        #         for price_tag in elements.find_all('li', {'class': 'price-txt'}):
        #             for price in price_tag.find_all('strong'):
        #                 gohappy_list.append(price.text)

        # encode_search = urllib.parse.quote(search)
        result = self.get_page('http://www.gohappy.com.tw/ec2/search?sid=&hotNum=0&search=' + self.encode_pro_name)

        gohappy_list = list()
        for elements in result.find_all('ol', {'class': 'proddata-list'}):
            for product in elements.find_all('h3'):
                if '【線上兌換】' not in product.text:
                    gohappy_list.append(product.text.replace('\n', ''))
            for prices in elements.find_all('table', {'class': 'price-table'}):
                if '純點數' not in prices.text:
                    for price in prices.find_all('strong'):
                        gohappy_list.append(price.text)

        ####將結果變成list裡面包tuple(產品, 價格)####
        gohappy_display = list()
        a, b = 0, 2
        x = int(len(gohappy_list) / 2)
        while x != 0:
            gohappy_display.append(tuple(gohappy_list[a:b]))
            x -= 1
            a, b = b, b + 2
        ####將結果變成list裡面包tuple(產品, 價格)####

        return gohappy_display

    def yahoo(self):

        result = self.get_page(self.__yahoo_url)
        yahoo = list()

        if result.find_all('div', {'class': 'wrap yui3-g'}):
            # print('1')
            for elements in result.find_all('div', {'class': 'wrap yui3-g'}):
                for product in elements.find_all('div', {'class': 'srp-pdtitle ellipsis'}):
                    yahoo.append(product.text.replace('\n', ''))
                for prices in elements.find_all('div', {'class': 'srp-pdprice'}):
                    if prices.find_all('span', {'class': 'srp-actprice-prefix'}):
                        for price in prices.find_all('em'):
                            yahoo.append(price.text.replace('$', '').replace('起', '').
                                         replace('\n', '').replace(',', ''))
                    elif prices.find_all('span', {'class': 'srp-listprice-prefix'}) and prices.find_all('span', {
                        'class': 'srp-actprice-prefix'}) is None:
                        yahoo.append(prices.text.replace('網路價 $', '').replace('起', '').
                                     replace('\n', '').replace(',', ''))
                    else:
                        for price in prices.find_all('span', {'class': 'srp-listprice-class'}):
                            yahoo.append(price.text.replace('$', '').replace('起', '').
                                         replace('\n', '').replace(',', ''))
                            # for price in prices.find_all('span', {'class': 'srp-listprice-class'}):
                            #     yahoo.append(price.text.replace('$', ''))
        elif result.find_all('div', {'class': 'srp-pdcontent'}):
            # print('2')
            for elements in result.find_all('div', {'class': 'srp-pdcontent'}):
                for product in elements.find_all('div', {'class': 'srp-pdtitle'}):
                    yahoo.append(product.text.replace('\n', ''))
                for prices in elements.find_all('div', {'class': 'srp-pdprice'}):
                    if prices.find_all('div', {'class': 'srp-actprice'}):
                        for price in prices.find_all('div', {'class': 'srp-actprice'}):
                            yahoo.append(price.text.replace('活動價 $', '').replace('起', '').replace(',', ''))
                    else:
                        for price in prices.find_all('div', {'class': 'srp-listprice'}):
                            # yahoo.append(price.text.replace('網路價 $', ''))
                            yahoo.append(price.text.replace(',', '').replace('網路價 $', ''))

        ###將結果變成list裡面包tuple(產品, 價格)####
        yahoo_display = list()
        a, b = 0, 2
        x = int(len(yahoo) / 2)
        while x != 0:
            yahoo_display.append(tuple(yahoo[a:b]))
            x -= 1
            a, b = b, b + 2
        ###將結果變成list裡面包tuple(產品, 價格)####
        return yahoo_display


    def udn(self):

        # def udn_pro_pages(search):
        #
        #     result = self.get_page(self.__udn_url)
        #     udn_pages = list()
        #     for pages in result.find_all('li', {'class': 'pager_item'}):
        #         page = pages.text.replace('\n', '').replace('\r', '').replace('\t', '')
        #         udn_pages.append(page)
        #         if '下一頁' in udn_pages:
        #             udn_pages.remove('下一頁')
        #
        #     return udn_pages

        # udn_list = list()
        # pages = udn_pro_pages(self.encode_pro_name)
        # for page in pages:
        #     result = self.get_page("http://shopping.udn.com/mall/cus/search/SearchAction.do?start=" + str(page) + "&keyword="
        #              + self.encode_pro_name + "&cid=&sort=weight&pickup=&minP=&maxP=&pageSize=20&key=32303137303230f7f25da1a0ab06cd67c0")
        #     for elements in result.find_all('li', {'class': 'lv3_item'}):
        #         for product in elements.find_all('p', {'class': 'pd_name'}):
        #             udn_list.append(product.text)
        #         for price in elements.find_all('p', {'class': 'pd_price'}):
        #             udn_list.append(price.text.replace('\n', '').replace('\t', '').replace('\r', '').replace('限時', ''))

        data = {'sort': 'weight', 'key': '32303137303231f6f259a2a8ac0fce6fc0', 'cid': '', 'keyword': self.correct_product_name}
        result = self.get_page('https://shopping.udn.com/mall/cus/search/Search.do', parameters=data)

        udn_list = list()
        if result.find_all('ul', {'class': 'lv3_item_list'}):
            for elements in result.find_all('li', {'class': 'lv3_item'}):
                for product in elements.find_all('p', {'class': 'pd_name'}):
                    udn_list.append(product.text)
                for price in elements.find_all('p', {'class': 'pd_price'}):
                    udn_list.append(
                        price.text.replace('\n', '').replace('\t', '').replace('\r', '').replace('限時', ''))

        ####將結果變成list裡面包tuple(產品, 價格)####
        udn_display = list()
        a, b = 0, 2
        x = int(len(udn_list) / 2)
        while x != 0:
            udn_display.append(tuple(udn_list[a:b]))
            x -= 1
            a, b = b, b + 2
        ####將結果變成list裡面包tuple(產品, 價格)####

        return udn_display

    def asap(self):

        import requests

        def get_asap_pro_id():

            import re

            asap_scripts = str()
            # asap_pages = int()

            pattern = 'sm_seq_list:.*?\]'

            result = self.get_page('http://www.asap.com.tw/search?q=' + self.encode_pro_name + '&s_c=1')
            for scripts in result.find_all('script'):
                asap_scripts = scripts.text
                #         for pages in result.find_all('ul', {'class': 'pagination'}):
                #             asap_pages = pages
                #             print(pages.text)

            match = re.search(pattern, asap_scripts)
            pro_id = match.group(0).replace('sm_seq_list:[', '').replace(']', '').replace('"', '').split(',')

            if 'null' in pro_id[0]:
                return None
            else:
                return pro_id

        pro_id = get_asap_pro_id()

        asap_display = list()
        if pro_id:
            parameters = {'sm_seq_list[]': pro_id,
                          'is_cross': 'false',
                          'cross_country': ''}

            result = requests.post('http://www.asap.com.tw/category/get_real_time_data', data=parameters)
            result_dict = json.loads(result.text)

            asap_list = list()
            for i in pro_id:
                name = result_dict.get('data').get(i).get('market_info').get('name')
                price = result_dict.get('data').get(i).get('market_info').get('price').get('final_price').get('price').replace(',', '')
                asap_list.extend((name, price))

            ####將結果變成list裡面包tuple(產品, 價格)####
            a, b = 0, 2
            x = int(len(asap_list) / 2)
            while x != 0:
                asap_display.append(tuple(asap_list[a:b]))
                x -= 1
                a, b = b, b + 2
        ####將結果變成list裡面包tuple(產品, 價格)####
        else:
            asap_display = []

        return asap_display


    def etmall(self):

        # parameters = {'SearchKeyword': self.correct_product_name,
        #               'SearchKey': self.correct_product_name,
        #               'ProductPage': '0',
        #               'RecordsPerPage': '40',
        #               'OrderBy': '_weight_,DESC'}
        #

        pat_product = 'aPL_GOODNM\[.*?\)'
        pat_price = 'aPL_DISCOUNT_VALUE\[.*?\;'
        pat_price2 = 'aPL_PRC\[.*?\;'

        result = str(self.get_page('http://www.etmall.com.tw/AllSearchFormResult.aspx?SearchKeyword=' + self.encode_pro_name + '&CategoryID='))

        product = re.findall(pat_product, result)
        price = re.findall(pat_price, result)
        price2 = re.findall(pat_price2, result)

        # print(price2)

        etmall_list = list()
        for i in range(len(product)):
            product_remove = re.sub(r"^aPL.*\car\('", '', product[i]).replace("')", '')
            if re.sub(r"^aPL.*\= \'", '', price[i]).replace("';", ''):
                price_remove = re.sub(r"^aPL.*\= \'", '', price[i]).replace("';", '')
            else:
                price_remove = re.sub(r"^aPL.*\= \'", '', price2[i]).replace("';", '')
            etmall_list.extend([product_remove, price_remove])

        ####將結果變成list裡面包tuple(產品, 價格)####
        etmall_display = list()
        a, b = 0, 2
        x = int(len(etmall_list) / 2)
        while x != 0:
            etmall_display.append(tuple(etmall_list[a:b]))
            x -= 1
            a, b = b, b + 2
        ####將結果變成list裡面包tuple(產品, 價格)####
        return etmall_display
        ####將結果變成list裡面包tuple(產品, 價格)####
        etmall_display = list()
        a, b = 0, 2
        x = int(len(etmall_list) / 2)
        while x != 0:
            etmall_display.append(tuple(etmall_list[a:b]))
            x -= 1
            a, b = b, b + 2
        ####將結果變成list裡面包tuple(產品, 價格)####
        return etmall_display


    def umall(self):

        # parameters = {'SearchKeyword': self.correct_product_name,
        #               'SearchKey': self.correct_product_name,
        #               'ProductPage': '0',
        #               'RecordsPerPage': '40',
        #               'OrderBy': '_weight_,DESC'}

        # result = str(self.get_page('http://www.u-mall.com.tw/Search.aspx', parameters=parameters))

        result = str(self.get_page('http://www.u-mall.com.tw/Search.aspx?SearchKeyword=' + self.encode_pro_name))

        pat_product = 'Tmp = changecar\(\'.*?\)'
        pat_price = 'Sys_showPRCValue\(.*?\)'
        product = re.findall(pat_product, result)
        price_error_string = re.findall(pat_price, result)
        # print(product, price_error_string)
        price_correct = list()
        for i in price_error_string:
            price_correct.append(
                [(re.sub(r"^Sys_.*('', |'Y', )", '', i).replace(")", '').replace("'", '').replace(' ', ''))])
        price_final = [min(x) for x in [i[0].split(',') for i in price_correct]]

        umall_list = list()
        for i in range(len(product)):
            product_remove = re.sub(r"^Tmp.*\('", '', product[i]).replace("')", '')
            price_remove = price_final[i]
            umall_list.extend([product_remove, price_remove])
        # return umall_list

        ####將結果變成list裡面包tuple(產品, 價格)####
        umall_display = list()
        a, b = 0, 2
        x = int(len(umall_list) / 2)
        while x != 0:
            umall_display.append(tuple(umall_list[a:b]))
            x -= 1
            a, b = b, b + 2
        ####將結果變成list裡面包tuple(產品, 價格)####

        return umall_display


    def to_ES(self):

        momo_data = self.momo()
        pchome_data = self.pchome()
        yahoo_data = self.yahoo()
        umall_data = self.umall()
        etmall_data = self.umall()
        udn_data = self.udn()
        gohappy_data = self.gohappy()
        asap_data = self.asap()

        # es_data = [momo_data, pchome_data, yahoo_data, umall_data, etmall_data, udn_data, gohappy_data, asap_data]

        ####計算資料的index####
        # def counter():
        #     len_all = len(asap_data + momo_data + pchome_data + yahoo_data +
        #                   umall_data + etmall_data + udn_data + gohappy_data)
        #     yield from range(len_all)
        #
        # counter = counter()
        ####計算資料的index####

        # def to_es(es_data):
        #     for i in range(len(es_data)):
        #         new_dict = dict()
        #         new_dict['name'] = es_data[i][0]
        #         new_dict['price'] = int(new_dict[i][1])
        count = 1
        while True:
            ####insert momo data into elasticsearch#####
            momo_dict = dict()
            for i in range(len(momo_data)):
                momo_dict['name'] = momo_data[i][0]
                momo_dict['price'] = int(momo_data[i][1])
                momo_dict['company'] = 'momo'
                self.es.index(index='product', doc_type='3C', id=count, body=momo_dict)
                count += 1
            ####insert momo data into elasticsearch#####

            ####insert pchome data into elasticsearch####
            pchome_dict = dict()

            for i in range(len(pchome_data)):
                pchome_dict['name'] = pchome_data[i][0]
                pchome_dict['price'] = int(pchome_data[i][1])
                pchome_dict['company'] = 'pchome'
                # self.es.index(index='product', doc_type='3C', id=next(counter), body=pchome_dict)
                self.es.index(index='product', doc_type='3C', id=count, body=pchome_dict)
                count += 1
            ####insert pchome data into elasticsearch####

            ####insert asap data into elasticsearch####
            asap_dict = dict()

            for i in range(len(asap_data)):
                asap_dict['name'] = asap_data[i][0]
                asap_dict['price'] = int(asap_data[i][1])
                asap_dict['company'] = 'asap'
                self.es.index(index='product', doc_type='3C', id=count, body=asap_dict)
                count += 1
            ####insert asap data into elasticsearch####

            ####insert umall data into elasticsearch####
            umall_dict = dict()

            for i in range(len(umall_data)):
                umall_dict['name'] = umall_data[i][0]
                umall_dict['price'] = int(umall_data[i][1])
                umall_dict['company'] = 'umall'
                self.es.index(index='product', doc_type='3C', id=count, body=umall_dict)
                count += 1
            ####insert umall data into elasticsearch####

            ####insert etmall data into elasticsearch####
            etmall_dict = dict()

            for i in range(len(etmall_data)):
                etmall_dict['name'] = etmall_data[i][0]
                etmall_dict['price'] = int(etmall_data[i][1])
                etmall_dict['company'] = 'etmall'
                self.es.index(index='product', doc_type='3C', id=count, body=etmall_dict)
                count += 1
            ####insert etmall data into elasticsearch####

            ####insert gohappy data into elasticsearch####
            gohappy_dict = dict()

            for i in range(len(gohappy_data)):
                gohappy_dict['name'] = gohappy_data[i][0]
                gohappy_dict['price'] = int(gohappy_data[i][1])
                gohappy_dict['company'] = 'gohappy'
                self.es.index(index='product', doc_type='3C', id=count, body=gohappy_dict)
                count += 1
            ####insert gohappy data into elasticsearch####

            ####insert udn data into elasticsearch####
            udn_dict = dict()

            for i in range(len(udn_data)):
                udn_dict['name'] = udn_data[i][0]
                udn_dict['price'] = int(udn_data[i][1])
                udn_dict['company'] = 'udn'
                self.es.index(index='product', doc_type='3C', id=count, body=udn_dict)
                count += 1
            ####insert udn data into elasticsearch####

            ####insert yahoo data into elasticsearch####
            yahoo_dict = dict()

            for i in range(len(yahoo_data)):
                yahoo_dict['name'] = yahoo_data[i][0]
                yahoo_dict['price'] = int(yahoo_data[i][1])
                yahoo_dict['company'] = 'yahoo'
                self.es.index(index='product', doc_type='3C', id=count, body=yahoo_dict)
                count += 1
            break
        ####insert udn data into elasticsearch####
        # print('finish inserting product data into elasticsearch')

    def refresh_ES(self):
        self.es.indices.refresh(index='product')

    def delte_ES(self):
        self.es.indices.delete(index='product')

    def from_ES(self):

        self.to_ES()
        self.refresh_ES()
        result = self.es.search(index="product", body={"size": 100, "min_score": 1,
                                                       "query": {"match": {
                                                           "name": {"query": self.correct_product_name,
                                                                    "operator": "or"}}}})
        def len_verify(store):
            len_store = len(store)
            while len_store < 6:
                store.append('')
                len_store += 1
            while len_store > 6:
                del store[-1]
                len_store -= 1
            return store

        def ES_store_data():

            asap_data = list()
            for i in result['hits']['hits']:
                if i['_source']['company'] == 'asap':
                    asap_data.extend([i['_source']['name'], i['_source']['price']])
            asap_data = len_verify(asap_data)

            gohappy_data = list()
            for i in result['hits']['hits']:
                if i['_source']['company'] == 'gohappy':
                    gohappy_data.extend([i['_source']['name'], i['_source']['price']])
            gohappy_data = len_verify(gohappy_data)

            udn_data = list()
            for i in result['hits']['hits']:
                if i['_source']['company'] == 'udn':
                    udn_data.extend([i['_source']['name'], i['_source']['price']])
            udn_data = len_verify(udn_data)

            pchome_data = list()
            for i in result['hits']['hits']:
                if i['_source']['company'] == 'pchome':
                    pchome_data.extend([i['_source']['name'], i['_source']['price']])
            pchome_data = len_verify(pchome_data)

            momo_data = list()
            for i in result['hits']['hits']:
                if i['_source']['company'] == 'momo':
                    momo_data.extend([i['_source']['name'], i['_source']['price']])
            momo_data = len_verify(momo_data)

            yahoo_data = list()
            for i in result['hits']['hits']:
                if i['_source']['company'] == 'yahoo':
                    yahoo_data.extend([i['_source']['name'], i['_source']['price']])
            yahoo_data = len_verify(yahoo_data)

            etmall_data = list()
            for i in result['hits']['hits']:
                if i['_source']['company'] == 'etmall':
                    etmall_data.extend([i['_source']['name'], i['_source']['price']])
            etmall_data = len_verify(etmall_data)

            umall_data = list()
            for i in result['hits']['hits']:
                if i['_source']['company'] == 'umall':
                    umall_data.extend([i['_source']['name'], i['_source']['price']])
            umall_data = len_verify(umall_data)

            # umall_data = [[i['_source']['name'], i['_source']['price']]
            #              for i in result['hits']['hits'] if i['_source']['company'] == 'umall']

            # store_data = [asap_data, gohappy_data, udn_data, pchome_data,
            #               momo_data, yahoo_data, etmall_data, umall_data]

            store_data = asap_data + umall_data + etmall_data + yahoo_data + \
                         pchome_data + momo_data + udn_data + gohappy_data

            # for store in store_data:
            #     len_store = len(store)
            #     while len_store < 3:
            #         store.append(null_tuple)
            #         len_store += 1
            #     while len_store > 3:
            #         del store[-1]
            #         len_store -= 1

            return store_data

        data = ES_store_data()
        self.delte_ES()
        return data

    def main(self):
        self.to_ES()


if __name__ == '__main__':
#
    np = payeasy.db('AZURE')
    parse_store = np.do_query("SELECT [PID_NUM],[PRO_NAME],[PWB_NAME] "
                                "FROM [dbo].[PRODUCT_PRICE_COMPARE] WHERE ASAP_PNAME1 is null")

    # ###test area###
    # # asap_data, gohappy_data, udn_data, pchome_data,
    # # momo_data, yahoo_data, etmall_data, umall_data]
    # # for i in range(len(parse_store)):
    # #     price = price_compare(parse_store[i][1])
    # #     print(price.correct_product_name)
    # #     price.to_ES()
    # # price = price_compare('Sunlus三樂事暖暖熱敷柔毛墊 大 -MHP811')
    # # print(price.correct_product_name)
    # # print(price.from_ES())
    # # print(price.umall())
    # # print(price.etmall())
    # # price.to_ES()
    # # print(price.from_ES())
    # # print(len(price.from_ES()))
    # ###test area###
    #
    print('start parsing store data')
    for i in range(len(parse_store)):
        price = price_compare(parse_store[i][1])
            # print(price.correct_product_name)
        result = price.from_ES()
            # print(result)
            # print('\n')
        # except Exception as e:
        #     print(e)
        sql_stat = (
                "update [dbo].[PRODUCT_PRICE_COMPARE] set "
                " [ASAP_PNAME1] = '" + result[0] + "',[ASAP_PPRICE1]='" + str(result[1]) + "'"
                ",[ASAP_PNAME2] = '" + result[2] + "',[ASAP_PPRICE2]='" + str(result[3]) + "'"
                ",[ASAP_PNAME3] = '" + result[4] + "',[ASAP_PPRICE3]='" + str(result[5]) + "'"
                ",[UMALL_PNAME1] = '" + result[6] + "',[UMALL_PPRICE1]='" + str(result[7]) + "'"
                ",[UMALL_PNAME2] = '" + result[8] + "',[UMALL_PPRICE2]='" + str(result[9]) + "'"
                ",[UMALL_PNAME3] = '" + result[10] + "',[UMALL_PPRICE3]='" + str(result[11]) + "'"
                ",[ETMALL_PNAME1] = '" + result[12] + "',[ETMALL_PPRICE1]='" + str(result[13]) + "'"
                ",[ETMALL_PNAME2] = '" + result[14] + "',[ETMALL_PPRICE2]='" + str(result[15]) + "'"
                ",[ETMALL_PNAME3] = '" + result[16] + "',[ETMALL_PPRICE3]='" + str(result[17]) + "'"
                ",[YAHOO_PNAME1] = '" + result[18] + "',[YAHOO_PPRICE1]='" + str(result[19]) + "'"
                ",[YAHOO_PNAME2] = '" + result[20] + "',[YAHOO_PPRICE2]='" + str(result[21]) + "'"
                ",[YAHOO_PNAME3] = '" + result[22] + "',[YAHOO_PPRICE3]='" + str(result[23]) + "'"
                ",[PCHOME_PNAME1] = '" + result[24] + "',[PCHOME_PPRICE1]='" + str(result[25]) + "'"
                ",[PCHOME_PNAME2] = '" + result[26] + "',[PCHOME_PPRICE2]='" + str(result[27]) + "'"
                ",[PCHOME_PNAME3] = '" + result[28] + "',[PCHOME_PPRICE3]='" + str(result[29]) + "'"
                ",[MOMO_PNAME1] = '" + result[30] + "',[MOMO_PPRICE1]='" + str(result[31]) + "'"
                ",[MOMO_PNAME2] = '" + result[32] + "',[MOMO_PPRICE2]='" + str(result[33]) + "'"
                ",[MOMO_PNAME3] = '" + result[34] + "',[MOMO_PPRICE3]='" + str(result[35]) + "'"
                ",[UDN_PNAME1] = '" + result[36] + "',[UDN_PPRICE1]='" + str(result[37]) + "'"
                ",[UDN_PNAME2] = '" + result[38] + "',[UDN_PPRICE2]='" + str(result[39]) + "'"
                ",[UDN_PNAME3] = '" + result[40] + "',[UDN_PPRICE3]='" + str(result[41]) + "'"
                ",[GOHAPPY_PNAME1] = '" + result[42] + "',[GOHAPPY_PPRICE1]='" + str(result[43]) + "'"
                ",[GOHAPPY_PNAME2] = '" + result[44] + "',[GOHAPPY_PPRICE2]='" + str(result[45]) + "'"
                ",[GOHAPPY_PNAME3] = '" + result[46] + "',[GOHAPPY_PPRICE3]='" + str(result[47]) + "'"
                " where [PID_NUM] = " + str(parse_store[i][0]))
        np.do_query(sql_stat)
        np.do_commit()
    print('finish parsing store data')


    # print(price_compare('Victorinox Altmont 3.0 標準型後背包').from_ES())
    # print(test3.correct_product_name)
    # print(test3.from_ES())
    # test.to_ES()
    # print(test.from_ES())
    # price = price_compare('SONY SBH80 立體聲頸掛式藍芽耳機')
    # print(price.from_ES())


    # # print(price.correct_product_name)
    # # # print(price.yahoo())
    # price.to_ES()
    # print(price.from_ES())
    # test = ['@Nature玫瑰蜂王乳保濕水嫩青春露','【台北/烏來】泉世界溫泉會館一泊二食雙人夜湯專案(A)']
    # for i in test:
    #     haha = price_compare(i)
    #     print(haha.from_ES())



    # print(price.from_ES())
    # for i in range(5):
    #     price = price_compare('Victorinox Altmont 3.0 標準型後背包')
    #     print(('ASAP購物', len(price.asap())))
    #     print(('森森購物', len(price.umall())))
    #     print(('東森購物', len(price.etmall())))
    #     print(('YAHOO購物', len(price.yahoo())))
    #     print(('PCHOME購物', len(price.pchome())))
    #     print(('MOMO購物', len(price.momo())))
    #     print(('UDN購物', len(price.udn())))
    #     print(('gohappy', len(price.gohappy())))
    # price = price_compare("PS4 CUH")
    # print(price.correct_product_name)
    # print(('ASAP購物', price.asap()))
    # print(('森森購物', price.umall()))
    # print(('東森購物', price.etmall()))
    # print(('YAHOO購物', price.yahoo()))
    # print(('PCHOME購物', price.pchome()))
    # print(('MOMO購物', price.momo()))
    # print(('UDN購物',price.udn()))
    # print(('gohappy', price.gohappy()))
    # price.to_ES()
    # price = price_compare(Sunlus三樂事暖暖熱敷柔毛墊(大)-MHP811)
    # print(price.from_ES())
