#! /usr/bin/env python
# -*- coding:UTF-8 -*-
import requests
#pip install pybitflyer
import pybitflyer
import json
import datetime

##ビットコインの取得時点の終値が返される
def bitflyer_api():
    api = pybitflyer.API()
    ticker = api.ticker(product_code="BTC_JPY")
    return ticker

def qitta_tags(qiita_user,page_num):

    #フォローしてるタグ情報を取得
    url = 'http://qiita.com/api/v2/users/' + qiita_user + '/following_tags'
    params = {'page': '1'}
    following_tags = requests.get(url, params=params).json()
    query = ''
    for i in range(len(following_tags)):
        query = query + 'tag:' + following_tags[i]['id'] + " OR "

    # QiitaAPIを使用してフォローしているタグを含む新着記事指定回数分取得
    url = 'http://qiita.com/api/v2/items'
    params = {'page': '1', 'per_page': page_num, 'query': query.rstrip(' OR ')}
    #params = {'page': '1', 'per_page': '10', 'query':'tags:python'}
    new_articles = requests.get(url, params=params).json()
    tmp = []

    for i in new_articles:
        #print(i["title"])
        tmp.append(i["url"])

    return tmp

def line_stamp(mesg,url,token):
    headers = {"Authorization": "Bearer " + token}
    message = '\n'
    message += mesg
    #送信内容とLINEスタンプの設定
    payload = {
    'message': message,
    'stickerPackageId': 1,
    'stickerId': 100,
    }

    r = requests.post(url, headers=headers, params=payload)

def line(mesg,url,token):
    headers = {"Authorization": "Bearer " + token}
    message = '\n'
    message += mesg
    payload = {"message":  message}
    requests.post(url, headers=headers, params=payload)

if __name__ == '__main__':
    """
    日付、スタンプ,BitCoinの終値、自分がフォローしてるtagのqiitaの記事（指定分）を返却する
    """
    url = "https://notify-api.line.me/api/notify"
    token = "Your Line Notify Access Token"

    #送信処理
    now = datetime.datetime.today()
    line_stamp(str(now.strftime('%Y-%m-%d %H:%M')),url,token)
    bit_data = bitflyer_api()
    line(bit_data["product_code"]+"\n"+str(bit_data["timestamp"])+"\n"+ "{:,.0f}".format(bit_data["ltp"])+"円",url,token)
    qiita_pages = qitta_tags("Your Qiita Account","5")#qiitaのアカウントと返却する記事の数
    #返却されたqiitaのページURL分送信
    for i in qiita_pages:
        line(i,url,token)
