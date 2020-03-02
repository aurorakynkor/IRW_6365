from __future__ import absolute_import
import scrapy
import logging
import time
import requests
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer
from scrapy.utils.log import configure_logging
from scrapy_scrapers.items import JobCountItem

#
# Get Keywords and Locations from text file or DB up here and set them up so all spiders can see them
#

keywords = ["Software", "Server", "Retail", "Barista", "Civil Engineering", "Chemical Engineering", "Nurse", "Doctor", "Construction", "Lawyer", "Janitor", "Teacher", "Security Guard", "Electrician", "Bartender", "Dentist", "Accountant"]
locations = ["Atlanta", "Tampa", "New York City", "Los Angeles", "Portland", "San Jose", "Las Vegas", "San Francisco", "New Orleans", "Boston", "Chicago", "Houston", "Phoenix", "San Antonio", "San Diego", "Austin", "Jacksonville", "Fort Worth", "Columbus", "Charlotte", "Denver", "Detroit", "Miami"]

#keywords = ["Software"]
#locations = ["Atlanta"]

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
        except:
            logging.debug(response.css('header.title h2.figure::text').get())

        item = JobCountItem()
        item['website'] = "Monster"
        item['keyword'] = keyword
        item['location'] = location
        item['count'] = job_count
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
        try:
            job_count = int(response.css('[id="job-count"]::text').get().replace(" Jobs Found","").replace(",","").replace("More Than ",""))
        except:
            logging.debug(response.css('[id="job-count"]::text').get())

        item = JobCountItem()
        item['website'] = "CareerBuilder"
        item['keyword'] = keyword
        item['location'] = location
        item['count'] = job_count
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
        try:
            job_count = int(response.css('span.posting-total::text').get().replace(",", ""))
        except:
            logging.debug(response.css('span.posting-total::text').get())

        item = JobCountItem()
        item['website'] = "SimplyHired"
        item['keyword'] = keyword
        item['location'] = location
        item['count'] = job_count
        yield item
        
#
# Manage Spider Proceses down here
#
start_time = time.time()

# 
# Gets Proxy List 
#
my_file = requests.get(url = "https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=US&ssl=no&anonymity=elite")
print(my_file.text)
file_lines = [''.join(["http://",str(x), '\n']) for x in my_file.text.splitlines()]
f = open("http_proxies.txt", 'w')
f.writelines(file_lines) 
f.close()

#
# Run Scraping Jobs
#

print(len(keywords))
print(len(locations))

runner = CrawlerRunner(get_project_settings())

configure_logging()

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

logging.debug(len(keywords))
logging.debug(len(locations))