from bs4 import BeautifulSoup
import urllib.request
import random

def get_page(url, parameters=None):
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
#
#
#
# def pchome():
#     import json
#
#     pchome = sget_page()
#
#     pchome_data = dict()
#     for x in pchome.find_all('p'):
#         item_data = json.loads(x.text)
#         pchome_data = item_data['prods']
#
#     pchome_display = [(i['name'], int(i['price'])) for i in pchome_data]
#
#     return pchome_display
#
#
# if __name__ == '__main__':
#     print('''{"QTime":30,"totalRows":6,"totalPage":1,"range":{"min":600,"max":4280},"cateName":"","q":"Nintendo \u8ff7\u4f60\u7d05\u767d\u6a5f Famicom Mini","subq":"","token":["Nintendo","\u8ff7\u4f60","\u8ff7","\u4f60","\u7d05\u767d","\u7d05","\u767d","\u6a5f","Famicom","Mini"],"prods":[{"Id":"DGBJAP-A9007TQ2V","cateId":"DGBJAP","picS":"\/pic\/v1\/data\/item\/201701\/D\/G\/B\/J\/A\/P\/sDGBJAP-A9007TQ2V000_587de8fe7bd6e.jpg","picB":"\/pic\/v1\/data\/item\/201701\/D\/G\/B\/J\/A\/P\/DGBJAP-A9007TQ2V000_587de8fe79a3a.jpg","name":"\u4efb\u5929\u5802 Nintendo \u8ff7\u4f60\u7d05\u767d\u6a5f Famicom Mini","describe":"\u4efb\u5929\u5802 Nintendo \u8ff7\u4f60\u7d05\u767d\u6a5f Famicom Mini","price":3888,"author":"","brand":"","publishDate":"","isNC17":0,"couponActid":[]},{"Id":"DGBJ88-A9007Q6J0","cateId":"DGBJAP","picS":"\/pic\/v1\/data\/item\/201612\/D\/G\/B\/J\/8\/8\/sDGBJ88-A9007Q6J0000_584f75e8bf6fe.jpg","picB":"\/pic\/v1\/data\/item\/201702\/D\/G\/B\/J\/8\/8\/DGBJ88-A9007Q6J0000_58983d2d60f4e.jpg","name":"\u4efb\u5929\u5802\u7d93\u5178\u8ff7\u4f60\u7d05\u767d\u6a5f","describe":"\u25bc\u6bcf\u65e5\u5f37\u6a94\u2027\u760b\u6bba\u7279\u8ce3\u25bc\u4efb\u5929\u5802\u7d93\u5178\u8ff7\u4f60\u7d05\u767d\u6a5f","price":3688,"author":"","brand":"","publishDate":"","isNC17":0,"couponActid":[]},{"Id":"QAAS0W-A9007RR22","cateId":"QAAF6U","picS":"\/pic\/v1\/data\/item\/201612\/Q\/A\/A\/S\/0\/W\/sQAAS0W-A9007RR22000_5864a7fbcd350.jpg","picB":"\/pic\/v1\/data\/item\/201702\/Q\/A\/A\/S\/0\/W\/QAAS0W-A9007RR22000_589292bd18f91.jpg","name":"\u4efb\u5929\u5802 Nintendo \u8ff7\u4f60\u7d05\u767d\u6a5f Famicom Mini ","describe":"\u4efb\u5929\u5802 Nintendo \u8ff7\u4f60\u7d05\u767d\u6a5f Famicom Mini ","price":3980,"author":"","brand":"","publishDate":"","isNC17":0,"couponActid":[]},{"Id":"QAAS0W-A9007R5G6","cateId":"QAAF6U","picS":"\/pic\/v1\/data\/item\/201612\/Q\/A\/A\/S\/0\/W\/sQAAS0W-A9007R5G6000_585b774eef9fd.jpg","picB":"\/pic\/v1\/data\/item\/201612\/Q\/A\/A\/S\/0\/W\/QAAS0W-A9007R5G6000_58631893065c6.jpg","name":"\u4efb\u5929\u5802 Nintendo Famicom Mini \u3010\u8ff7\u4f60\u7d05\u767d\u6a5f\u3011(\u964430\u6b3e\u7d93\u5178\u61f7\u820a\u6b3e\u904a\u6232) ","describe":"\u4efb\u5929\u5802 Nintendo Famicom Mini \u3010\u8ff7\u4f60\u7d05\u767d\u6a5f\u3011","price":4280,"author":"","brand":"","publishDate":"","isNC17":0,"couponActid":[]},{"Id":"DGBJAP-A9007QWD0","cateId":"DGBJAP","picS":"\/pic\/v1\/data\/item\/201612\/D\/G\/B\/J\/A\/P\/sDGBJAP-A9007QWD0000_5858c6ff81de1.jpg","picB":"\/pic\/v1\/data\/item\/201612\/D\/G\/B\/J\/A\/P\/DGBJAP-A9007QWD0000_5858c6ff8028a.jpg","name":"\u4efb\u5929\u5802 FAMICOM \u8ff7\u4f60\u7248 \u7d05\u767d\u6a5f","describe":"\u4efb\u5929\u5802 FAMICOM \u8ff7\u4f60\u7248 \u7d05\u767d\u6a5f","price":3980,"author":"","brand":"","publishDate":"","isNC17":0,"couponActid":[]},{"Id":"DGBJAP-A9007T4FS","cateId":"DGBJAP","picS":"\/pic\/v1\/data\/item\/201701\/D\/G\/B\/J\/A\/P\/sDGBJAP-A9007T4FS000_58777f4b2a9ca.jpg","picB":"\/pic\/v1\/data\/item\/201701\/D\/G\/B\/J\/A\/P\/DGBJAP-A9007T4FS000_58777f4b272ec.jpg","name":"\u4efb\u5929\u5802\u8ff7\u4f60\u7d05\u767d\u6a5f-\u539f\u5ee0\u5c08\u7528\u8b8a\u58d3\u5668","describe":"\u4efb\u5929\u5802\u8ff7\u4f60\u7d05\u767d\u6a5f-\u539f\u5ee0\u5c08\u7528\u8b8a\u58d3\u5668","price":600,"author":"","brand":"","publishDate":"","isNC17":0,"couponActid":[]}]}''')

def gohappy(search):

    encode_search = urllib.parse.quote(search)
    result = get_page('http://www.gohappy.com.tw/ec2/search?sid=&hotNum=0&search=' + encode_search)

    gohappy = list()
    for elements in result.find_all('ol', {'class': 'proddata-list'}):
        for product in elements.find_all('h3'):
            gohappy.append(product.text.replace('\n', ''))
        for price in elements.find_all('strong'):
            gohappy.append(price.text)


    ####將結果變成list裡面包tuple(產品, 價格)####
    gohappy_display = list()
    a, b = 0, 2
    x = int(len(gohappy) / 2)
    while x != 0:
        gohappy_display.append(tuple(gohappy[a:b]))
        x -= 1
        a, b = b, b + 2
    ####將結果變成list裡面包tuple(產品, 價格)####

    return gohappy_display

print(gohappy('Nintendo 任天堂 迷你紅白機'))






















