import requests
from bs4 import BeautifulSoup

def get_careerbuilder_jobs (job_keyword, job_location):
    """This function takes a web url, and scrapes jobs from a url and gets
    all jobs posted within the last week

    Parameters:
    job_keyword: String
    job_location: String

    Returns:
    job_count: list we can return to our db query, the only info we need is the raw number of jobs
    """
    #https://www.careerbuilder.com/jobs?posted=7&pay=&cat1=&radius=30&emp=&cb_apply=false&cb_workhome=false&keywords=Software&location=Atlanta
    url = "https://www.careerbuilder.com/jobs?posted=30&radius=30&keywords="+ job_keyword +"&location="+ job_location
    page = requests.get(url)
    #print(page.status_code)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id = "job-count")
    job_count = results.text
    
    #format data
    job_count = job_count.replace("More Than ","")
    start = -1
    end = job_count.find(' Jobs Found')
    job_count = job_count[start + 1:end]
    job_count = job_count.replace(",","")

    return job_count

if __name__ == '__main__':
    keywords = ["Software", "Waiter", "Retail", "Barista", "Civil Engineering", "Chemical Engineering"]
    locations = ["Atlanta", "Tampa", "New York City", "Los Angeles", "Portland", "San Jose"]

    job_data = []

    for keyword in keywords:
        print()
        print(keyword)
        for location in locations:
            job_count = get_careerbuilder_jobs(keyword, location)
            print(location + " : " + job_count)
            job_data.append(keyword + location + get_careerbuilder_jobs(keyword, location))