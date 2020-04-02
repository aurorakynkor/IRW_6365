from __future__ import absolute_import
import scrapy
import logging
import time
import requests
import pandas as pd
import numpy as np
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer
from scrapy.utils.log import configure_logging
from scrapy_scrapers.items import JobCountItem

#
# Get Keywords and Locations from text file or DB up here and set them up so all spiders can see them
#

locations = []
keywords = []

#
# Define Spiders Here
#
class MonsterSpider(scrapy.Spider):
    name = "monster_spider"

    def start_requests(self):
        urls = []

        for job_keyword in keywords:
            for job_location in locations:
                urls.append("https://www.monster.com/jobs/search/?q="+ job_keyword +"&rad=5&where="+ job_location +"&tm=7")

        #creates a scrapy request for those pages
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        #Note to self, monster doesn't do 404 when it errors

        start_keyword = "https://www.monster.com/jobs/search/?q="
        end_keyword = response.url.find("&rad=5&where=")
        keyword = response.url[len(start_keyword) : end_keyword]
        keyword = keyword.replace("%20", " ")

        start_location = response.url.find("&rad=5&where=") + len("&rad=5&where=")
        end_location = response.url.find("&tm=7")
        location = response.url[start_location : end_location]
        location = location.replace("%20", " ")

        job_count = 0
        try:
            job_count = int(response.css('header.title h2.figure::text').get().replace("(", "").replace("Jobs Found)",""))
            item = JobCountItem()
            item['website'] = "Monster"
            item['keyword'] = keyword
            item['location'] = location
            item['count'] = job_count
            yield item
        except:
            logging.warning("Monster Failed")
            logging.warning(keyword + " " + location)
            logging.warning(response.css('header.title h2.figure::text').get())
            logging.warning(response.xpath('//body//p//text()').extract())

            item = JobCountItem()
            item['website'] = "Monster"
            item['keyword'] = keyword
            item['location'] = location
            item['count'] = 0
            yield item
                

           

class CareerBuilderSpider(scrapy.Spider):
    name = "careerbuilder_spider"

    def start_requests(self):
        urls = []

        for job_keyword in keywords:
            for job_location in locations:
                urls.append("https://www.careerbuilder.com/jobs?posted=7&radius=5&keywords="+ job_keyword +"&location="+ job_location)

        #creates a scrapy request for those pages
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        #Note to self, career builder does 404
        start_keyword = "https://www.careerbuilder.com/jobs?posted=7&radius=5&keywords="
        end_keyword = response.url.find("&location=")
        keyword = response.url[len(start_keyword) : end_keyword]
        keyword = keyword.replace("+", " ")
        keyword = keyword.replace("%20", " ")

        start_location = response.url.find("&location=") + len("&location=")
        location = response.url[start_location : len(response.url)]
        location = location.replace("+", " ")
        location = location.replace("%20", " ")

        job_count = 0

        if response.status == 404:
            item = JobCountItem()
            item['website'] = "CareerBuilder"
            item['keyword'] = keyword
            item['location'] = location
            item['count'] = job_count
            yield item
        else:
            try:
                job_count = int(response.css('[id="job-count"]::text').get().replace(" Jobs Found","").replace(",","").replace("More Than ",""))
                item = JobCountItem()
                item['website'] = "CareerBuilder"
                item['keyword'] = keyword
                item['location'] = location
                item['count'] = job_count
                yield item
            except:
                logging.warning("CareerBuilder Failed")
                logging.warning(keyword + " " + location)
                logging.warning(response.css('[id="job-count"]::text').get())
                logging.warning(response.xpath('//body//p//text()').extract())

                item = JobCountItem()
                item['website'] = "CareerBuilder"
                item['keyword'] = keyword
                item['location'] = location
                item['count'] = 0
                yield item

            

class SimplyHiredSpider(scrapy.Spider):
    name = "simplyhired_spider"

    def start_requests(self):
        urls = []

        for job_keyword in keywords:
            for job_location in locations:
                urls.append("https://www.simplyhired.com/search?q=" + job_keyword + "&l="+ job_location +"&mi=5&fdb=7")

        #creates a scrapy request for those pages
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        start_keyword = "https://www.simplyhired.com/search?q="
        end_keyword = response.url.find("&l=")
        keyword = response.url[len(start_keyword) : end_keyword]
        keyword = keyword.replace("+", " ")
        keyword = keyword.replace("%20", " ")

        start_location = response.url.find("&l=") + len("&l=")
        end_location = response.url.find("&mi=5&fdb=7")
        location = response.url[start_location : end_location]
        location = location.replace("+", " ")
        location = location.replace("%20", " ")

        job_count = 0
        if response.status == 404:
            item = JobCountItem()
            item['website'] = "SimplyHired"
            item['keyword'] = keyword
            item['location'] = location
            item['count'] = job_count
            yield item
        else:
            try:
                job_count = response.css('span.CategoryPath-total::text').get()
                job_count2 = response.css('span.posting-total::text').get()

                if job_count == None:
                    job_count = 0
                else:
                    job_count = job_count.replace(",", "")
                if job_count2 == None:
                    job_count2 = 0
                else:
                    job_count2 = job_count2.replace(",", "")

                job_count = int(job_count)
                job_count2 = int(job_count2)

                #prints the greater of two responses
                job_count = job_count if (job_count > job_count2) else job_count2

                item = JobCountItem()
                item['website'] = "SimplyHired"
                item['keyword'] = keyword
                item['location'] = location
                item['count'] = job_count
                yield item
        

            except:
                logging.warning(response.css('span.CategoryPath-total::text').get())
                logging.warning(response.css('span.posting-total::text').get())

           
#
# Manage Spider Proceses down here
#
start_time = time.time()

# 
# Gets Proxy List 
#
my_file = requests.get(url = "https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=US&ssl=no&anonymity=elite")
file_lines = [''.join(["http://",str(x), '\n']) for x in my_file.text.splitlines()]
f = open("http_proxies.txt", 'w')
f.writelines(file_lines) 
f.close()

#
# Load locations from csv
#

locations = pd.read_csv('city_population_data.csv')['city_state'].to_numpy()

#
# Load Keywords from csv
#

f = open("jobs_list.txt", "r")
for x in f:
    keywords.append(x)
#
# Run Scraping Jobs
#
runner = CrawlerRunner(get_project_settings())

configure_logging()

logging.getLogger('scrapy').setLevel(logging.INFO)

runner.crawl(MonsterSpider)
runner.crawl(SimplyHiredSpider)
runner.crawl(CareerBuilderSpider)
d = runner.join()
d.addBoth(lambda _: reactor.stop())
reactor.run()

print("#################")
print("Spiders Finished")
print("#################")

print(time.time() - start_time)

print("Keywords:" + str(len(keywords)))
print("Locations:" + str(len(locations)))

print("SimplyHired Query Count:" + str(sum(1 for line in open('simplyhired_spider.jl'))))
print("Monster Query Count:" + str(sum(1 for line in open('monster_spider.jl'))))
print("CareerBuilder Query Count:" + str(sum(1 for line in open('careerbuilder_spider.jl'))))

