from crml_api.models import *
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from decimal import Decimal
#import pickle

def run(*args):

    reviews = Review.objects.filter(reviewed=True, extracted=False)
    vectorizer = CountVectorizer(strip_accents='ascii')

    for r in reviews:

        tf_list = vectorizer.fit_transform([r.review_content]).toarray()[0]
        features = vectorizer.get_feature_names()
        r.extracted = True
        r.save()

        for i in range(len(features)):

            try:
                Training.objects.create(reviewId=r, feature=features[i], value=Decimal(tf_list[i].item()))
            except:
                print(r.review_content+" Save Failed")