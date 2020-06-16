# -*- coding: utf-8 -*-
import scrapy
import json
import time
from scrapy import Request
from urllib.parse import urlencode


class MasterSpider(scrapy.Spider):
    name = 'master'
    start_url = 'http://jgz.app.todayguizhou.com/appAPI/nav-mylist.html?'
    news_list_host = 'http://jgz.app.todayguizhou.com/appAPI/news-getCatePage.html?'
    # dt = "2019-01-01 00:00:00"
    # # 转换成时间数组
    # timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    # # 转换成时间戳
    # timestamp = int(time.mktime(timeArray))
    # if_next_page = True

    def start_requests(self):
        """获取新闻类别列表"""
        data = {
            'city': '贵阳',
            'versionCode': '524'
        }
        url = self.start_url + urlencode(data)
        yield Request(url=url, callback=self.news_category_parse)

    def news_category_parse(self, response):
        """获取不同新闻类别里的新闻列表"""
        category_list = json.loads(response.text)['data']['category_list']
        for category in category_list:
            url = self.news_list_host + urlencode({'cate_id': category['cate_id']})
            yield Request(url=url, callback=self.news_list_parse)
            """翻页,只翻前100页"""
            # self.if_next_page = True
            # page_num = 2
            for page in range(2, 100):
                data = {
                    'cate_id': category['cate_id'],
                    'page': str(page)
                }
                next_url = self.news_list_host + urlencode(data)
                yield Request(url=next_url, callback=self.news_list_parse)
            #     page_num += 1

    def news_list_parse(self, response):
        """获取新闻详情链接"""
        special_host = 'http://jgz.app.todayguizhou.com/appAPI/special-index.html'
        news_list = json.loads(response.text)['data']['list']
        for news in news_list:
            # print(news['news_addtime'])
            if news['is_special'] == 1:     # 判断该新闻是否是专题新闻
                special_data = {'special_id': news['special_id']}
                special_url = special_host + urlencode(special_data)
                yield Request(url=special_url, callback=self.news_list_parse)
            else:
                news_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(news['news_addtime'])))
                news_url = news['shareurl']
                yield Request(url=news_url, callback=self.news_detail_parse, meta={'time': news_time})

            # if int(news['news_addtime']) < self.timestamp:   # 如果某一条新闻的时间早于2019年一月一日，就不再翻页
            #     self.if_next_page = False
            #     break
            # print(news['news_title'])
        # print('------------', response.meta['cate_name'], '------------------')

    def news_detail_parse(self, response):
        """获取新闻详情"""
        try:
            title = response.xpath('//div[@class="detail warpper"]/h1/text()').extract()[0]
        except:
            title = response.xpath('//title/text()').extract()[0]
        content = response.xpath('normalize-space(//div[@class="detail-item"])').extract()[0]
        print('----------', title, '-----------------')
        print('!!!!!!!!!!', response.meta['time'], '!!!!!!!!!!!!!!!')
        print(content)
