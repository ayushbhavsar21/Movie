# app.py
from flask import Flask, render_template, request, jsonify
import pickle
import requests
app = Flask(__name__, static_url_path='/static')


@app.route('/')
def index():
    movies = pickle.load(open('./movie_list.pkl', 'rb'))
    return render_template('index.html', movies=movies['title'].values)

@app.route('/recommend', methods=['POST'])
def recommend():
    selected_movie = request.json['movie']
    recommended_movies = get_recommendations(selected_movie)
    return jsonify(recommended_movies)

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return full_path

def get_recommendations(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append({
            'name': movies.iloc[i[0]].title,
            'poster': fetch_poster(movie_id)
        })
    return recommended_movies

if __name__ == '__main__':
    movies = pickle.load(open('./movie_list.pkl','rb'))
    similarity = pickle.load(open('./similarity.pkl','rb'))
    app.run(debug=True)
