from fastapi import FastAPI
from .recommendations import load_data, clean_data, collaborative_filtering, content_based_filtering, model_based_filtering, cluster_based_recommendations

app = FastAPI()
books, ratings = load_data()
df = clean_data(books, ratings)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Book Recommendation API"}

@app.get("/recommendations/user/{user_id}")
def get_user_recommendations(user_id: int):
    recommendations = collaborative_filtering(df, user_id)
    return {"user_id": user_id, "recommendations": recommendations}

@app.get("/recommendations/book/{book_id}")
def get_book_recommendations(book_id: int, data_type: str = 'structured'):
    recommendations = content_based_filtering(books, book_id, data_type)
    return {"book_id": book_id, "recommendations": recommendations}

@app.get("/recommendations/model/{user_id}")
def get_model_recommendations(user_id: int):
    recommendations = model_based_filtering(ratings, user_id)
    return {"user_id": user_id, "recommendations": recommendations}

@app.get("/recommendations/cluster/{book_id}")
def get_cluster_recommendations(book_id: int):
    recommendations = cluster_based_recommendations(books, book_id)
    return {"book_id": book_id, "recommendations": recommendations}
