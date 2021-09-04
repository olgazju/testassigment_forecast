# Test Assigment Weather Rest API


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

- Lowest humidity point (place + time).

http://0.0.0.0:8000/lower_humidity_point

- Rank the cities by their last (most recent) “feels_like” value (order
    should be low to high).

http://0.0.0.0:8000/rank_cities_by_feels_like
