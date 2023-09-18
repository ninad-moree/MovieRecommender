import streamlit as st
import pickle
import pandas as pd
import requests


def posters(movie_id):
    # the url is fetched from the Tmdb website;
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=8fca304aff144d0a24d0c626616c03bf&language=en-US'.format(
            movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]  # calculating the index of the movie name
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(posters(movie_id))
    return recommended_movies, recommended_movies_posters


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Choose A Movie Name',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters1 = recommend(selected_movie_name)

    st.text("Recommended movies are :")

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters1[0])
    with col2:
        st.text(names[1])
        st.image(posters1[1])
    with col3:
        st.text(names[2])
        st.image(posters1[2])
    with col4:
        st.text(names[3])
        st.image(posters1[3])
    with col5:
        st.text(names[4])
        st.image(posters1[4])
