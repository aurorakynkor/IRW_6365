from __future__ import absolute_import
import scrapy
import logging
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer
from scrapy.utils.log import configure_logging
from scrapy_scrapers.items import JobCountItem

#
# Get Keywords and Locations from text file or DB up here and set them up so all spiders can see them
#

#keywords = ["Software", "Waiter", "Retail", "Barista", "Civil Engineering", "Chemical Engineering"]
#locations = ["Atlanta", "Tampa", "New York City", "Los Angeles", "Portland", "San Jose"]

keywords = ["Software"]
locations = ["Atlanta"]

#
# Define Spiders Here
#
class MonsterSpider(scrapy.Spider):
    name = "monster_spider"

    def start_requests(self):
        urls = []

        for job_keyword in keywords:
            for job_location in locations:
                urls.append("https://www.monster.com/jobs/search/?q="+ job_keyword +"&where="+ job_location +"&intcid=skr_navigation_nhpso_searchMain")

        #creates a scrapy request for those pages
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        start_keyword = "https://www.monster.com/jobs/search/?q="
        end_keyword = response.url.find("&where=")
        keyword = response.url[len(start_keyword) : end_keyword]
        keyword = keyword.replace("%20", " ")

        start_location = response.url.find("&where=") + len("&where=")
        end_location = response.url.find("&intcid=skr_navigation_nhpso_searchMain")
        location = response.url[start_location : end_location]
        location = location.replace("%20", " ")

        job_count = int(response.css('header.title h2.figure::text').get().replace("(", "").replace("Jobs Found)",""))

        item = JobCountItem()
        item['website'] = "Monster"
        item['keyword'] = keyword
        item['location'] = location
        item['count'] = job_count

        self.log(keyword)
        self.log(location)
        self.log(job_count)

        return item

class CareerBuilderSpider(scrapy.Spider):
    name = "careerbuilder_spider"

    def start_requests(self):
        urls = []

        for job_keyword in keywords:
            for job_location in locations:
                urls.append("https://www.careerbuilder.com/jobs?posted=30&radius=30&keywords="+ job_keyword +"&location="+ job_location)

        #creates a scrapy request for those pages
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        start_keyword = "https://www.careerbuilder.com/jobs?posted=30&radius=30&keywords="
        end_keyword = response.url.find("&location=")
        keyword = response.url[len(start_keyword) : end_keyword]
        keyword = keyword.replace("+", " ")
        keyword = keyword.replace("%20", " ")

        start_location = response.url.find("&location=") + len("&location=")
        location = response.url[start_location : len(response.url)]
        location = location.replace("+", " ")
        location = location.replace("%20", " ")

        job_count = int(response.css('[id="job-count"]::text').get().replace(" Jobs Found","").replace(",","").replace("More Than ",""))

        item = JobCountItem()
        item['website'] = "CareerBuilder"
        item['keyword'] = keyword
        item['location'] = location
        item['count'] = job_count

        self.log(keyword)
        self.log(location)
        self.log(job_count)

        return item
class SimplyHiredSpider(scrapy.Spider):
    name = "simplyhired_spider"

    def start_requests(self):
        urls = []

        for job_keyword in keywords:
            for job_location in locations:
                urls.append("https://www.simplyhired.com/search?q=" + job_keyword + "&l="+ job_location +"&fdb=7&job=9r--0qwC3hOxlMuL9mPRwZ2fsE31-_bow90r8xPM1jWTKS85ac6LGg")

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
        end_location = response.url.find("&fdb=7&job=9r")
        location = response.url[start_location : end_location]
        location = location.replace("+", " ")
        location = location.replace("%20", " ")

        job_count = int(response.css('span.posting-total::text').get().replace(",", ""))

        item = JobCountItem()
        item['website'] = "SimplyHired"
        item['keyword'] = keyword
        item['location'] = location
        item['count'] = job_count

        self.log(keyword)
        self.log(location)
        self.log(job_count)

        return item

#
# Manage Spider Proceses down here
#

runner = CrawlerRunner(get_project_settings())

configure_logging()
runner = CrawlerRunner()

@defer.inlineCallbacks
def crawl():
    yield runner.crawl(MonsterSpider)
    yield runner.crawl(SimplyHiredSpider)
    yield runner.crawl(CareerBuilderSpider)
    reactor.stop()

crawl()
reactor.run()

print("#################")
print("Spiders Finished")
print("#################")
