import time
import random
import requests
import json

def get_myself_order():
    headers = {
        'authority': 'buyertrade.taobao.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'origin': 'https://buyertrade.taobao.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://buyertrade.taobao.com/trade/itemlist/list_bought_items.htm?spm=a21bo.jianhua.1997525045.2.5af911d9htImtW',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,en-US;q=0.6',
        # 添加自己的cookie
        'cookie': '您的cookie',
    }

    params = (
        ('action', 'itemlist/BoughtQueryAction'),
        ('event_submit_do_query', '1'),
        ('_input_charset', 'utf8'),
    )
    # 输入要爬取的页数
    for page in range(1,18):
        data = {
          'canGetHistoryCount': 'false',
          'historyCount': '0',
          'needQueryHistory': 'false',
          'onlineCount': '0',
          'pageNum': page,
          'pageSize': '15',
          'queryForV2': 'false',
          'prePageNo': page-1
        }
        time.sleep(random.randint(1,2))
        response = requests.post('https://buyertrade.taobao.com/trade/itemlist/asyncBought.htm', headers=headers, params=params, data=data)
        data = response.json()
        orders = data['mainOrders']
        for order in orders:
            try:
                order_name = order['subOrders'][0]['itemInfo']['title']
                order_time = order['orderInfo']['createDay']
                order_number = order['orderInfo']['id']
                order_price = order['subOrders'][0]['priceInfo']['realTotal']
                order_shop = order['seller']['nick']
            except:
                order_shop = order['seller']['shopName']
            result = {
                'order_name':order_name,
                'order_time': order_time,
                'order_number': order_number,
                'order_price': order_price,
                'order_shop': order_shop,

            }
            with open('myself_order.txt','a',encoding='utf-8')as f:
                f.write(str(result)+'\n')
            print(result)
get_myself_order()
