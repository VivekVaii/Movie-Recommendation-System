import streamlit as st
import pickle

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)

# ---------------- LOAD DATA ---------------- #

movies = pickle.load(open("movies.pkl", "rb"))


# ---------------- BUILD SIMILARITY ---------------- #

@st.cache_resource
def build_similarity(df):

    cv = CountVectorizer(max_features=5000, stop_words="english")

    vectors = cv.fit_transform(df["tags"]).toarray()

    similarity = cosine_similarity(vectors)

    return similarity


similarity = build_similarity(movies)


# ---------------- RECOMMEND FUNCTION ---------------- #

def recommend(movie):

    movie_index = movies[movies["title"] == movie].index[0]

    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []

    for i in movie_list:
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies


# ---------------- SIDEBAR ---------------- #

st.sidebar.title("About")

st.sidebar.info("""
This project recommends movies using

✅ Content-Based Filtering

✅ NLP (CountVectorizer)

✅ Cosine Similarity

Dataset: TMDB 5000 Movies
""")


# ---------------- TITLE ---------------- #

st.markdown(
    "<h1 style='text-align:center;'>🎬 Movie Recommendation System</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center;'>Find movies similar to your favorite ones!</p>",
    unsafe_allow_html=True
)

# ---------------- SELECT BOX ---------------- #

selected_movie = st.selectbox(
    "Select a Movie",
    movies["title"].values
)

# ---------------- BUTTON ---------------- #

if st.button("Recommend"):

    with st.spinner("Finding similar movies..."):
        recommendations = recommend(selected_movie)

    st.success("Recommendations Ready!")

    st.subheader("Recommended Movies")

    cols = st.columns(5)

    for i, movie in enumerate(recommendations):
        with cols[i]:
            st.markdown("## 🎬")
            st.write(movie)


# ---------------- FOOTER ---------------- #

st.markdown("---")

