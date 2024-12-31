from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load movie dataset
movies_df = pd.read_csv("data/movies.csv")

# Function to recommend movies based on cosine similarity
def recommend_movies(query):
    # Create a TF-IDF Vectorizer to convert movie titles into vectors
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(movies_df['title'])

    # Transform the query into the same vector space
    query_vec = tfidf_vectorizer.transform([query])

    # Compute cosine similarity between the query and all movies
    cosine_similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()

    # Get indices of the most similar movies
    similar_indices = cosine_similarities.argsort()[-10:][::-1]

    # Return the top 10 most similar movies
    return movies_df['title'].iloc[similar_indices].tolist()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.json.get('query', '').lower()
    if query:
        # Get recommendations based on the query
        recommended_movies = recommend_movies(query)
        return jsonify({'movies': recommended_movies})
    return jsonify({'movies': []})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
