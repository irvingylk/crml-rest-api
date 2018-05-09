from crml_api.models import *
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, ENGLISH_STOP_WORDS
from decimal import Decimal
#import pickle

def run(*args):

    reviews = Review.objects.filter(reviewed=True, extracted=False)
    vectorizer = CountVectorizer(strip_accents='ascii', stop_words=ENGLISH_STOP_WORDS)

    for r in reviews:

        try:
            a = vectorizer.fit_transform([r.review_content]).toarray()
        except:
            continue
        

        if len(a) == 0:
            continue

        tf_list = a[0]
        features = vectorizer.get_feature_names()
        r.extracted = True
        r.save()

        for i in range(len(features)):

            try:
                Training.objects.create(reviewId=r, feature=features[i], value=Decimal(tf_list[i].item()))
            except:
                print(r.review_content+" Save Failed")