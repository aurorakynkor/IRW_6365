Setup Instructions:

Install Wamp 3.2.0 
I downloaded wamp a month ago from http://www.wampserver.com/en/ (currently the website is down for some reason)
https://sourceforge.net/projects/wampserver/
Under the select components tab, check off MySQL8.0.18
Click through and install
Download Github Repo from https://github.com/aurorakynkor/IRW_6365
Download Python 3.7.4
https://www.python.org/downloads/release/python-374/
Doublecheck by running python --version
Install Python Packages
Install pip
python -m pip install --upgrade pip
Python -m pip install plotly
Python -m pip install mysql-connector-python.py
Python -m pip install pandas
Python -m pip install scrapy
Python -m pip install requests
Python -m pip install scrapy-proxies
Python -m pip install scrapy_random_useragent_pro
Python -m pip install scrapy_fake_useragent
Setup DB
Run Wamp
Go to your toolbar tray and right click the green wamp icon
Search for an option called “Invert Default DBMS MariaDB <-> Mysql” and click it
Click on green wamp icon again and click phpmyadmin
Login
User: root
Password: 
Server choice: MySQL
Create DB
On left hand side click new
At the top you should see an option to create Database
Under Database Name type “jobdb”
Make sure the other dropdown says utf8mb4_0900_ai_ci
Click Create
On left hand side click jobdb 
At the top find the option to IMPORT
You should see an option to import a file by browsing your computer
Find the jobdb.sql file in IRW_6365 and select that file
Don’t change anything else and select Go
The tables we’ve collected should appear on the left!

File Structure:

location_data
    city_population_lat_lng_data.csv
    #generates city_population_lat_lng_data.csv from us_all_location_data.csv
    location_data.py
    us_all_location_data.csv
scrapy_scrapers
    Spiders
        #Each of the Scrapers and Runner exist in spiders.py
        spiders.py
    city_population_data.csv
    #job item code
    items.py
    #the list of job keywords used in this project
    #middlewares used in this project
    middlewares.py
    #pipeline for job items to go to SQL DB
    pipelines.py
    #Scrapy specific settings and DB connection
    settings.py
#Run to see map, details below
job_map.py
#database code and data from our scrapes
jobdb.sql
#the list of job keywords we created
jobs_list.txt
scrapy.cfg

Key Executables:

Job_map.py:

Go to Terminal/Command Prompt
CD to IRW_6365 directory
Run “python job_map.py -s <start_date: YYYY_MM_DD> -e <end_date: YYYY_MM_DD> -k <keyword from jobs_ist.txt> -w <careerbuilder, simplyhired, monster, aggregate (for all 3)>
Job map should show up in your web browser!

Crawler (the program that fetches data from IRW’s):

Go to Terminal/Command Prompt
CD to IRW_6365/scrapy_scrapers
Type “Scrapy Crawl”
Scraper should be running!
Wait 13-15 hours for scraping to finish!

Optional Files:

location_data.py

Go to Terminal/Command Prompt
CD to IRW_6365/location_data
Type “python location_data.py”
city_population_lat_lng_data.csv will appear!
