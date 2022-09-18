from fastapi import FastAPI
import uvicorn
import pandas as pd
import pickle

app = FastAPI(title="Movie Recommender System")
data = pd.read_csv('data/final_data.csv')

with open('mlruns/1/9d8cb8220262429fbc9bf0b548a4454a/artifacts/model/model.pkl', 'rb') as f:
    similarity = pickle.load(f)

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
    uvicorn.run(app, host='127.0.0.1', port=8000, debug=True)

