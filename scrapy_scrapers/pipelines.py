# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import json
import MySQLdb
from scrapy.exceptions import NotConfigured
from datetime import datetime



class JobItemPipeline(object):
	def __init__(self, db, user, passwd, host):
        self.db = db
        self.user = user
        self.passwd = passwd
        self.host = host
        self.date = datetime.today().strftime('%Y_%m_%d')

    def from_crawler(cls, crawler):
	    db_settings = crawler.settings.getdict("DB_SETTINGS")
	    if not db_settings: # if we don't define db config in settings
	        raise NotConfigured # then reaise error
	    db = db_settings['db']
	    user = db_settings['user']
	    passwd = db_settings['passwd']
	    host = db_settings['host']
	    return cls(db, user, passwd, host) # returning pipeline instance

    def open_spider(self, spider):
        self.conn = MySQLdb.connect(db=self.db,
                                user=self.user, passwd=self.passwd,
                                host=self.host,
                                charset='utf8', use_unicode=True)
    	self.cursor = self.conn.cursor()
    	#
    	#Create tables if they dont exist somewhere in here using this tablename convention
    	#
    	tablename = item.get("website") + "_"+ self.date

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
    	tablename = item.get("website") + "_"+ self.date
        sql = "INSERT INTO " + tablename + " (keyword, location, count) VALUES (%s, %s, %i)"
    	self.cursor.execute(sql,
                        (
                            item.get("keyword"),
                            item.get("location"),
                            item.get("count"),
                        )
                       )
   	 	self.conn.commit()
        return item