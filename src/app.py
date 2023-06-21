from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
import uvicorn
import pandas as pd
import pickle
import os
from datetime import date, timedelta
import time
from dotenv import load_dotenv
from minio import Minio
import warnings
import logging

warnings.filterwarnings("ignore")

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s: [%(levelname)s]: %(message)s"
)

app = FastAPI(title="Movie Recommender System")


load_dotenv()
minio_client = None
BUCKET = os.getenv("S3_BUCKET")
minio_client = Minio(
            "minio:9000",
            os.getenv("S3_ACCESS_KEY"),
            os.getenv("S3_SECRET_KEY"),
            secure=False,
        )

def parse_date():
    """Parse current day, month, and year"""
    today = date.today()
    return today.day, today.month, today.year


@app.on_event("startup")
@repeat_every(seconds=60)
async def startup_event():
    """load data on startup"""
    global data, similarity
    day, month, year = parse_date()
    data_path = f'artifacts/{day}-{month}-{year}/data_.pkl'
    sim_path = f'artifacts/{day}-{month}-{year}/similarity.pkl'
    data_ = minio_client.get_object(BUCKET, data_path)
    sim = minio_client.get_object(BUCKET, sim_path)
    logging.info("loading data from Minio : %s")
    data = pickle.load(data_)
    similarity = pickle.load(sim)


@app.get('/predict')
def get_top_similar_items(movie:str):
    '''
	You can use the following as an example\n
    - Built by Olawale Abimbola
	- Titan A.E.\n
	- Ender's Game\n
	- Independence Day\n
	- Battle: Los Angeles\n
	- Edge of Tomorrow\n
	- The Lovers\n
	- Jupiter Ascending\n
	- Star Trek Into Darkness\n
	- The Fifth Element\n
	- Avatar
    '''
    movie_index = data[data['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate( distances)),reverse =True , key = lambda x:x[1])[1:10]
    recom = []
    for i in movie_list:
        rec = data.iloc[i[0]].title
        recom.append(rec)
    return recom


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', debug=True)