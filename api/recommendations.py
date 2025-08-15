import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD

def load_data():
    books = pd.read_csv('data/books.csv')
    ratings = pd.read_csv('data/ratings.csv')
    return books, ratings

def clean_data(books, ratings):
    df = pd.merge(ratings, books, on='book_id')
    df.dropna(inplace=True)
    return df

def collaborative_filtering(df, user_id):
    user_item_matrix = df.pivot_table(index='user_id', columns='book_id', values='rating')
    user_item_matrix.fillna(0, inplace=True)
    user_similarity = cosine_similarity(user_item_matrix)
    user_similarity_df = pd.DataFrame(user_similarity, index=user_item_matrix.index, columns=user_item_matrix.index)
    
    similar_users = user_similarity_df[user_id].sort_values(ascending=False).index[1:]
    recommended_books = []
    for similar_user in similar_users:
        recommended_books.extend(user_item_matrix.loc[similar_user].sort_values(ascending=False).index)
    
    recommended_books = [book for book in recommended_books if user_item_matrix.loc[user_id, book] == 0]
    return list(dict.fromkeys(recommended_books))[:10]

def content_based_filtering(books, book_id, data_type='structured'):
    if data_type == 'unstructured':
        corpus = []
        for book_id_val in books['book_id']:
            try:
                with open(f'data/unstructured/{book_id_val}.txt', 'r') as f:
                    corpus.append(f.read())
            except FileNotFoundError:
                corpus.append('')
        
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(corpus)
    else: # structured
        books['content'] = books['title'] + ' ' + books['author'] + ' ' + books['genre']
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(books['content'])

    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    idx = books[books['book_id'] == book_id].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    book_indices = [i[0] for i in sim_scores]
    return books['book_id'].iloc[book_indices].tolist()

def model_based_filtering(ratings, user_id):
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(ratings[['user_id', 'book_id', 'rating']], reader)
    trainset, testset = train_test_split(data, test_size=0.25)
    
    algo = SVD()
    algo.fit(trainset)
    
    predictions = algo.test(testset)
    
    user_predictions = [pred for pred in predictions if pred.uid == user_id]
    user_predictions.sort(key=lambda x: x.est, reverse=True)
    
    recommended_book_ids = [pred.iid for pred in user_predictions[:10]]
    return recommended_book_ids

def cluster_based_recommendations(books, book_id, n_clusters=5):
    books['content'] = books['title'] + ' ' + books['author'] + ' ' + books['genre']
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(books['content'])
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    kmeans.fit(tfidf_matrix)
    
    cluster_labels = kmeans.labels_
    books['cluster'] = cluster_labels
    
    book_cluster = books[books['book_id'] == book_id]['cluster'].iloc[0]
    
    recommended_books = books[books['cluster'] == book_cluster]
    recommended_books = recommended_books[recommended_books['book_id'] != book_id]
    
    return recommended_books['book_id'].head(10).tolist()

def dimensionality_reduction(ratings):
    user_item_matrix = ratings.pivot_table(index='user_id', columns='book_id', values='rating').fillna(0)
    svd = TruncatedSVD(n_components=50, random_state=42)
    matrix_reduced = svd.fit_transform(user_item_matrix)
    return matrix_reduced
