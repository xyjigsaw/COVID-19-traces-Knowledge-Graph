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


class traceSpider(CrawlSpider):
    name = 'traceSpider'
    allowed_domains = ['xw.qq.com']
    start_urls = ['https://xw.qq.com/act/fytrace']

    def parse(self, response):
        item = RouteTrackItem()

        item['location'] = []
        item['pubtime'] = []
        item['info'] = []
        item['description'] = []
        item['traces'] = []
        item['source'] = []
        root_info = response.xpath('//div[@class="jsx-2527464865 root"]').extract()
        for ri in root_info:
            html_tree = etree.HTML(ri)
            try:
                loc_tmp = html_tree.xpath('//p[@class="jsx-2527464865 item location"]/span/text()')
                item['location'].extend(loc_tmp)
            except:
                item['location'].extend(' ')
            try:
                time_tmp = html_tree.xpath('//p[@class="jsx-2527464865 item pubtime"]/span/text()')
                item['pubtime'].extend(time_tmp)
            except:
                item['pubtime'].extend(' ')
            try:
                info_tmp = html_tree.xpath('//p[@class="jsx-2527464865 item info"]/span/text()')
                item['info'].extend(info_tmp)
            except:
                item['info'].extend(' ')
            try:
                des_tmp = html_tree.xpath('//p[@class="jsx-2527464865 item other"]/span/text()')
                item['description'].extend(des_tmp)
            except:
                item['description'].extend(' ')
            try:
                src_tmp = html_tree.xpath('//p[@class="jsx-2527464865 source"]/a/text()')
                item['source'].extend(src_tmp)
            except:
                item['source'].extend(' ')

            try:
                traces_tmp = html_tree.xpath('//ol[@class="jsx-2527464865 traces"]//li/p//text()')
                dicx = dict(zip(traces_tmp[::2], traces_tmp[1::2]))
                item['traces'].append(str(dicx))
            except:
                item['traces'].extend(' ')

        yield item

    def remove_html(self, string):
        pattern = re.compile(r'<[^>]+>')
        return (re.sub(pattern, '', string).replace('\n', '')).strip()

