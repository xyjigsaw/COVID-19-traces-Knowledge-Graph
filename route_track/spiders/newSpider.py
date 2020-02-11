# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from route_track.items import RouteTrackItem
from lxml import etree
import re
'''
    location = scrapy.Field()
    pubtime = scrapy.Field()
    info = scrapy.Field()
    description = scrapy.Field()
    traces = scrapy.Field()
    source = scrapy.Field()
'''


class NewspiderSpider(CrawlSpider):
    name = 'newSpider'
    allowed_domains = ['xw.qq.com']
    start_urls = ['https://xw.qq.com/act/fytrace']

    def parse(self, response):
        item = RouteTrackItem()
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()

        item['location'] = response.xpath('//p[@class="jsx-2527464865 item location"]/span/text()').extract()
        item['pubtime'] = response.xpath('//p[@class="jsx-2527464865 item pubtime"]/span/text()').extract()
        item['info'] = response.xpath('//p[@class="jsx-2527464865 item info"]/span/text()').extract()
        item['description'] = response.xpath('//p[@class="jsx-2527464865 item other"]/span/text()').extract()
        # item['source'] = response.xpath('//p[@class="jsx-2527464865 source"]/a/text()').extract()
        raw_traces = response.xpath('//ol[@class="jsx-2527464865 traces"]').extract()
        item['traces'] = []
        for i in raw_traces:
            tmp = (etree.HTML(i)).xpath('//li/p//text()')
            dicx = dict(zip(tmp[::2], tmp[1::2]))
            item['traces'].append(str(dicx))
        del_index = self.get_undefined(item['location'], 'undefined  ')
        item['location'] = [item['location'][i] for i in range(0, len(item['location']), 1) if i not in del_index]
        item['pubtime'] = [item['pubtime'][i] for i in range(0, len(item['pubtime']), 1) if i not in del_index]
        item['info'] = [item['info'][i] for i in range(0, len(item['info']), 1) if i not in del_index]
        item['description'] = [item['description'][i] for i in range(0, len(item['description']), 1) if i not in del_index]

        print(len(item['location']), len(item['pubtime']), len(item['info']), len(item['description']), len(item['traces']))

        yield item

    def remove_html(self, string):
        pattern = re.compile(r'<[^>]+>')
        return (re.sub(pattern, '', string).replace('\n', '')).strip()

    def get_undefined(self, lst, item):
        return [index for (index, value) in enumerate(lst) if value == item]

