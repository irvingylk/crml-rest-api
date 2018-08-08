from crml_api.models import Review, Training
from sklearn.feature_extraction.text import CountVectorizer, ENGLISH_STOP_WORDS
from decimal import Decimal


def run(*args):

    extractFeatures()


def extractFeatures():

    reviews = Review.objects.filter(reviewed=True, extracted=False)

    for r in reviews:

        featuresTf = extractFeaturesFromCorpus(r.review_content)

        if featuresTf is None:
            continue

        for key in featuresTf:

            try:
                Training.objects.create(
                    reviewId=r, feature=key, value=Decimal(featuresTf[key].item()))
            except:
                continue

        r.extracted = True
        r.save()


def extractFeaturesFromCorpus(corpus) -> {}:

    vectorizer = CountVectorizer(
        strip_accents='ascii', stop_words=ENGLISH_STOP_WORDS)

    try:
        corpusVectorized = vectorizer.fit_transform([corpus]).toarray()
        corpusVectorized = corpusVectorized[0]
    except:
        return None

    featuresName = vectorizer.get_feature_names()

    dic = {}

    for i in range(len(featuresName)):

        dic[featuresName[i]] = corpusVectorized[i]

    return dic


def FeaturesVectorToGlobal(featuresVector: {}, featuresNameGlobalIndex: {}) -> []:

    n = [0] * len(featuresNameGlobalIndex)

    for key in featuresVector:

        if key in featuresNameGlobalIndex:

            index = featuresNameGlobalIndex[key]
            n[index] = featuresVector[key]

    return n


def GetGlobalFeaturesIndex() -> {}:

    features = Training.objects.values('feature').distinct()

    featuresDic = {}
    for i in range(len(features)):
        featuresDic[features[i]['feature']] = i

    return featuresDic


def GetFeaturesIndex(reviews: [Review]) -> {}:

    features = Training.objects.filter(
        reviewId__in=reviews).values('feature').distinct()

    featuresDic = {}

    for i in range(len(features)):
        featuresDic[features[i]['feature']] = i

    return featuresDic


def GetFeaturesVector(review) -> {}:

    trainings_from_review = Training.objects.filter(reviewId=review)
    featuresDic = {}

    for training in trainings_from_review:
        featuresDic[training.feature] = float(training.value)

    return featuresDic
