## Import Libraries 
import pandas as pd
import ast 
import logging
import warnings
import os
from datetime import date
import time
from dotenv import load_dotenv
from minio import Minio
from datetime import date, timedelta
from io import BytesIO
import io

warnings.filterwarnings("ignore")

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s: [%(levelname)s]: %(message)s"
)


def read_minio_env():
    """Read Minio environment variables"""
    logging.info("Reading environment variables to connect to Minio ...")
    load_dotenv()
    return (
        os.getenv("S3_BUCKET"),
        os.getenv("S3_ACCESS_KEY"),
        os.getenv("S3_SECRET_KEY"),
        os.getenv("S3_URL")
    )

def parse_date():
    """Parse current day, month, and year"""
    today = date.today()
    return today.day, today.month, today.year

def minio_to_pandas(minio_client, bucket, path):
    """Read JSON from Minio as a pandas DataFrame"""
    obj = minio_client.get_object(bucket, path)
    return pd.read_json(obj)

def import_data():
    '''Import Dataset'''
    logging.info('Loading main dataset! ...')
    credit = pd.read_csv('credits.csv')
    movies = pd.read_csv('movies.csv')
    logging.info('Data Loaded Sucessfully!! ...')
    return credit, movies


def merge_df(credit, movies): 
    '''
    merge the credit and movie dataset based on the title
    '''
    logging.info('Merging the base dataset')
    df_movies = movies.merge(credit, on="title")
    logging.info(f'Credit shape {credit.shape} ...')
    logging.info(f'Movie shape {movies.shape} ...')
    logging.info(f'Merged shape {df_movies.shape} ...')
    return df_movies

def feature_selection(df):
    logging.info('selecting important columns ...')
    df_movies = df[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
    logging.info('drop missing nan ...')
    df_movies.dropna(inplace=True)
    df_movies.isnull().sum()
    return df_movies


def convert(obj):
    '''This function is meant to clean KEYWORDS
     AND GENRES columns'''
    temp = []
    for i in ast.literal_eval(obj):
        temp.append(i['name'].replace(" ", "").lower())
    return temp



def convertCast(obj):
    '''This function is meant to clean CAST columns'''
    temp = []
    count = 0
    for i in ast.literal_eval(obj):
        if count < 4:
            temp.append(i['name'].replace(" ", "").lower())
        count += 1
    return temp


def get_director(obj):
    '''This function is meant to clean CREW columns'''
    temp = []
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            temp.append(i['name'].replace(" ", "").lower())
            break
    return temp


def deep_cleaning(df_movies):
    logging.info('Deep cleaning!!!')
    df_movies['tags'] = df_movies['overview'] + df_movies['genres'] + df_movies['keywords'] + df_movies['cast'] + df_movies['crew']
    final_df = df_movies[['movie_id','title','tags']]
    final_df['tags'] = final_df['tags'].apply(lambda x :" ".join(x))
    final_df['tags'] = final_df['tags'].apply(lambda x :x.replace(",",""))
    logging.info('Data Cleaned Successfully!!!')
    return final_df

def main():
    '''main function'''
    load_dotenv()
    start_time = time.time()
    minio_client = None
    bucket = os.getenv("S3_BUCKET")
    minio_client = Minio(
            "minio:9000",
            os.getenv("S3_ACCESS_KEY"),
            os.getenv("S3_SECRET_KEY"),
            secure=False,
        )
    day, month, year = parse_date()
    credit, movies = import_data()
    df_movies = merge_df(credit, movies)
    logging.info('Cleaning Features ...')
    df_movies['genres'] = df_movies['genres'].apply(convert)
    logging.info('Cleaning Features ...')
    df_movies['keywords'] = df_movies['keywords'].apply(convert)
    logging.info('Cleaning cast ...')
    df_movies['cast'] = df_movies['cast'].apply(convertCast)
    logging.info('Cleaning CREW ...')
    df_movies['crew'] = df_movies['crew'].apply(get_director)
    df_movies['overview'] = df_movies['overview'].astype(str).apply(lambda x: x.split())
    final_df = deep_cleaning(df_movies)
    logging.info("Saving recommendations to Minio ...")
    bytes_file = final_df.to_json(
        orient="records", indent=4).encode()
    minio_client.put_object(
        bucket_name=bucket,
        object_name=f"recom_data/{day}-{month}-{year}/data.json",
        data=BytesIO(bytes_file),
        length=len(bytes_file),
    )

    logging.info(
        "ETL saved to :  recom_data/%s-%s-%s/...",
        day,
        month,
        year,
    )

    elapsed_time_secs = timedelta(seconds=round(time.time() - start_time))
    logging.info(
        "ETL took: %s secs (Wall clock time)", elapsed_time_secs
    )

if __name__ == '__main__':
    main()