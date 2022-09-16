## Import Libraries 
import pandas as pd
import ast #Importing Abstract Syntax Trees

##Import Dataset 
credit = pd.read_csv('data/credits.csv')
movies = pd.read_csv('data/movies.csv')

print('Data Loaded Sucessfully!!!!!!')

## merge dataset 
df_movies = movies.merge(credit, on="title")
print(len(df_movies))

### selecting important columns 
df_movies = df_movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]\

###drop missing nan 
df_movies.dropna(inplace=True)
df_movies.isnull().sum()

## Define Data Cleaning Functions 

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


df_movies['genres'] = df_movies['genres'].apply(convert)
df_movies['keywords'] = df_movies['keywords'].apply(convert)
df_movies['cast'] = df_movies['cast'].apply(convertCast)
df_movies['crew'] = df_movies['crew'].apply(get_director)
df_movies['overview'] = df_movies['overview'].apply(lambda x : x.split())
df_movies['tags'] = df_movies['overview'] + df_movies['genres'] + df_movies['keywords'] + df_movies['cast'] + df_movies['crew']
final_df = df_movies[['movie_id','title','tags']]
final_df['tags'] = final_df['tags'].apply(lambda x :" ".join(x))
final_df['tags'] = final_df['tags'].apply(lambda x :x.replace(",",""))
print('Data Cleaned Successfully!!!')

final_df.to_csv('data/final_data.csv', index=False)
print('Data Saved Successfully!!!')