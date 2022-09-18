import pickle 
import pandas as pd
data = pd.read_csv('data/final_data.csv')

with open('mlruns/1/9d8cb8220262429fbc9bf0b548a4454a/artifacts/model/model.pkl', 'rb') as f:
    similarity = pickle.load(f)


def recommend(movie):
    movie_index = data[data['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate( distances)),reverse =True , key = lambda x:x[1])[1:10]

    for i in movie_list:
        print(data.iloc[i[0]].title)