from bs4 import BeautifulSoup
import urllib.request
import random
import re
import json
import requests


class price_compare():

    def __init__(self, product_name):

        def replace_string():
            replace_string = ['/', ':', '【', '】', '《', '》', '+', '※', '(', ')', '_']
            for i in self.product_name:
                if i in replace_string:
                    self.product_name = self.product_name.replace(i, ' ')
            return self.product_name.replace('福利網獨享', '')

        self.product_name = product_name
        self.correct_product_name = replace_string()
        self.encode_pro_name = urllib.parse.quote(self.correct_product_name)
        self.__momo_url = 'http://www.momoshop.com.tw/mosearch/' + self.encode_pro_name + '.html'
        self.__pchome_url = 'http://ecshweb.pchome.com.tw/search/v3.3/all/results?q=' + self.encode_pro_name + '&page=1&sort=rnk/dc'
        self.__yahoo_url = 'https://tw.search.buy.yahoo.com/search/shopping/product?p=' + self.encode_pro_name + '&qt=product&cid=&clv='
        self.__udn_url = 'http://shopping.udn.com/mall/cus/search/SearchAction.do?start=1&keyword=' + self.encode_pro_name + '&cid=&sort=weight&pickup=&minP=&maxP=&pageSize=20&key=32303137303230f7f25da1a0ab06cd67c0'
        self.__etmall_url = 'http://www.etmall.com.tw/Pages/AllSearchFormResult.aspx'

    def print(self):
        print(self.correct_product_name)
        # self.correct_product_name = self.replace_string()                   ####產品名稱
        # self.encode_pro_name = urllib.parse.quote(self.correct_product_name)  ####url encode

    # def get_page(self, url):
    #
    #     request = urllib.request.Request(url)
    #
    #     ####隨機header挑選####
    #     foo = [
    #         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',
    #         'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko',
    #         'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
    #         'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_7; da-dk) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1'
    #         'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
    #         'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2722.0 Safari/537.36'
    #         'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
    #     ]
    #     headers = str(random.choice(foo))
    #     ####隨機header挑選####
    #
    #     request.add_header('User-Agent', headers)
    #     response = urllib.request.urlopen(request, timeout=180)
    #     html = BeautifulSoup(response.read().decode('utf-8'), 'lxml')
    #     response.close()
    #
    #     return html
    def get_page(self, url, parameters=None):

        if parameters:
            encode_parameters = urllib.parse.urlencode(parameters).encode('utf-8')
        else:
            encode_parameters = None

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
        response = urllib.request.urlopen(request, data=encode_parameters, timeout=180)
        html = BeautifulSoup(response.read().decode('utf-8'), 'lxml')
        response.close()

        return html

    def get_page2(self, url):

        request = urllib.request.Request(url)

        ####隨機header挑選####
        foo = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',
            'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_7; da-dk) AppleWebKit/533.21.1 (KHTML, li e Gecko) Version/5.0.5 Safari/533.21.1'
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2722.0 Safari/537.36'
            'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
        ]
        headers = str(random.choice(foo))
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
            for i in result.find_all('ul', {'id': 'chessboard'}):
                for x in i.find_all(['a', 'b']):
                    #                 if x.text != '' and len(momo) != 8:
                    if x.text != '':
                        momo.append(x.text)
        else:
            for i in result.find_all('script'):
                momo_goods_url = i.text.strip('location.href=').strip(';').strip('\'"').replace(',', '')

            momo_goods_detail = self.get_page2(momo_goods_url)
            for i in momo_goods_detail.find_all('div', {'class': 'prdnoteArea'}):
                for product in i.find('h1'):
                    momo.append(product)
                for prices in i.find_all('li', {'class': 'special'}):
                    for price in prices.find('span'):
                        momo.append(price.replace(',', ''))
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
                gohappy_list.append(product.text.replace('\n', ''))
            for price in elements.find_all('strong'):
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
            for elements in result.find_all('div', {'class': 'wrap yui3-g'}):
                for product in elements.find_all('div', {'class': 'yui3-u srp-pdcontent'}):
                    yahoo.append(product.text.replace('\n', ''))
                for prices in elements.find_all('div', {'class': 'srp-pdprice'}):
                    for price in prices.find_all('span', {'class': 'srp-listprice-class'}):
                        yahoo.append(price.text.replace('$', ''))
        elif result.find_all('div', {'class': 'srp-pdcontent'}):
            for elements in result.find_all('div', {'class': 'srp-pdcontent'}):
                for product in elements.find_all('div', {'class': 'srp-pdtitle'}):
                    yahoo.append(product.text.replace('\n', ''))
                for prices in elements.find_all('div', {'class': 'srp-pdprice'}):
                    if prices.find_all('div', {'class': 'srp-actprice'}):
                        for price in prices.find_all('div', {'class': 'srp-actprice'}):
                            yahoo.append(price.text.replace('活動價 $', '').replace('起', ''))
                    else:
                        for price in prices.find_all('div', {'class': 'srp-listprice'}):
                            yahoo.append(price.text.replace('網路價 $', ''))
                            #             yahoo.append(price.text.replace('$',''))

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

        def udn_pro_pages(search):

            result = self.get_page(self.__udn_url)
            udn_pages = list()
            for pages in result.find_all('li', {'class': 'pager_item'}):
                page = pages.text.replace('\n', '').replace('\r', '').replace('\t', '')
                udn_pages.append(page)
                if '下一頁' in udn_pages:
                    udn_pages.remove('下一頁')

            return udn_pages

        udn_list = list()
        pages = udn_pro_pages(self.encode_pro_name)
        for page in pages:
            result = self.get_page("http://shopping.udn.com/mall/cus/search/SearchAction.do?start=" + str(page) + "&keyword="
                     + self.encode_pro_name + "&cid=&sort=weight&pickup=&minP=&maxP=&pageSize=20&key=32303137303230f7f25da1a0ab06cd67c0")
            for elements in result.find_all('li', {'class': 'lv3_item'}):
                for product in elements.find_all('p', {'class': 'pd_name'}):
                    udn_list.append(product.text)
                for price in elements.find_all('p', {'class': 'pd_price'}):
                    udn_list.append(price.text.replace('\n', '').replace('\t', '').replace('\r', '').replace('限時', ''))

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
                price = result_dict.get('data').get(i).get('market_info').get('price').get('final_price').get('price')
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

        parameters = {'SearchKeyword': self.correct_product_name,
                      'SearchKey': self.correct_product_name,
                      'ProductPage': '0',
                      'RecordsPerPage': '40',
                      'OrderBy': '_weight_,DESC'}

        result = str(self.get_page(self.__etmall_url, parameters = parameters))
        return result
        # pat_product = 'aPL_GOODNM\[.*?\)'
        # # pat2='aPL_PRC\[.*?\;'
        # pat_price = 'aPL_DISCOUNT_VALUE\[.*?\;'
        # product = re.findall(pat_product, result)
        # price = re.findall(pat_price, result)
        #
        # etmall_list = list()
        # for i in range(len(product)):
        #     product_remove = re.sub(r"^aPL.*\car\('", '', product[i]).replace("')", '')
        #     price_remove = re.sub(r"^aPL.*\= \'", '', price[i]).replace("';", '')
        #     etmall_list.extend([product_remove, price_remove])
        #
        # ####將結果變成list裡面包tuple(產品, 價格)####
        # etmall_display = list()
        # a, b = 0, 2
        # x = int(len(etmall_list) / 2)
        # while x != 0:
        #     etmall_display.append(tuple(etmall_list[a:b]))
        #     x -= 1
        #     a, b = b, b + 2
        # ####將結果變成list裡面包tuple(產品, 價格)####
        # return etmall_display


    def umall(self):

        parameters = {'SearchKeyword': self.correct_product_name,
                      'SearchKey': self.correct_product_name,
                      'ProductPage': '0',
                      'RecordsPerPage': '40',
                      'OrderBy': '_weight_,DESC'}

        result = str(self.get_page('http://www.u-mall.com.tw/Search.aspx', parameters=parameters))
        pat_product = 'Tmp = changecar\(\'.*?\)'
        pat_price = 'Sys_showPRCValue\(.*?\)'
        product = re.findall(pat_product, result)
        price_error_string = re.findall(pat_price, result)

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

        from elasticsearch import Elasticsearch
        es = Elasticsearch([{'host': '10.10.110.155', 'port': 9200}])

        momo_data = self.momo()
        pchome_data = self.pchome()
        payeasy_data = self.payeasy()

        ####計算資料的index####
        def counter():
            len_all = len(momo_data + pchome_data + payeasy_data)
            yield from range(len_all)

        counter = counter()
        ####計算資料的index####

        ####insert momo data into elasticsearch#####
        momo_dict = dict()

        for i in range(len(momo_data)):
            momo_dict['name'] = momo_data[i][0]
            momo_dict['price'] = int(momo_data[i][1])
            momo_dict['company'] = 'momo'
            es.index(index='product', doc_type='3C', id=next(counter), body=momo_dict)
        ####insert momo data into elasticsearch#####

        ####insert pchome data into elasticsearch####
        pchome_dict = dict()

        for i in range(len(pchome_data)):
            pchome_dict['name'] = pchome_data[i][0]
            pchome_dict['price'] = int(pchome_data[i][1])
            pchome_dict['company'] = 'pchome'
            es.index(index='product', doc_type='3C', id=next(counter), body=pchome_dict)
        ####insert pchome data into elasticsearch####

        ####insert payeasy data into elasticsearch####
        payeasy_dict = dict()

        for i in range(len(payeasy_data)):
            payeasy_dict['name'] = payeasy_data[i][0]
            payeasy_dict['price'] = int(payeasy_data[i][1])
            payeasy_dict['company'] = 'payeasy'
            es.index(index='product', doc_type='3C', id=next(counter), body=payeasy_dict)
            ####insert payeasy data into elasticsearch####

if __name__ == '__main__':
        price = price_compare('【Nintendo】任天堂 FAMICOM Mini 經典迷你紅白機')
        # price = price_compare('【福利網獨享】iRobot Roomba 880 機器人掃地機/吸塵器 ')
        price.print()
        # print(('ASAP購物', price.asap()))
        # print(('森森購物', price.umall()))
        # print(('東森購物', price.etmall()))
        # print(('YAHOO購物', price.yahoo()))
        # print(('PCHOME購物', price.pchome()))
        # print(('MOMO購物', price.momo()))
        # print(('UDN購物', price.udn()))
        # print(('GOHAPPY購物', price.gohappy()))
        # Nintendo
        # 任天堂
        # 迷你紅白機