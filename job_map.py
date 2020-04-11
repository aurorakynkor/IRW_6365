import plotly.graph_objects as go
import mysql.connector
import pandas as pd
import sys, getopt
import datetime
from scrapy.utils.project import get_project_settings


def main(argv):
    # Options:
    # 4 Data set Options, careerbuilder, simplyhired, monster, aggregate of all 3
    # start_date, end_date
    # Keyword Options
    start_date = ""
    end_date = ""
    keyword = ""
    website = ""
    keywords = []
    f = open("jobs_list.txt", "r")
    for x in f:
        keywords.append(x.rstrip())

    try:
        opts, args = getopt.getopt(argv,"hs:e:k:w:",["start_date=","end_date=", "keyword=", "website="])
    except getopt.GetoptError:
        print('job_map.py -s <start_date> -e <end_date> -k <keyword> -w <website>')
        print('start_date and end_date must be formated "YYYY_MM_DD" with _s')
        print('keyword must be one of these: ')
        print(keywords)
        print('website must be careerbuilder, monster, simplyhired or aggregate (for combination of all 3)')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('job_map.py -s <start_date> -e <end_date> -k <keyword> -w <website>')
            print('start_date and end_date must be formated "YYYY_MM_DD" with _s')
            print('keyword must be one of these: ')
            print(keywords)
            print('website must be careerbuilder, monster, simplyhired or aggregate (for combination of all 3)')
            sys.exit()
        elif opt in ("-s", "--start_date"):
            arg = arg.split("_")
            arg = datetime.date(int(arg[0]), int(arg[1]), int(arg[2]))
            start_date = arg
        elif opt in ("-e", "--end_date"):
            arg = arg.split("_")
            arg = datetime.date(int(arg[0]), int(arg[1]), int(arg[2]))
            end_date = arg
        elif opt in ("-k", "--keyword"):
            keyword = arg
        elif opt in ("-w", "--website"):
            website = arg

    return [start_date, end_date, keyword, website]

if __name__ == "__main__":
    args_list = main(sys.argv[1:])
    start_date = args_list[0]
    end_date = args_list[1]
    keyword = args_list[2]
    website = args_list[3]

    ##################################
    # Get names of all Tables in jobdb
    ##################################

    db_settings = get_project_settings().getdict("DB_SETTINGS")
    if not db_settings: # if we don't define db config in settings
        raise NotConfigured # then reaise error

    db = db_settings['db']
    user = db_settings['user']
    passwd = db_settings['passwd']
    host = db_settings['host']

    conn = mysql.connector.connect(db="information_schema", user=user, passwd=passwd, host=host, charset='utf8', use_unicode=True)
    cursor = conn.cursor()
    sql = "SELECT table_name FROM information_schema.tables WHERE table_schema ='"+ db +"';"
    cursor.execute(sql)
    
    myresult = cursor.fetchall()

    table_name_list = []
    for x in myresult:

        table_name_list.append(x)

    conn.commit()

    ###########################
    # Get Relevant Table Names
    ###########################
    query_table_names = []

    for table_name in table_name_list:
        table_name = table_name[0]
        split = table_name.split("_")
        table_website = split[0]
        table_year = int(split[1])
        table_month = int(split[2])
        table_day = int(split[3])
        table_date = datetime.date(table_year, table_month, table_day)

        if website == "aggregate":
            names = ["careerbuilder", "simplyhired", "monster"]
            if table_website in names and start_date <= table_date <= end_date:
                query_table_names.append(table_name)
        else:
            if table_website == website and start_date <= table_date <= end_date:
                query_table_names.append(table_name)

    ###########################
    # Query Tables and store in Df
    ###########################
    df = pd.DataFrame(columns = ['keyword', 'city', 'count'])

    for table_name in query_table_names:
        conn = mysql.connector.connect(db=db, user=user, passwd=passwd, host=host, charset='utf8', use_unicode=True)
        cursor = conn.cursor()

        sql = "SELECT * FROM "+ db +"." + table_name + " WHERE keyword = '" + keyword + "';"
        cursor.execute(sql)
        
        myresult = cursor.fetchall()

        results_list = []

        for x in myresult:
            results_list.append(x)

        conn.commit()

        appenddf = pd.DataFrame(columns = ['keyword', 'city', 'count'], data=results_list)
        df = df.append(appenddf)
    
    df = df.groupby(['keyword','city'], as_index=False)['count'].sum()

    location_data = pd.read_csv("location_data/city_population_lat_lng_data.csv").reset_index()

    df = df.set_index('city').join(location_data.set_index('city_state')).reset_index()
    df = df.rename(columns={"level_0": "city_state"})

    df = df.fillna(0)

    df['text'] = df['city'] + "<br>Total " + keyword + " Jobs: " + df['count'].astype(str)

    mean = df['count'].mean()

    ###########################
    # Create Map
    ###########################

    
    limits = [(0,mean/2),(mean/2,mean),(mean, mean * 2),(mean * 2, mean * 4),(mean * 4, 100000)]
    colors = ["darkblue","lightblue","yellow","orange","red"]
    cities = []
    scale = 6000

    title = "U.S. " + keyword + " Jobs from " + start_date.strftime("%b %d %Y ") + " to " + end_date.strftime("%b %d %Y ") + " based on " + website

    fig = go.Figure()

    for i in range(len(limits)):
        lim = limits[i]
        df_sub = df[(df['count'] >= lim[0]) & (df['count'] < lim[1])]
        fig.add_trace(go.Scattergeo(
            locationmode = 'USA-states',
            lon = df_sub['lng'],
            lat = df_sub['lat'],
            text = df_sub['text'],
            marker = dict(
                size = df_sub['population'] / scale,
                color = colors[i],
                line_color='rgb(40,40,40)',
                line_width=0.5,
                sizemode = 'area'
            ),
            name = '{0} - {1}'.format(lim[0],lim[1])))

    fig.update_layout(
            title_text = title +'<br>(Click legend to toggle traces)',
            showlegend = True,
            geo = dict(
                scope = 'usa',
                landcolor = 'rgb(217, 217, 217)',
            )
        )

    fig.show()