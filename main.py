from fastapi import FastAPI, HTTPException

from metrics import *

app = FastAPI()

@app.get("/avg_tmp_per_city_per_day")
async def get_avg_temp():
    result = avg_temp()

    if "error" in result:
        raise HTTPException(status_code=404, detail="No connection to the database")

    return result

@app.get("/lower_humidity_point")
async def get_lowest_humidity():
    result = lowest_humidity()

    if "error" in result:
        raise HTTPException(status_code=404, detail="No connection to the database")

    return result

@app.get("/rank_cities_by_feels_like")
async def get_rank_cities():
    result = rank_cities()

    if "error" in result:
        raise HTTPException(status_code=404, detail="No connection to the database")

    return result

