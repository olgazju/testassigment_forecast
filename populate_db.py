import requests
from datetime import datetime
from sqlalchemy import create_engine
import psycopg2
import pandas as pd


API_KEY = "30097314c03d379548cdbfb826584314"
LIMIT = '1'
ISO_CODE = "IL"
CITIES = ("Jerusalem", "Haifa", "Tel Aviv", "Eilat", "Tiberias")

# Geocoding API
# https://openweathermap.org/api/geocoding-api

geodata = []

city_id = 0 # get last id from database
for city in CITIES:
    payload = {'q': "{}, {}".format(city, ISO_CODE), 'limit': LIMIT, 'appid': API_KEY}
    r = requests.get('http://api.openweathermap.org/geo/1.0/direct', params=payload)


    result = r.json()

    # set try here
    geodata.append({'country': result[0]["country"],
                    'city_name': result[0]['name'],
                    'lat': result[0]['lat'],
                    'lon': result[0]['lon'],
                    'city_id': city_id})

    city_id += 1

print(geodata)

# Forecast API
# https://openweathermap.org/forecast5#geo5

weather_data = []
for city in geodata:
    payload = {'lat': city["lat"], 'lon': city["lon"], 'units': 'metric', 'appid': API_KEY}
    r = requests.get('http://api.openweathermap.org/data/2.5/forecast', params=payload)

    for forecast in r.json()['list']:
        weather_data.append({'f_dt': datetime.strptime(forecast["dt_txt"], '%Y-%m-%d %H:%M:%S'),
                'temp': forecast["main"]["temp"],
                'feels_like': forecast["main"]["feels_like"],
                'humidity': forecast["main"]["humidity"],
                'city_id': city["city_id"]})


cities_df = pd.DataFrame(geodata)
forecast_df = pd.DataFrame(weather_data)
        

# save both tables
alchemyEngine = create_engine('postgresql+psycopg2://postgres:1@127.0.0.1/BeeHeroTask', pool_recycle=3600);
postgreSQLConnection = alchemyEngine.connect();
cities_table = "forecastapp_cities";
forecast_table = "forecastapp_forecast"

try:
    cities_df.to_sql(cities_table, postgreSQLConnection, index=False, if_exists='append')
    frame = forecast_df.to_sql(forecast_table, postgreSQLConnection, index=False, if_exists="append")

except ValueError as vx:
    print(vx)

except Exception as ex:  
    print(ex)

else:
    print("PostgreSQL Tables has been populated successfully.")
finally:
    postgreSQLConnection.close();


