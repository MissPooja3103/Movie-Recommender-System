import pickle
import streamlit as st
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=d145eee15593afdad80a14199acc0a3f&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:13]:  # Get 12 recommended movies
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

# Custom HTML and CSS for header
header_html = """
    <style>
    .header {
        color: #ff6f61;
        font-size: 3em;
        font-weight: bold;
        text-align: center;
        font-family: 'Arial', sans-serif;
        text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5);
        padding: 20px;
        background-color: #f2f2f2;
        border-radius: 10px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 30px;
    }
    </style>
    <div class="header">
        Movie Recommender System
    </div>
"""

# Display the custom styled header
st.markdown(header_html, unsafe_allow_html=True)

movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    # Create 3 rows with 4 columns for each
    for i in range(0, 12, 4):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])
        with col2:
            st.text(recommended_movie_names[i+1])
            st.image(recommended_movie_posters[i+1])
        with col3:
            st.text(recommended_movie_names[i+2])
            st.image(recommended_movie_posters[i+2])
        with col4:
            st.text(recommended_movie_names[i+3])
            st.image(recommended_movie_posters[i+3])
