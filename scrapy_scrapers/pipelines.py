# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import json
import mysql.connector
from scrapy.exceptions import NotConfigured
from datetime import datetime
from scrapy.utils.project import get_project_settings



class JobItemPipeline(object):

	def __init__(self):
		db_settings = get_project_settings().getdict("DB_SETTINGS")
		logging.warning(db_settings)
		if not db_settings: # if we don't define db config in settings
			raise NotConfigured # then reaise error
		self.db = db_settings['db']
		self.user = db_settings['user']
		self.passwd = db_settings['passwd']
		self.host = db_settings['host']
		self.date = datetime.today().strftime('%Y_%m_%d')
		self.conn = None
		self.cursor = None

	def open_spider(self, spider):
		self.conn = mysql.connector.connect(db=self.db, user=self.user, passwd=self.passwd, host=self.host, charset='utf8', use_unicode=True)
		self.cursor = self.conn.cursor()
		
		tablename = spider.name + "_" + self.date
		sql = "CREATE TABLE IF NOT EXISTS `jobdb`.`" + tablename + "` ( `keyword` VARCHAR(50) NOT NULL , `location` VARCHAR(50) NOT NULL , `count` INT(25) NOT NULL) ENGINE = MyISAM;"
		
		self.cursor.execute(sql)
		self.conn.commit()

	def close_spider(self, spider):
		self.conn.close()

	def process_item(self, item, spider):
		tablename = item.get("website") + "_"+ self.date
		sql = "INSERT INTO " + tablename + " (keyword, location, count) VALUES (%s, %s, %s)"
		self.cursor.execute(sql, (item.get("keyword"), item.get("location"), item.get("count"),))
		self.conn.commit()
		return item