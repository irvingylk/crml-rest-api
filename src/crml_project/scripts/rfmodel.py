from crml_api.models import *
from scripts import extract_features
from sklearn.ensemble import RandomForestClassifier


def classifier():

    extract_features.extractFeatures()
    features = Training.objects.values('feature').distinct()
    reviews = Review.objects.filter(extracted=True)

    featuresDic = {}
    for i in range(len(features)):
        featuresDic[features[i]['feature']] = i

    x, y = [], []

    for r in reviews:
        rsfs = Training.objects.filter(reviewId=r)
        n = [0] * len(features)
        
        for rf in rsfs:
            index = featuresDic[rf.feature]
            n[index] = float(rf.value)
        
        x.append(n)
        y.append(r.tag.tagId)

    if len(y) == 0:
        return None

    classifier = RandomForestClassifier()
    classifier.fit(x, y)

    dic = {}
    dic['classifier'] = classifier
    dic['featuresIndex'] = featuresDic

    return dic

def predict():

    return None

