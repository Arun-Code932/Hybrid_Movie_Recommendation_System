import pickle
import requests
import re
import os

from dotenv import load_dotenv
load_dotenv()
movies = pickle.load(
    open("/100_Days_of_ml/Hybrid_Movie_Recommendation_System/models/movies.pkl","rb")
)

content_similarity = pickle.load(
    open("/100_Days_of_ml/Hybrid_Movie_Recommendation_System/models/similarity.pkl","rb")
)

collaborative_similarity = pickle.load(
    open("/100_Days_of_ml/Hybrid_Movie_Recommendation_System/models/collaborative_similarity.pkl","rb")
)

movie_mapping = pickle.load(
    open("/100_Days_of_ml/Hybrid_Movie_Recommendation_System/models/movie_mapping.pkl","rb")
)

API_KEY = os.getenv("TMDB_API_KEY")

def clean_title(title):

    title = re.sub(r"\(\d{4}\)", "", title)

    title = title.lower()

    title = re.sub(r"[^a-z0-9\s]", " ", title)

    title = re.sub(r"\s+", " ", title)

    title = title.strip()

    return title

def get_movielens_title(tmdb_title):

    cleaned = clean_title(tmdb_title)

    movie = movie_mapping[
        movie_mapping["clean_title"] == cleaned
    ]

    if movie.empty:
        return None

    return movie.iloc[0]["movielens_title"]

def fetch_trailer(movie_id):

    try:

        url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={API_KEY}"

        response = requests.get(url)

        data = response.json()

        for video in data.get("results", []):

            if video["site"] == "YouTube" and video["type"] == "Trailer":

                return f"https://www.youtube.com/watch?v={video['key']}"

        return None

    except:

        return None
        

def fetch_movie_details(movie_id):

    try:

        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"

        response = requests.get(url)

        data = response.json()

        return {
                
                    "poster":
                    "https://image.tmdb.org/t/p/w500" + data["poster_path"]
                    if data.get("poster_path")
                    else "",
                
                    "rating":
                    data.get("vote_average", "N/A"),
                
                    "release":
                    data.get("release_date", "N/A"),
                
                    "overview":
                    data.get("overview", "No Overview"),
                
                    "genres":
                    ", ".join(
                        [genre["name"] for genre in data.get("genres", [])]
                    ),
                
                    "runtime":
                    data.get("runtime", "N/A"),
                
                    "language":
                    data.get("original_language", "N/A"),
                
                    "vote_count":
                    data.get("vote_count", "N/A"),
                
                    "trailer":
                    fetch_trailer(movie_id)
                
                }
    except:

        return {

                "poster": "",
            
                "rating": "N/A",
            
                "release": "N/A",
            
                "overview": "No Overview",
            
                "genres": "",
            
                "runtime": "N/A",
            
                "language": "N/A",
            
                "vote_count": "N/A",
            
                "trailer": None
            
            }
def get_selected_movie_details(movie):

    movie_data = movies[
        movies["title"] == movie
    ]

    if movie_data.empty:
        return None

    movie_id = movie_data.iloc[0]["id"]

    details = fetch_movie_details(movie_id)

    return {

        "title": movie,

        **details

    }


def recommend(movie):

    movie_index = movies[
        movies["title"] == movie
    ].index[0]

    distances = content_similarity[movie_index]

    movie_list = sorted(

    list(enumerate(distances)),

    key=lambda x: x[1],

    reverse=True

    )[1:21]

    recommendations = []

    for i in movie_list:

        movie_id = movies.iloc[i[0]].id

        details = fetch_movie_details(movie_id)

        recommendations.append(

    {

        "title": movies.iloc[i[0]].title,

        "score": i[1],

        "movie_id": movie_id,

        **details

    }

)

    return recommendations




def recommend_movie(movie):

    if movie not in collaborative_similarity.columns:

        return []

    similar_movies = collaborative_similarity[movie]

    similar_movies = similar_movies.sort_values(
        ascending=False
    )

    recommendations = []

    for movie_name, score in similar_movies.iloc[1:21].items():
        movie = movie_mapping[
            movie_mapping["movielens_title"] == movie_name
        ]

        if movie.empty:
            continue

        tmdb_title = movie.iloc[0]["tmdb_title"]

        movie_data = movies[
            movies["title"] == tmdb_title
        ]

        if movie_data.empty:
            continue

        movie_id = movie_data.iloc[0]["id"]

        details = fetch_movie_details(movie_id)

        recommendations.append({

            "title": tmdb_title,

            "score": score,

            "movie_id": movie_id,

            **details

        })

    return recommendations

def hybrid_recommend(movie, n=5):

    # Content-Based Recommendations
    content_movies = recommend(movie)

    # Convert TMDB title to MovieLens title
    movielens_title = get_movielens_title(movie)

    # Collaborative Recommendations
    if movielens_title:
        collaborative_movies = recommend_movie(movielens_title)
    else:
        collaborative_movies = []

    
    final_scores = {}


    for movie in content_movies:

        final_scores[movie["title"]] = {

            "data": movie,

            "score": movie["score"] * 0.6

        }
   
    for movie in collaborative_movies:

        if movie["title"] in final_scores:

            final_scores[movie["title"]]["score"] += movie["score"] * 0.4

        else:

            final_scores[movie["title"]] = {

                "data": movie,

                "score": movie["score"] * 0.4

            }

    
    sorted_movies = sorted(

        final_scores.values(),

        key=lambda x: x["score"],

        reverse=True

    )


    recommendations = []

    for movie in sorted_movies[:n]:

        recommendations.append(movie["data"])

    return recommendations
