import requests
from bs4 import BeautifulSoup

def get_monster_jobs (job_keyword, job_location):
    """This function takes a web url, and scrapes jobs from a url and gets
    all jobs posted within the last week

    Parameters:
    job_keyword: String
    job_location: String

    Returns:
    job_count: list we can return to our db query, the only info we need is the raw number of jobs
    """

    url = "https://www.monster.com/jobs/search/?q="+ job_keyword +"&where="+ job_location +"&intcid=skr_navigation_nhpso_searchMain"
    page = requests.get(url)
    #print(page.status_code)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find("header", class_= "title")
    job_count = results.text
    
    #format data
    start = job_count.find('(')
    end = job_count.find(' Jobs Found')
    job_count = job_count[start + 1:end]

    return job_count

if __name__ == '__main__':
    keywords = ["Software", "Waiter", "Retail", "Barista", "Civil Engineering", "Chemical Engineering"]
    locations = ["Atlanta", "Tampa", "New York", "Los Angeles", "Portland", "San Jose"]

    job_data = []

    for keyword in keywords:
        print()
        print(keyword)
        for location in locations:
            job_count = get_monster_jobs(keyword, location)
            print(location + " : " + job_count)
            job_data.append(keyword + location + get_monster_jobs(keyword, location))