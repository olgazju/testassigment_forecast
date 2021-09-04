# Test Assigment Weather Rest API

## Architecture

**1st Docker:** postgressql db 

BeeHeroTask database:
- table forecastapp_cities (city_id(pk), city_name, country, lat, lon)
- table forecastapp_forecast (id(pk), f_dt, temp, feels_like, humidity, city_id(fk=forecastapp_cities.city_id))

**2nd Docker:** web app with 3 endpoints (with help of FastAPI, pandas, sqlalchemy)

**populate_db.py** script which populates postgressql db (5 Day / 3 Hour Forecast API was used - https://openweathermap.org/forecast5)

## Getting started

1. Install Docker Desktop

2. Run in root folder 

`docker-compose up -d --build`

3. Check if containers are running

`docker ps`

4. Populate database from Weather API

From root folder:

`python3 -m venv env`

`source env/bin/activate`

`pip3 install -r requirements.txt`

`python3 python3 populate_db.py`

You should see the next message: PostgreSQL Tables has been populated successfully.

5. Calculations

- Average temp for each city for each day.

http://0.0.0.0:8000/avg_tmp_per_city_per_day

Example: "[{\"city_name\":\"Eilat\",\"date\":\"2021-09-04T00:00:00.000Z\",\"avg_temp\":32.53},{\"city_name\":\"Eilat\",\"date\":\"2021-09-05T00:00:00.000Z\",\"avg_temp\":31.76},{\"city_name\":\"Eilat\",\"date\":\"2021-09-06T00:00:00.000Z\",\"avg_temp\":30.53} ...

- Lowest humidity point (place + time).

http://0.0.0.0:8000/lower_humidity_point

Example: "[{\"city_name\":\"Eilat\",\"f_dt\":\"2021-09-09T12:00:00.000Z\",\"humidity\":18.0}]"

- Rank the cities by their last (most recent) “feels_like” value (order
    should be low to high).

http://0.0.0.0:8000/rank_cities_by_feels_like

Example: "[{\"rank\":1,\"city_name\":\"Jerusalem\",\"feels_like\":21.12},{\"rank\":2,\"city_name\":\"Haifa\",\"feels_like\":26.29},{\"rank\":3,\"city_name\":\"Tiberias\",\"feels_like\":26.43},{\"rank\":4,\"city_name\":\"Tel Aviv District\",\"feels_like\":28.53},{\"rank\":5,\"city_name\":\"Eilat\",\"feels_like\":30.06}]"

6. What I would add:

- Save password to DB and Weather API token into Google Cloud’s Secret Manager

- Add Airflow instance in docker and make populate_db.py as scheduled task inside Airflow DAG (also email on failing)

- Add ingested_time to both tables and support of primary keys for adding new cities into scheduled task inside Airflow DAG

- Add tests

