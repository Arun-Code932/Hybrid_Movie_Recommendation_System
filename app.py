import streamlit as st
import pickle
import time
from recommender import hybrid_recommend, get_selected_movie_details



st.set_page_config(
    page_title="🎬 CineMatch AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)




# ---------------- THEME ---------------- #
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

movies = pickle.load(
    open("models/movies.pkl", "rb")
)



st.markdown("""
<div style='text-align:center;'>

<h1>🎬 CineMatch AI</h1>

<h4 style='color:gray;'>

Discover your next favourite movie using AI

</h4>

</div>
""", unsafe_allow_html=True)

st.divider()




st.markdown("## 🔎 Find Your Favourite Movie")

# Movie Dropdown
selected_movie = st.selectbox(
    "🎥 Select Movie",
    movies["title"].values
)

# Number of Recommendations Dropdown
num_movies = st.selectbox(
    "🎬 Number of Recommendations",
    [5, 10, 15]
)

# Search Button
search = st.button(
    "🔍 Search Movies",
    use_container_width=True
)


if search:

    progress_text = st.empty()
    progress_bar = st.progress(0)
    
    progress_text.write("🍿 Preparing recommendations...")
    progress_bar.progress(20)
    time.sleep(0.5)
    
    progress_text.write("🤖 AI is analyzing movie similarities...")
    progress_bar.progress(40)
    time.sleep(0.5)
    
    progress_text.write("🎬 Fetching movie details...")
    progress_bar.progress(60)
    time.sleep(0.5)
    
    progress_text.write("🖼 Loading movie posters...")
    progress_bar.progress(80)
    time.sleep(0.5)
    
    recommendations = hybrid_recommend(
        selected_movie,
        num_movies
    )
    
    progress_text.write("✅ Recommendations Ready!")
    progress_bar.progress(100)
    time.sleep(0.5)
    
    progress_bar.empty()
    progress_text.empty()

    selected_details = get_selected_movie_details(selected_movie)
        
    top_movie = recommendations[0]["title"]
        
    st.markdown(f"## 📌 Selected Movie : **{selected_movie}**")

    with st.container(border=True):
            
                st.image(
                    selected_details["poster"],
                    width=250
                )
            
                st.write(f"⭐ Rating : {selected_details['rating']}")
            
                st.write(f"🎭 {selected_details['genres']}")
            
                st.write(f"📅 Release : {selected_details['release']}")
            
                st.write(f"⏱ Runtime : {selected_details['runtime']} min")
            
                if selected_details["trailer"]:
            
                    st.link_button(
                        "🎥 Watch Trailer",
                        selected_details["trailer"],
                        use_container_width=True
                    )
            
                st.success(f"🥇 AI's Top Recommendation : **{top_movie}**")

                st.divider()
        
    
    
    cols = st.columns(5)

    st.divider()

    if num_movies == 5:

        cols = st.columns(5)
    
    elif num_movies == 10:
    
        cols = st.columns(5)
    
    else:
    
        cols = st.columns(5)

    for i, movie in enumerate(recommendations):

        if i % 5 == 0:
    
            cols = st.columns(5)
    
        with cols[i % 5]:

            with st.container(border=True):

                st.image(
                    movie["poster"],
                    use_container_width=True
                )

                st.markdown(
                    f"""
                    <h4 style='text-align:center;'>
                    {movie['title']}
                    </h4>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"""
                    <p style='text-align:center;'>
                    ⭐ <b>{movie['rating']}</b>
                    </p>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"""
                    <p style='text-align:center;'>
                    🎭 {movie['genres']}
                    </p>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"""
                    <p style='text-align:center;'>
                    📅 {movie['release']}
                    </p>
                    """,
                    unsafe_allow_html=True
                )

                with st.expander("📖 Story"):

                    st.write(movie["overview"])

                if movie["trailer"]:

                    st.link_button(
                        "🎥 Watch Official Trailer",
                        movie["trailer"],
                        use_container_width=True
                    )

                else:
                
                    st.info("Trailer Not Available")
st.divider()

st.markdown(
"""
<div style='text-align:center;'>

<h4>🎬 CineMatch AI</h4>

<p>
Made with ❤️ by <b>Arun Kumar</b>
</p>

<p>
Python • Pandas • Scikit-Learn • Streamlit • TMDB API
</p>

</div>
""",
unsafe_allow_html=True
)
