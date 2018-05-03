from crml_api.models import *
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import pickle

def run(*args):

    reviews = Reviewed.objects.filter(reviewed=True)
    vectorizer = CountVectorizer(strip_accents='ascii')
    transformer = TfidfTransformer()

    tags = []
    texts = []

    for r in reviews:
        text = r.reviewId.review_content
        tags.append(r.reviewId.reviewtag.tag.tagId)
        texts.append(text)

    if len(texts) == 0:
        return

    x = vectorizer.fit_transform(texts)
    tfidf = transformer.fit_transform(x)

    data = {}
    data['tag'] = tags
    data['feature'] = vectorizer.get_feature_names()
    data['tf'] = x.toarray()
    data['tfidf'] = tfidf.toarray()

    pickle.dump(data, open('temp.pkl', 'wb'))
    print('temp file created')