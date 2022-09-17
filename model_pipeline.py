import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity # Importing cosine_similarity
import mlflow
import mlflow.sklearn

if __name__ == "__main__":
    ### Initializing MLflow
    mlflow.set_experiment(experiment_name="Movie_Recommender")
    ##import data
    data = pd.read_csv('data/final_data.csv')
    print('Data loaded sucessully')
    cv = CountVectorizer(stop_words="english",max_features=5000)
    vector = cv.fit_transform(data['tags'][:1000]).toarray()
    print(vector[0])
    cosine_similarity(vector).shape
    similarity = cosine_similarity(vector)
    sorted(list(enumerate(similarity[0])),reverse =True , key = lambda x:x[1])[1:6]
    print(similarity)
    print('Model sucessfully built!!!')
    mlflow.sklearn.log_model(similarity, 'model')
