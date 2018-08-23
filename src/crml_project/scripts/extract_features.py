from crml_api.models import Review, Training, Training_m1, Training_m2
from sklearn.feature_extraction.text import CountVectorizer, ENGLISH_STOP_WORDS
from decimal import Decimal

import nltk
nltk.download('punkt')
nltk.download('stopwords')


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


def Tokenization(corpus: str) -> list:

    return nltk.word_tokenize(corpus)


def RemoveStopWords(tokens: list) -> list:

    stopwords = nltk.corpus.stopwords.words('english')
    non_stopwords_tokens = tokens[:]

    for token in tokens:

        if token in stopwords or len(token) == 1:

            non_stopwords_tokens.remove(token)

    return non_stopwords_tokens


def SnowballStem(tokens: list) -> list:

    stemmer = nltk.stem.snowball.SnowballStemmer("english")
    stemmed_tokens = []

    for token in tokens:

        stemmed_tokens.append(stemmer.stem(token))

    return stemmed_tokens


def TermFrequency(tokens: list) -> dict:

    return dict(nltk.FreqDist(tokens))


def FeaturesTfToGlobal(featuresVector: dict, featuresNameGlobalIndex: dict) -> list:

    n = [0] * len(featuresNameGlobalIndex)

    for key in featuresVector:

        if key in featuresNameGlobalIndex:

            index = featuresNameGlobalIndex[key]
            n[index] = featuresVector[key]

    return n


def GetBinaryFromTf(globalFeatureTf: list) -> list:

    n = []

    for v in globalFeatureTf:

        if v > 0:

            n.append(1)
        else:

            n.append(0)

    return n

# M1 = tokenization + stopwords


def ExtractFeatureFromCorpusM1(corpus: str) -> dict:

    return TermFrequency(RemoveStopWords(Tokenization(corpus)))


def GetM1GlobalFeaturesIndex() -> dict:

    features = Training_m1.objects.values('feature').distinct()
    featuresDic = {}

    for i in range(len(features)):
        featuresDic[features[i]['feature']] = i

    return featuresDic


def GetM1PartialFeaturesIndex(reviews: [Review]) -> dict:

    features = Training_m1.objects.filter(
        reviewId__in=reviews).values('feature').distinct()

    featuresDic = {}

    for i in range(len(features)):
        featuresDic[features[i]['feature']] = i

    return featuresDic


def GetM1FeaturesTf(review: Review) -> dict:

    trainings_from_review = Training_m1.objects.filter(reviewId=review)
    featuresTf = {}

    for training in trainings_from_review:
        featuresTf[training.feature] = float(training.value)

    return featuresTf


# M2 = tokenization + stopwords + stemming


def ExtractFeatureFromCorpusM2(corpus: str) -> dict:

    return TermFrequency(SnowballStem(RemoveStopWords(Tokenization(corpus))))


def GetM2GlobalFeaturesIndex() -> dict:

    features = Training_m2.objects.values('feature').distinct()
    featuresDic = {}

    for i in range(len(features)):
        featuresDic[features[i]['feature']] = i

    return featuresDic


def GetM2PartialFeaturesIndex(reviews: [Review]) -> dict:

    features = Training_m2.objects.filter(
        reviewId__in=reviews).values('feature').distinct()

    featuresDic = {}

    for i in range(len(features)):
        featuresDic[features[i]['feature']] = i

    return featuresDic


def GetM2FeaturesTf(review: Review) -> dict:

    trainings_from_review = Training_m2.objects.filter(reviewId=review)
    featuresTf = {}

    for training in trainings_from_review:
        featuresTf[training.feature] = float(training.value)

    return featuresTf
