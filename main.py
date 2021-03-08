# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import requests
import time


def get_latest_crypto_price():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '10',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '76827abf-9adb-438a-8e9c-ef393114234e',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
    return format_data(data)


def format_data(data):
    res = [0, 0]
    if data['data'][0]['symbol'] == 'BTC':
        res[0] = data['data'][0]['quote']['USD']['price']
    if data['data'][1]['symbol'] == 'ETH':
        res[1] = data['data'][1]['quote']['USD']['price']
    return res


def send_wechat(info):
    server_chan_sckey = "SCU145296T34757c1e6fd50bd1ca4e03cc7425a3315ff3cb93dcd22"
    default_user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.3"

    """推送信息到微信"""
    url = 'http://sc.ftqq.com/{}.send'.format(server_chan_sckey)
    payload = {
        "text": 'Latest Price',
        "desp": info
    }
    headers = {
        'User-Agent': default_user_agent
    }
    requests.get(url, params=payload, headers=headers)


def weatherSend(last, now):
    last_btc = last[0]
    last_eth = last[1]
    now_btc = now[0]
    now_eth = now[1]
    #test
    # for Amt in range(46600, 55000, 1):
    #     if last_btc < Amt and now_btc >= Amt + 1:
    #         send_wechat("btc's price upupup " + str(now_btc))
    #         break
    # for Amt in range(55000, 46600, -1):
    #     if last_btc >= Amt and now_btc < Amt - 1:
    #         send_wechat("btc's price downdowndown " + str(now_btc))
    #         break

    for Amt in range(30000, 100001, 200):
        if last_btc < Amt and now_btc >= Amt + 200:
            send_wechat("btc's price upupup " + str(now_btc))
            break
    for Amt in range(100000, 29999, -200):
        if last_btc >= Amt and now_btc < Amt - 200:
            send_wechat("btc's price downdowndown " + str(now_btc))
            break
    for Amt in range(700, 3000, 20):
        if last_eth < Amt and now_eth >= Amt + 20:
            send_wechat("eth's price upupup " + str(now_eth))
            break
    for Amt in range(3000, 699, -20):
        if last_eth >= Amt and now_eth < Amt - 20:
            send_wechat("eth's price downdowndown " + str(now_eth))
            break


if __name__ == '__main__':
    # 1min to update
    last = []
    now = []
    while True:
        last = get_latest_crypto_price()
        print("last btc : " + str(last[0]) + " last eth : " + str(last[1]))
        time.sleep(61)
        now = get_latest_crypto_price()
        print("now btc : " + str(now[0]) + " now eth : " + str(now[1]))
        weatherSend(last, now)
