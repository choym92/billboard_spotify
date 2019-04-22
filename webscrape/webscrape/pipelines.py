# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import CsvItemExporter

class WebscrapePipeline(object):
    # def process_item(self, item, spider):
    #     return item



    # __init__ will define the filename of the csv.
    def __init__(self):
        self.filename = 'billboard_top100.csv'
    # open the csv and begin to use CsvItemExporter object and start exporting
    def open_spider(self, spider):
        self.csvfile = open(self.filename, 'wb')
        self.exporter = CsvItemExporter(self.csvfile)
        self.exporter.start_exporting()
    # finish exporting then close csv
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.csvfile.close()
    # handles each item object that was yielded in the scraper
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
    