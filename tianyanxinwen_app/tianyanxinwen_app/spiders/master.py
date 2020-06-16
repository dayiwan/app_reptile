# -*- coding: utf-8 -*-
import scrapy
import json
import time
from urllib.parse import urljoin
from scrapy import Request
from urllib.parse import urlencode
from ..items import TianyanxinwenAppItem


class MasterSpider(scrapy.Spider):
    name = 'master'
    start_url = 'http://jgz.app.todayguizhou.com/appAPI/nav-mylist.html?'
    news_list_host = 'http://jgz.app.todayguizhou.com/appAPI/news-getCatePage.html?'

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
            cate_name = category['cate_name']
            yield Request(url=url, callback=self.news_list_parse, meta={'cate_name': cate_name})
            """翻页,只翻前100页"""
            for page in range(2, 100):
                data = {
                    'cate_id': category['cate_id'],
                    'page': str(page)
                }
                next_url = self.news_list_host + urlencode(data)
                yield Request(url=next_url, callback=self.news_list_parse, meta={'cate_name': cate_name})

    def news_list_parse(self, response):
        """获取新闻详情链接"""
        special_host = 'http://jgz.app.todayguizhou.com/appAPI/special-index.html'
        news_list = json.loads(response.text)['data']['list']
        for news in news_list:
            info_dict = dict()
            if news['is_special'] == 1:     # 判断该新闻是否是专题新闻
                special_data = {'special_id': news['special_id']}
                special_url = special_host + urlencode(special_data)
                yield Request(url=special_url, callback=self.news_list_parse, meta={'cate_name': response.meta['cate_name']})
            else:
                news_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(news['news_addtime'])))
                news_url = news['shareurl']
                info_dict['url'] = news_url
                info_dict['title'] = news['news_title']
                info_dict['author'] = news['news_reporterName']
                info_dict['category'] = response.meta['cate_name']
                info_dict['time'] = news_time
                yield Request(url=news_url, callback=self.news_detail_parse, meta=info_dict)

    def news_detail_parse(self, response):
        """获取新闻详情"""
        item = TianyanxinwenAppItem()
        host = 'http://jgz.app.todayguizhou.com'
        content = response.xpath('normalize-space(//div[@class="detail-item"])').extract()[0]
        img_list = response.xpath('//img/@src').extract()
        item['img_list'] = list()
        if len(img_list) > 0:
            for img in img_list:
                'http' in img or item['img_list'].append(urljoin(host, img))
        item['title'] = response.meta['title']
        item['author'] = response.meta['author']
        item['category'] = response.meta['category']
        item['time'] = response.meta['time']
        item['content'] = content
        print(item['img_list'])

