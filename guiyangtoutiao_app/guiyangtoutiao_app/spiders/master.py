# -*- coding: utf-8 -*-
import scrapy, json
import time
from scrapy import FormRequest


class MasterSpider(scrapy.Spider):
    name = 'master'
    time = int(time.time()*1000)
    data = {
        'platform': 'Android',
        'deviceId': '65ba2b90bb3ec5',
        'check_sum': '21539f05349a11ebf1435e388462bca0',
        # 'categoryId': '4_GUIDELIST_5002000000000000',
        'categoryType': 'category',
        # 'pageSize': '10',
        'ecAppId': '4',
        'version': '1',
        'api_token': '424f8e2f-b8ed-4b32-9a5e-e9f11c4c8889',
        'timestamp': str(time),
        'appId': '615df35e-246c-4a88-9430-356f7d36f2cd',
        'nonce': '498e3d20-1992-4f4d-925d-707a25d6997c'
    }
    start_url = 'http://phone.gyntv.com.cn:9090/mi/r/ec3_mi_api/MiApiAction!myChannelList.do'
    url = 'http://phone.gyntv.com.cn:9090/mi/r/ec3_pub/v1.0/getNewsListByCategoryId'
    get_cookie = {"code": 1,
                  "result": {
                      "sysTime": "1592190069335",
                      "data": {
                          "allowMakeTask": "0",
                          "email": "",
                          "icon": "",
                          "inviCode": "",
                          "level": "1",
                          "name": "客户端外网应用用户",
                          "phone": "",
                          "qqOpenId": "",
                          "role": "普通",
                          "roleKind": "100",
                          "score": "0",
                          "seed": "98e6e575468e03e7124a060a6470fa7e",
                          "token": "d0328aef-6a6c-42ec-992b-91c4d7520235",
                          "userId": "200509766",
                          "wbOpenId": "",
                          "wxOpenId": ""}
                  }}

    def start_requests(self):
        yield FormRequest(url=self.start_url, formdata=self.data, callback=self.news_list_parse)

    def news_list_parse(self, response):
        print(response, '1111111111111')
        res = json.loads(response.text)
        print(res)
