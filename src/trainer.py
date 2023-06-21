import pandas as pd
import logging
import warnings
import os
from datetime import date
import time
from dotenv import load_dotenv
from minio import Minio
from datetime import date, timedelta
import pickle
import io
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity 
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

def read_data(minio_client, bucket, path):
    """Read JSON from Minio as a pandas DataFrame"""
    obj = minio_client.get_object(bucket, path)
    return pd.read_json(obj)

def wait_until(minio_client, bucket, path, timeout, period=10):
    """Wait until ETL extracts data to pull it"""
    must_end = time.time() + timeout
    while time.time() < must_end:
        list_objects = minio_client.list_objects(bucket, recursive=True)
        list_items = [item.object_name for item in list_objects]
        if path in list_items:
            return True
        time.sleep(period)
        logging.info("Waiting for ETL to finish ...")
    
    logging.error("Timeout occurred. ETL did not complete within the specified timeout period.")
    return False


def main():
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
    data_path = f"recom_data/{day}-{month}-{year}/data.json"
    if wait_until(minio_client, bucket, data_path, 300, period=10):
        logging.info("Reading user data from Minio ...")
        data = read_data(minio_client, bucket, data_path)
        logging.info("Reading data from Minio ...")
    logging.info('Data loaded sucessully')
    cv = CountVectorizer(stop_words="english",max_features=5000)
    vector = cv.fit_transform(data['tags'][:1000]).toarray()
    cosine_similarity(vector).shape
    similarity = cosine_similarity(vector)
    sorted(list(enumerate(similarity[0])),reverse =True , key = lambda x:x[1])[1:6]
    logging.info('Model sucessfully built!!!')
    logging.info("Saving model Artifacts ...")
    bytes_file = pickle.dumps(similarity)
    minio_client.put_object(
        bucket_name=bucket,
        object_name=f"artifacts/{day}-{month}-{year}/similarity.pkl",
        data=io.BytesIO(bytes_file),
        length=len(bytes_file)
    )

    bytes_file = pickle.dumps(data)
    minio_client.put_object(
        bucket_name=bucket,
        object_name=f"artifacts/{day}-{month}-{year}/data_.pkl",
        data=io.BytesIO(bytes_file),
        length=len(bytes_file)
    )

    elapsed_time_secs = timedelta(seconds=round(time.time() - start_time))
    logging.info(
        "training took: %s secs (Wall clock time)", elapsed_time_secs
    )

if __name__ == "__main__":
    main()
