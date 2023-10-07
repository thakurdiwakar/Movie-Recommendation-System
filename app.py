import pandas as pd
import streamlit as st
import pickle
import requests
from imdb import IMDb

# Function to fetch movie poster from API


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=c47c17d18af7b44870b3e69c1a189acf&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

# Function to recommend movies


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movie = []
    recommend_movie_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommend_movie.append(movies.iloc[i[0]].title)
        # Fetch Poster from API
        recommend_movie_posters.append(fetch_poster(movie_id))
    return recommend_movie, recommend_movie_posters

# Load movie data and similarity matrix
movies_dict = pickle.load(open('model/movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('model/similarity.pkl', 'rb'))

# Set Streamlit app title
st.title('Movie Recommendation System')

# Create a sidebar for movie details
st.sidebar.header('Movie Details')

# Create a select box for movie selection
selected_movie_name = st.sidebar.selectbox('Search Your Movie', movies['title'].values)

# Display movie poster in the sidebar
selected_movie_id = movies[movies['title'] == selected_movie_name]['movie_id'].values[0]
st.sidebar.image(fetch_poster(selected_movie_id), use_column_width=True)

# Create a star rating component
movie_rating = st.sidebar.slider('Rate the movie:', 0, 10, 5, 1)

# Custom CSS styles for improved appearance
st.markdown(
    """
    <style>
    .stSelectbox {
        width: 100%;
        padding: 10px;
    }
    .stButton {
        width: 100%;
        padding: 10px;
        background-color: #007BFF;
        color: white;
        font-weight: bold;
        border-radius: 5px;
    }
    .stButton:hover {
        background-color: #0056b3;
    }
    .stImage {
        max-width: 100%;
        height: auto;
    }
    .sidebar .sidebar-content {
        background-color: #f5f5f5;
        padding: 20px;
        border-radius: 10px;
    }
    .sidebar .stTextInput {
        width: 100%;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Create a button to trigger recommendations
if st.button('Recommend'):
    with st.spinner("Fetching recommendations..."):
        names, posters = recommend(selected_movie_name)
        cols = st.columns(5)

        for i, col in enumerate(cols):
            with col:
                st.image(posters[i], caption=names[i], width=200)


# Display movie description and rating in the sidebar using IMDbPY
ia = IMDb()
movie_info = ia.get_movie(selected_movie_id)

st.sidebar.header('Movie Description')
if 'plot' in movie_info:
    st.sidebar.write(movie_info['plot'])
else:
    st.sidebar.write('Description not available')

st.sidebar.header('Your Rating')
st.sidebar.write(f'You rated this movie: {movie_rating}/10')


