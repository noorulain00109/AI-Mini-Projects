"""
Movie Match Movie Recommendation System
A clean Streamlit app built on top of a content-based
similarity model (movies.pkl + similarity.pkl).

Run with:  streamlit run app.py
"""

import random
import pickle
from pathlib import Path

import streamlit as st

# ----------------------------------------------------------------------
# PAGE CONFIG (must be first Streamlit call)
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Movie Match |  Movie Recommender",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ----------------------------------------------------------------------
# STYLING — simple, solid, light theme
# ----------------------------------------------------------------------
def inject_css():
    st.markdown(
        """
   <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    .stApp {
        background: #f7f8fc;
        color: #22223b;
    }

    /* Hide default Streamlit chrome */
    #MainMenu, footer, header {
        visibility: hidden;
    }

    /* Hero banner */
    .hero {
        padding: 2.2rem 2rem;
        border-radius: 20px;
        background: #6c63ff;
        margin-bottom: 1.8rem;
    }

    .hero h1 {
        font-size: 2.6rem;
        font-weight: 800;
        margin: 0;
        color: white;
        letter-spacing: -1px;
    }

    .hero p {
        font-size: 1.05rem;
        color: rgba(255, 255, 255, 0.92);
        margin-top: 0.4rem;
    }

    /* Section headers */
    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin: 1.6rem 0 0.8rem 0;
        border-left: 5px solid #6c63ff;
        padding-left: 0.7rem;
        color: #22223b;
    }

    /* Movie card */
    .movie-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 0.9rem;
        transition: box-shadow 0.2s ease, border 0.2s ease;
        height: 100%;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }

    .movie-card:hover {
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
        border: 1px solid #c9c6f7;
    }

    .movie-title {
        font-weight: 600;
        font-size: 1rem;
        line-height: 1.3rem;
        min-height: 2.5rem;
        color: #22223b;
    }

    .movie-rating {
        display: inline-block;
        background: #e5e2fd;
        color: #3f3a70;
        font-weight: 600;
        font-size: 0.78rem;
        padding: 2px 9px;
        border-radius: 8px;
        margin-top: 0.4rem;
    }

    /* Buttons */
    div.stButton > button {
        background: #6c63ff;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.55rem 1.2rem;
        font-weight: 600;
    }

    div.stButton > button:hover {
        background: #5a52e0;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e5e7eb;
    }

    section[data-testid="stSidebar"] * {
        color: #22223b;
    }

    .footer-note {
        text-align: center;
        color: #8a8a9a;
        font-size: 0.8rem;
        margin-top: 3rem;
    }
</style>
        """,
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------------------
# DATA LOADING
# ----------------------------------------------------------------------
@st.cache_resource(show_spinner="Loading movie database...")
def load_data():
    models_dir = Path("models")
    movies = pickle.load(open(models_dir / "movies.pkl", "rb"))
    similarity = pickle.load(open(models_dir / "similarity.pkl", "rb"))
    return movies, similarity


def get_title_col(movies):
    """Support either 'title_x' or plain 'title' column naming."""
    for candidate in ("title_x", "title"):
        if candidate in movies.columns:
            return candidate
    raise KeyError("No title column found in movies dataframe.")


def movie_display_data(movies, idx):
    """Return a dict of display info for a movie row."""
    title_col = get_title_col(movies)
    title = movies.iloc[idx][title_col]
    return {"title": title}


# ----------------------------------------------------------------------
# RECOMMENDATION ENGINE
# ----------------------------------------------------------------------
def recommend(movies, similarity, movie_title, top_n=5):
    title_col = get_title_col(movies)
    matches = movies[movies[title_col] == movie_title]
    if matches.empty:
        return []
    movie_index = matches.index[0]
    distances = similarity[movie_index]
    ranked = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1],
    )[1: top_n + 1]
    return [(i, score) for i, score in ranked]


# ----------------------------------------------------------------------
# UI COMPONENTS
# ----------------------------------------------------------------------
def render_movie_card(details, score=None):
    match_html = ""
    if score is not None:
        match_html = f'<span class="movie-rating">{score * 100:.0f}% match</span>'

    st.markdown(
        f"""
        <div class="movie-card">
            <div class="movie-title">{details['title']}</div>
            {match_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.expander("Details"):
        st.markdown(
            f"[Watch trailer on YouTube](https://www.youtube.com/results?search_query={details['title'].replace(' ', '+')}+trailer)"
        )


# ----------------------------------------------------------------------
# MAIN APP
# ----------------------------------------------------------------------
def main():
    inject_css()

    # ---------------- Sidebar ----------------
    with st.sidebar:
        st.markdown("## Movie Match")
        st.caption("Movie recommendations")

        top_n = st.slider("Number of recommendations", min_value=3, max_value=10, value=5)

    # ---------------- Load data ----------------
    try:
        movies, similarity = load_data()
    except FileNotFoundError:
        st.error(
            "Couldn't find `models/movies.pkl` or `models/similarity.pkl`. "
            "Make sure these files sit inside a `models/` folder next to this script."
        )
        st.stop()

    title_col = get_title_col(movies)
    movie_list = movies[title_col].values

    # ---------------- Hero ----------------
    st.markdown(
        """
        <div class="hero">
            <h1>Movie Match</h1>
            <p>Find something worth watching, powered by smart recommendations</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---------------- Search + Surprise Me ----------------
    col_search, col_random = st.columns([4, 1])
    with col_search:
        selected_movie = st.selectbox("Search for a movie you love", movie_list)
    with col_random:
        st.write("")
        st.write("")
        if st.button("Random Guess"):
            selected_movie = random.choice(movie_list)
            st.session_state["forced_selection"] = selected_movie

    if st.session_state.get("forced_selection"):
        selected_movie = st.session_state.pop("forced_selection")
        st.info(f"Randomly picked: **{selected_movie}**")

    # ---------------- Selected movie preview ----------------
    sel_idx = movies[movies[title_col] == selected_movie].index[0]
    sel_details = movie_display_data(movies, sel_idx)

    st.markdown('<div class="section-title">You selected</div>', unsafe_allow_html=True)
    st.subheader(sel_details["title"])

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------- Recommend button ----------------
    if st.button("Get Recommendations", type="primary"):
        with st.spinner("Finding movies you'll love..."):
            results = recommend(movies, similarity, selected_movie, top_n=top_n)

        if not results:
            st.warning("No recommendations found for this movie.")
        else:
            st.markdown('<div class="section-titl' \
            'e">Recommended for you</div>', unsafe_allow_html=True)
            cols = st.columns(min(len(results), 5))
            for pos, (idx, score) in enumerate(results):
                details = movie_display_data(movies, idx)
                with cols[pos % len(cols)]:
                    render_movie_card(details, score=score)

    st.markdown(
        '<div class="footer-note">Movie Match | Content-based recommendation engine</div>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()