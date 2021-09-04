import os
import psycopg2
import pandas as pds
from sqlalchemy import create_engine


QUERIES = {'avg_temp': '''SELECT 
                            city_name, 
                            date(f_dt), 
                            ROUND(CAST(AVG(temp) AS numeric), 2) as avg_temp
                        FROM \"forecastapp_forecast\" as forecast 
                        join \"forecastapp_cities\" as cities 
                            on 
                            forecast.city_id=cities.city_id 
                        group by city_name, date(f_dt)
                        order by city_name, date(f_dt)''',

            'lowest_humidity': '''SELECT city_name, f_dt, humidity
                                 FROM
                                 (
                                     SELECT ROW_NUMBER() OVER (ORDER BY humidity) as RowNum, *
                                     FROM \"forecastapp_forecast\"  
                                 ) as forecast 
                                 join \"forecastapp_cities\" as cities 
                                    on forecast.city_id=cities.city_id
                                 WHERE RowNum = 1
                                  ''',

            'rank_cities': ''' SELECT city_name, feels_like
                                 FROM
                                 (
                                     SELECT ROW_NUMBER() OVER (PARTITION BY city_id ORDER BY f_dt DESC) as RowNum, *
                                     FROM \"forecastapp_forecast\"
                                 ) as forecast 
                                 join \"forecastapp_cities\" as cities 
                                    on forecast.city_id=cities.city_id
                                 WHERE RowNum = 1 order by feels_like'''
          }



alchemyEngine = create_engine('postgresql+psycopg2://{}:{}@{}/{}'.format(os.environ.get('DB_USER', 'postgres'),
                                                                                         os.environ.get('DB_PASSWORD', 'pa55w0rd'), 
                                                                                        os.environ.get('DB_HOST', 'db'),
                                                                                         os.environ.get('DB_NAME', 'BeeHeroTask')), pool_recycle=3600);


def run_query_in_pandas(query: str):

    dbConnection = alchemyEngine.connect()

    try:

        result = pds.read_sql(query, 
                            dbConnection)

        print(result)
        return result.to_json(orient='records', date_format='iso')
    except Exception as ex:  
        print(ex)
        return {}
    else:
        print("All metrics were calculated successfully.")

    finally:
        dbConnection.close()


def avg_temp():
    '''
    Average temp for each city for each day.
    '''
    return run_query_in_pandas(QUERIES['avg_temp'])

def lowest_humidity():
    '''
    Lowest humidity point (place + time).
    '''
    return run_query_in_pandas(QUERIES['lowest_humidity'])

def rank_cities():
    '''
    Rank the cities by their last (most recent) “feels_like” value (order
    should be low to high).
    '''
    return run_query_in_pandas(QUERIES['rank_cities'])
