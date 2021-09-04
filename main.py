from fastapi import FastAPI

from metrics import *

app = FastAPI()

@app.get("/avg_tmp_per_city_per_day")
async def get_avg_temp():
    return avg_temp()

@app.get("/lower_humidity_point")
async def get_lowest_humidity():
    return lowest_humidity()

@app.get("/rank_cities_by_feels_like")
async def get_rank_cities():
    return rank_cities()

