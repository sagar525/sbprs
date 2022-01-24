import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer


class RecommendationSystem:

    def __init__(self):
        #load the pickles files and review data
        self.predicted_ratings = pickle.load(open('pickles/predicted_ratings.pkl', 'rb'))
        self.sentiment_model = pickle.load(open('pickles/model.pkl', 'rb'))
        self.vocabulary = pickle.load(open('pickles/tfidfvocabulary.pkl', 'rb'))
        self.reviews_db = pd.read_csv('data/sample30.csv')
        self.vectorizer = TfidfVectorizer(strip_accents='unicode',
                                          vocabulary=self.vocabulary)

    def recommend_products(self, username):

        ## check the username
        if username.lower() not in self.reviews_db['reviews_username'].str.lower().values:
            return None

        ## if exists get the recommended products using recommendation system
        item_list = self.predicted_ratings.loc[username].sort_values(ascending=False)[0:20].index

        ## filter out the data of those items
        item_review_data = self.reviews_db[self.reviews_db['name'].isin(item_list)]

        # vectorize reviews
        review_vectors = self.vectorizer.fit_transform(item_review_data['reviews_text'])

        #calculate predictions
        item_review_data['prediction'] = self.sentiment_model.predict(review_vectors)

        #count total positives(-- Note 0: Negative so they will not be counted)
        item_review_data = item_review_data.groupby('name').sum()

        #get the percentage
        item_review_data['positive_percentage'] = item_review_data.apply(lambda x: x['prediction'] / sum(x),
                                                                         axis=1)
        #pick top 5
        best_5 = item_review_data.sort_values('positive_percentage', ascending=False).iloc[:5, :].index

        #send to calling program
        return self.reviews_db[self.reviews_db.name.isin(best_5)][[
                  'name', 'brand', 'categories', 'manufacturer']].drop_duplicates().to_html(index=False)



