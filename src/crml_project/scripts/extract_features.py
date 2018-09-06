from crml_api.models import Review, Training

import nltk
nltk.download('punkt')
nltk.download('stopwords')


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


def GetM1GlobalFeaturesIndex(reviews: [Review]) -> dict:

    globalFeaturesDic = {}
    index = 0

    for review in reviews:

        content = review.review_content

        features = RemoveStopWords(Tokenization(content))

        for feature in features:

            if feature not in globalFeaturesDic:

                globalFeaturesDic[feature] = index
                index += 1

    return globalFeaturesDic


# M2 = tokenization + stopwords + stemming


def ExtractFeatureFromCorpusM2(corpus: str) -> dict:

    return TermFrequency(SnowballStem(RemoveStopWords(Tokenization(corpus))))


def GetM2GlobalFeaturesIndex(reviews: [Review]) -> dict:

    globalFeaturesDic = {}
    index = 0

    for review in reviews:

        content = review.review_content

        features = SnowballStem(RemoveStopWords(Tokenization(content)))

        for feature in features:

            if feature not in globalFeaturesDic:

                globalFeaturesDic[feature] = index
                index += 1

    return globalFeaturesDic
