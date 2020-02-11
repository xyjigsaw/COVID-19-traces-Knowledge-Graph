# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

'''
    location = scrapy.Field()
    pubtime = scrapy.Field()
    info = scrapy.Field()
    description = scrapy.Field()
    traces = scrapy.Field()
    source = scrapy.Field()
'''
import csv
import pandas as pd


class RouteTrackPipeline(object):
    def process_item(self, item, spider):
        # f = open('track.csv', 'a', encoding='utf-8')
        # csv_writer = csv.writer(f)
        # csv_writer.writerow(["位置", "发布时间", "病患信息", "其他信息", "行为轨迹", "来源"])
        # csv_writer.writerow(item['location'])
        # csv_writer.writerow(item['pubtime'])
        # csv_writer.writerow(item['info'])
        # csv_writer.writerow(item['description'])
        # csv_writer.writerow(item['traces'])
        # csv_writer.writerow(item['source'])
        # f.close()
        dataframe = pd.DataFrame({"位置": item['location'], "发布时间": item['pubtime'], "病患信息": item['info'],
                                  "其他信息": item['description'], "行为轨迹": item['traces'], "来源": item['source']})
        # 将DataFrame存储为csv,index表示是否显示行名，default=True
        dataframe.to_csv(r"track.csv", sep=',')

        '''
        dataframe = pd.DataFrame({"位置": item['location']})
        # 将DataFrame存储为csv,index表示是否显示行名，default=True
        dataframe.to_csv(r"location.csv", sep=',')

        dataframe = pd.DataFrame({"发布时间": item['pubtime']})
        # 将DataFrame存储为csv,index表示是否显示行名，default=True
        dataframe.to_csv(r"pubtime.csv", sep=',')

        dataframe = pd.DataFrame({"病患信息": item['info']})
        # 将DataFrame存储为csv,index表示是否显示行名，default=True
        dataframe.to_csv(r"info.csv", sep=',')

        dataframe = pd.DataFrame({"其他信息": item['description']})
        # 将DataFrame存储为csv,index表示是否显示行名，default=True
        dataframe.to_csv(r"other.csv", sep=',')

        dataframe = pd.DataFrame({"行为轨迹": item['traces']})
        # 将DataFrame存储为csv,index表示是否显示行名，default=True
        dataframe.to_csv(r"trace.csv", sep=',')
        '''

        return item
