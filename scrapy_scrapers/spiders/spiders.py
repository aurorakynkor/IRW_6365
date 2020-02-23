import scrapy
import logging
from scrapy.crawler import CrawlerProcess


#
# Get Keywords and Locations from text file or DB up here and set them up so all spiders can see them
#

keywords = ["Software", "Waiter", "Retail", "Barista", "Civil Engineering", "Chemical Engineering"]
locations = ["Atlanta", "Tampa", "New York City", "Los Angeles", "Portland", "San Jose"]

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

        self.log(keyword)
        self.log(location)
        self.log(job_count)

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

        self.log(keyword)
        self.log(location)
        self.log(job_count)


#
# Manage Spider Proceses down here
#

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(MonsterSpider)
process.crawl(CareerBuilderSpider)
process.start()