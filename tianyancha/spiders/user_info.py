# -*-coding:utf-8 -*-
# 
# Created on 2016-03-01, by felix
# 

__author__ = 'felix'

import scrapy
import json
import urllib

from ..items import TianyanchaItem
from scrapy.http.request import Request


class TianyanchaSpider(scrapy.Spider):
    name = "user_info"
    allowed_domains = ["www.tianyancha.com"]
    start_urls = ['http://www.tianyancha.com']
    company_name = ''

    def __init__(self, company_name, *args, **kwargs):
        super(TianyanchaSpider, self).__init__(*args, **kwargs)
        self.company_name = company_name

    def parse(self, response):
        url = "http://www.tianyancha.com/search/%s.json" % (urllib.quote(self.company_name),)
        yield Request(url, callback=self.parse_page)

    def parse_page(self, response):
        response_content = json.loads(response.body)
        total = int(response_content['totalPage']) if response_content['totalPage'] else 0
        i = 1
        while i <= total:
            yield Request("http://www.tianyancha.com/search/%s.json?pn=%s" % (urllib.quote(self.company_name), i), callback=self.parse_id)
            i += 1

    def parse_id(self, response):
        response_content = json.loads(response.body)
        for data in response_content['data']:
            yield Request("http://www.tianyancha.com/company/%s.json" % (data['id'],), callback=self.parse_info)

    def parse_info(self, response):
        response_content = json.loads(response.body)
        res_data = response_content['data']['baseInfo']

        item = TianyanchaItem()
        item["name"] = res_data["name"].encode('gbk', 'ignore') if res_data.has_key("name") else ''
        item["phone"] = res_data["phoneNumber"] if res_data.has_key("phoneNumber") else ''
        item["address"] = res_data["regLocation"].encode('gbk', 'ignore') if res_data.has_key("regLocation") else ''
        item["email"] = res_data["email"] if res_data.has_key("email") else ''
        return item