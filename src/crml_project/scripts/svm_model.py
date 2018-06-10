from crml_api.models import *
from scripts import extract_features
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from pymemcache.client import base
import pickle


def getClassifier():

    dic = {}

    try:
        client = base.Client(('localhost', 11211))
        classifier_in_bytes = client.get('svm_classifier')
        featuresIndex_in_bytes = client.get('featuresIndex')
    except:
        classifier_in_bytes = None
        featuresIndex_in_bytes = None

    if classifier_in_bytes and featuresIndex_in_bytes:
        print('load cached classifier....')
        classifier = pickle.loads(classifier_in_bytes)
        featuresDic = pickle.loads(featuresIndex_in_bytes)

    else:
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

        classifier = svm.SVC(decision_function_shape='ovo')
        classifier.fit(x, y)
        print('cache classifier.....')
        client.set('svm_classifier', pickle.dumps(classifier))
        client.set('featuresIndex', pickle.dumps(featuresDic))

    dic['classifier'] = classifier
    dic['featuresIndex'] = featuresDic

    return dic

