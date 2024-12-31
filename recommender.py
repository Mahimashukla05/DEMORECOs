import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
movies = pd.read_csv('data/movies.csv')

# Fill missing values and preprocess
movies['genres'] = movies['genres'].fillna('')
movies['keywords'] = movies['keywords'].fillna('')
movies['tagline'] = movies['tagline'].fillna('')
movies['overview'] = movies['overview'].fillna('')

# Create combined features column
movies['combined_features'] = (
    movies['genres'] + " " +
    movies['keywords'] + " " +
    movies['tagline'] + " " +
    movies['overview']
)

# Vectorize features
vectorizer = CountVectorizer(stop_words='english')
feature_matrix = vectorizer.fit_transform(movies['combined_features'])

# Compute cosine similarity
similarity = cosine_similarity(feature_matrix)

# Recommendation function
def recommend_movies(movie_title):
    movie_title = movie_title.lower()
    if movie_title not in movies['title'].str.lower().values:
        return ["Movie not found. Please try again."]
    
    idx = movies[movies['title'].str.lower() == movie_title].index[0]
    scores = list(enumerate(similarity[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:11]  # Top 10 similar
    recommended = [movies.iloc[i[0]]['title'] for i in scores]
    return recommended
