#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: Evan
# @Time: 2020/6/8

import requests
url = 'https://mapi.gzstv.com/v2/news/news_list/'
header = {
    'Accept': 'application/json;charset=utf-8',
    'Accept-Encoding': 'gzip',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; OPPO R17 Pro Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36 DJ-CDNT/218',
    'Content-Type': 'application/json;charset=utf-8',
    'Connection': 'Keep-Alive'
}
data = {
    'signature': 'ab145d65d824fb4264537ef4cf4d9425',
    'token': '0c3ad253a813471c5896116199cf30efa2b1ccf260304e0561a6ca7b489ab044',
    'parameter': {"from_pk": 259819, "num": 10, "category_id": 1, "mc_cid": 0}
}
res = requests.post(url=url,verify=False, headers=header, data=data)
print(res.text)
