import scrapy
import logging

class MonsterSpider(scrapy.Spider):
    name = "monster_spider"

    def start_requests(self, *args, **kwargs):
        urls = []   
        keywords = ["Software","Barista", "Chemical Engineer"]
        locations = ["Atlanta", "New York", "Los Angeles"]
        #Generates all keyword/location pairs
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