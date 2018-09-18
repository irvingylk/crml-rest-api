from crml_api.models import Review, Training
import nltk
nltk.download('punkt')
nltk.download('stopwords')

E1 = "tokenization, stop-words, term-frequency"
E2 = "tokenization, stop-words, binary"
E3 = "tokenization, stop-words, stemming, term-frequency"
E4 = "tokenization, stop-words, stemming, binary"
E5 = "tokenization, stop-words, term-frequency, tfidf"
E6 = "tokenization, stop-words, binary, tfidf"
E7 = "tokenization, stop-words, stemming, term-frequency, tfidf"
E8 = "tokenization, stop-words, stemming, binary, tfidf"

E9 = "tokenization, stop-words, term-frequency, SMOTEENN"
E10 = "tokenization, stop-words, binary, SMOTEENN"
E11 = "tokenization, stop-words, stemming, term-frequency, SMOTEENN"
E12 = "tokenization, stop-words, stemming, binary, SMOTEENN"
E13 = "tokenization, stop-words, term-frequency, tfidf, SMOTENN"
E14 = "tokenization, stop-words, binary, tfidf, SMOTENN"
E15 = "tokenization, stop-words, stemming, term-frequency, tfidf, SMOTENN"
E16 = "tokenization, stop-words, stemming, binary, tfidf, SMOTENN"

E17 = "tokenization, stop-words, term-frequency, SMOTETOMEK"
E18 = "tokenization, stop-words, binary, SMOTETOMEK"
E19 = "tokenization, stop-words, stemming, term-frequency, SMOTETOMEK"
E20 = "tokenization, stop-words, stemming, binary, SMOTETOMEK"
E21 = "tokenization, stop-words, term-frequency, tfidf, SMOTETOMEK"
E22 = "tokenization, stop-words, binary, tfidf, SMOTETOMEK"
E23 = "tokenization, stop-words, stemming, term-frequency, tfidf, SMOTETOMEK"
E24 = "tokenization, stop-words, stemming, binary, tfidf, SMOTETOMEK"

USE_STEMMING = [E3, E4, E7, E8, E11, E12, E15, E16, E19, E20, E23, E24]
USE_BINARY = [E2, E4, E6, E8, E10, E12, E14, E16, E18, E20, E22, E24]
USE_TF = [E1, E3, E5, E7, E9, E11, E13, E15, E17, E19, E21, E23]
USE_TFIDF = [E5, E6, E7, E8, E13, E14, E15, E16, E21, E22, E23, E24]
USE_SMOTEENN = [E9, E10, E11, E12, E13, E14, E15, E16]
USE_SMOTETOMEK = [E17, E18, E19, E20, E21, E22, E23, E24]


def FeaturesVectorToGlobal(featuresVector: {}, featuresNameGlobalIndex: {}) -> []:

    n = [0] * len(featuresNameGlobalIndex)

    for key in featuresVector:

        if key in featuresNameGlobalIndex:

            index = featuresNameGlobalIndex[key]
            n[index] = featuresVector[key]

    return n


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


def GetBinaryFromTf(tf: dict) -> list:

    for t in tf:

        if tf[t] > 0:
            tf[t] = 1
        else:
            tf[t] = 0

    return tf


def GetGlobalFeaturesIndex(review: [Review], train_index: [int], extractionMethod: str) -> dict:

    globalFeaturesDic = {}
    globalFeatures = []

    if extractionMethod not in USE_STEMMING:

        for i in train_index:

            content = review[i].review_content
            globalFeatures += RemoveStopWords(Tokenization(content))

    elif extractionMethod in USE_STEMMING:

        for i in train_index:

            content = review[i].review_content
            globalFeatures += SnowballStem(
                RemoveStopWords(Tokenization(content)))

    globalFeatures = list(set(globalFeatures))

    for i in range(len(globalFeatures)):

        globalFeaturesDic[globalFeatures[i]] = i

    return globalFeaturesDic


def ExtractFeatureFromCorpus(globalFeaturesDic: dict, corpus: str, extractionMethod: str) -> list:

    if extractionMethod in USE_TF and extractionMethod not in USE_STEMMING:
        return FeaturesTfToGlobal(TermFrequency(RemoveStopWords(Tokenization(corpus))), globalFeaturesDic)
    elif extractionMethod in USE_BINARY and extractionMethod not in USE_STEMMING:
        return FeaturesTfToGlobal(GetBinaryFromTf(TermFrequency(RemoveStopWords(Tokenization(corpus)))), globalFeaturesDic)
    elif extractionMethod in USE_TF and extractionMethod in USE_STEMMING:
        return FeaturesTfToGlobal(TermFrequency(SnowballStem(RemoveStopWords(Tokenization(corpus)))), globalFeaturesDic)
    elif extractionMethod in USE_BINARY and extractionMethod in USE_STEMMING:
        return FeaturesTfToGlobal(GetBinaryFromTf(TermFrequency(SnowballStem(RemoveStopWords(Tokenization(corpus))))), globalFeaturesDic)

    return None
