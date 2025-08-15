import streamlit as st
import pandas as pd
import sys
sys.path.append('api')
from recommendations import content_based_filtering, load_data

st.title("Book Recommendation Engine")

books, _ = load_data()
book_titles = books['title'].tolist()

selected_book = st.selectbox("Select a book you like:", book_titles)

if st.button("Get Recommendations"):
    book_id = books[books['title'] == selected_book]['book_id'].iloc[0]
    recommendations = content_based_filtering(books, book_id)
    recommended_books = books[books['book_id'].isin(recommendations)]
    st.write("Here are your top 10 recommendations:")
    for index, row in recommended_books.iterrows():
        st.write(f"- {row['title']} by {row['author']}")
