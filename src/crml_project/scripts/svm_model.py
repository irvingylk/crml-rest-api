from crml_api.models import Review
from sklearn import svm
from pymemcache.client import base
from . import extract_features
import pickle


SVM_Model_KEY = 'SVM_MODEL'
SVM_CLASSIFIER_POSITION = 0
SVM_GLOBAL_FEATURES_INDEX_POSITION = 1
TRAININGS_SIZE_POSITION = 2


def GetClassifier():

    try:
        client = base.Client(('localhost', 11211))
        model_in_bytes = client.get(SVM_Model_KEY)
        model = pickle.loads(model_in_bytes)
    except:
        model = None

    if model is None:
        model = CacheClassifier()

    return model


def CacheClassifier():

    reviews = Review.objects.filter(extracted=True)
    trainings_size = reviews.count()

    global_features_index = extract_features.GetGlobalFeaturesIndex()

    x, y = [], []

    for r in reviews:

        features_vector = extract_features.GetFeaturesVector(r)
        global_features_vector = extract_features.FeaturesVectorToGlobal(
            features_vector, global_features_index)

        x.append(global_features_vector)
        y.append(r.tag.tagId)

    classifier = svm.SVC(decision_function_shape='ovo')

    try:
        classifier.fit(x, y)
        client = base.Client(('localhost', 11211))
        model = (classifier, global_features_index, trainings_size)
        client.set(SVM_Model_KEY, pickle.dumps(model))
    except:

        return None

    return model


def MakePrediction(review):

    model = GetClassifier()

    if model:

        classifier = model[SVM_CLASSIFIER_POSITION]
        global_features_index = model[SVM_GLOBAL_FEATURES_INDEX_POSITION]
        trainings_size = model[TRAININGS_SIZE_POSITION]

        if trainings_size == review.trainings_size:

            if review.predicted:
                return (review.predicted.tagId, None)
            return None

        features_vector = extract_features.GetFeaturesVector(review)

        x = extract_features.FeaturesVectorToGlobal(
            features_vector, global_features_index)
        y = classifier.predict([x])

        return (y[0], trainings_size)

    return None


def GetClassifierWithSpecificReviews(reviews: [Review]):

    global_features_index = extract_features.GetFeaturesIndex(reviews)
    x, y = [], []

    for r in reviews:

        features_vector = extract_features.GetFeaturesVector(r)
        global_features_vector = extract_features.FeaturesVectorToGlobal(
            features_vector, global_features_index)

        x.append(global_features_vector)
        y.append(r.tag.tagId)

    classifier = svm.SVC(decision_function_shape='ovo')

    try:
        classifier.fit(x, y)
    except:
        return None

    return (classifier, global_features_index)
