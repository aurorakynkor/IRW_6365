import pandas as pd 

if __name__ == '__main__':
	data = pd.read_csv("us_all_location_data.csv")
	
	print(data.columns)

	top_x_cities = data.nlargest(600, 'population')
	
	top_x_cities['city_state'] = top_x_cities['city'] + ", " + top_x_cities['state_id']

	top_x_cities = top_x_cities[['city_state','population', 'lat', 'lng']]
	
	print(top_x_cities.to_string())

	top_x_cities.to_csv('city_population_lat_lng_data.csv')