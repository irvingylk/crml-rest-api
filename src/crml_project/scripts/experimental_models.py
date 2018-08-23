from crml_api.models import Review, Performance_m1, Performance_m2, Algorithm, Training_m1, Training_m2
from sklearn import svm
from .evaluate_models import SelectTestSet, IncrementalTrainingSet, CalculateF1s

from .extract_features import GetM1FeaturesTf, GetM1PartialFeaturesIndex, GetM2FeaturesTf
from .extract_features import GetM2PartialFeaturesIndex, FeaturesTfToGlobal, GetBinaryFromTf
from .extract_features import ExtractFeatureFromCorpusM1, ExtractFeatureFromCorpusM2


def run(*args):
    print("start")
    Training_m1.objects.all().delete()
    Training_m2.objects.all().delete()
    print("remove done")
    reviews = Review.objects.filter(extracted=True)
    print("get reviews done")
    for review in reviews:

        corpus = review.review_content

        m1FeatureTf = ExtractFeatureFromCorpusM1(corpus)

        for feature in m1FeatureTf:

            try:
                print("here 1")
                Training_m1.objects.create(
                    reviewId=review, feature=feature, value=m1FeatureTf[feature])
                print("here 2")
            except:
                continue
        print("t1")

        m2FeatureTf = ExtractFeatureFromCorpusM2(corpus)

        for feature in m2FeatureTf:

            try:
                Training_m2.objects.create(
                    reviewId=review, feature=feature, value=m2FeatureTf[feature])
            except:
                continue

    print("extract done")
    testSet = SelectTestSet(20)
    print("testSet done")
    RewriteM1TfHistoricalPerformance(20, 1, testSet)
    RewriteM2BinaryHistoricalPerformance(20, 1, testSet)
    RewriteM2TfHistoricalPerformance(20, 1, testSet)
    RewriteM2BinaryHistoricalPerformance(20, 1, testSet)

    print("Done!")


def RewriteM1TfHistoricalPerformance(min: int, inc: int, testSet: [str]):

    Performance_m1.objects.filter(binary=False).delete()
    incSets = IncrementalTrainingSet(min, inc, testSet)

    for reviews in incSets:

        x, y = [], []
        partialFeaturesIndex = GetM1PartialFeaturesIndex(reviews)

        for review in reviews:

            featuresTf = GetM1FeaturesTf(review)
            x.append(FeaturesTfToGlobal(featuresTf, partialFeaturesIndex))
            y.append(review.tag.tagId)

        classifier = svm.SVC(decision_function_shape='ovo')
        classifier.fit(x, y)

        reviewsPredictions = {}

        testReviews = Review.objects.filter(reviewId__in=testSet)

        for review in testReviews:

            partialFeaturesVector = FeaturesTfToGlobal(
                GetM1FeaturesTf(review), partialFeaturesIndex)

            reviewsPredictions[review] = classifier.predict(
                [partialFeaturesVector])

        f1scores = CalculateF1s(reviewsPredictions)

        Performance_m1.objects.create(algorithm=Algorithm.objects.get(
            algorithmId=1), size=len(reviews), binary=False, sa_f1=f1scores[1],
            og_f1=f1scores[2], vr_f1=f1scores[3], sl_f1=f1scores[4], tx_f1=f1scores[5],
            ld_f1=f1scores[6], sp_f1=f1scores[7], ck_f1=f1scores[8], rs_f1=f1scores[9],
            lg_f1=f1scores[10], it_f1=f1scores[11], tr_f1=f1scores[12], pc_f1=f1scores[13],
            ot_f1=f1scores[14])


def RewriteM1BinaryHistoricalPerformance(min: int, inc: int, testSet: [str]):

    Performance_m1.objects.filter(binary=True).delete()
    incSets = IncrementalTrainingSet(min, inc, testSet)

    for reviews in incSets:

        x, y = [], []
        partialFeaturesIndex = GetM1PartialFeaturesIndex(reviews)

        for review in reviews:

            featuresTf = GetM1FeaturesTf(review)
            x.append(GetBinaryFromTf(FeaturesTfToGlobal(
                featuresTf, partialFeaturesIndex)))
            y.append(review.tag.tagId)

        classifier = svm.SVC(decision_function_shape='ovo')
        classifier.fit(x, y)

        reviewsPredictions = {}

        testReviews = Review.objects.filter(reviewId__in=testSet)

        for review in testReviews:

            partialFeaturesVector = FeaturesTfToGlobal(
                GetM1FeaturesTf(review), partialFeaturesIndex)

            reviewsPredictions[review] = classifier.predict(
                [partialFeaturesVector])

        f1scores = CalculateF1s(reviewsPredictions)

        Performance_m1.objects.create(algorithm=Algorithm.objects.get(
            algorithmId=1), size=len(reviews), binary=True, sa_f1=f1scores[1],
            og_f1=f1scores[2], vr_f1=f1scores[3], sl_f1=f1scores[4], tx_f1=f1scores[5],
            ld_f1=f1scores[6], sp_f1=f1scores[7], ck_f1=f1scores[8], rs_f1=f1scores[9],
            lg_f1=f1scores[10], it_f1=f1scores[11], tr_f1=f1scores[12], pc_f1=f1scores[13],
            ot_f1=f1scores[14])


def RewriteM2TfHistoricalPerformance(min: int, inc: int, testSet: [str]):

    Performance_m2.objects.filter(binary=False).delete()
    incSets = IncrementalTrainingSet(min, inc, testSet)

    for reviews in incSets:

        x, y = [], []
        partialFeaturesIndex = GetM2PartialFeaturesIndex(reviews)

        for review in reviews:

            featuresTf = GetM2FeaturesTf(review)
            x.append(FeaturesTfToGlobal(featuresTf, partialFeaturesIndex))
            y.append(review.tag.tagId)

        classifier = svm.SVC(decision_function_shape='ovo')
        classifier.fit(x, y)

        reviewsPredictions = {}

        testReviews = Review.objects.filter(reviewId__in=testSet)

        for review in testReviews:

            partialFeaturesVector = FeaturesTfToGlobal(
                GetM2FeaturesTf(review), partialFeaturesIndex)

            reviewsPredictions[review] = classifier.predict(
                [partialFeaturesVector])

        f1scores = CalculateF1s(reviewsPredictions)

        Performance_m2.objects.create(algorithm=Algorithm.objects.get(
            algorithmId=1), size=len(reviews), binary=False, sa_f1=f1scores[1],
            og_f1=f1scores[2], vr_f1=f1scores[3], sl_f1=f1scores[4], tx_f1=f1scores[5],
            ld_f1=f1scores[6], sp_f1=f1scores[7], ck_f1=f1scores[8], rs_f1=f1scores[9],
            lg_f1=f1scores[10], it_f1=f1scores[11], tr_f1=f1scores[12], pc_f1=f1scores[13],
            ot_f1=f1scores[14])


def RewriteM2BinaryHistoricalPerformance(min: int, inc: int, testSet: [str]):

    Performance_m2.objects.filter(binary=True).delete()
    incSets = IncrementalTrainingSet(min, inc, testSet)

    for reviews in incSets:

        x, y = [], []
        partialFeaturesIndex = GetM2PartialFeaturesIndex(reviews)

        for review in reviews:

            featuresTf = GetM2FeaturesTf(review)
            x.append(GetBinaryFromTf(FeaturesTfToGlobal(
                featuresTf, partialFeaturesIndex)))
            y.append(review.tag.tagId)

        classifier = svm.SVC(decision_function_shape='ovo')
        classifier.fit(x, y)

        reviewsPredictions = {}

        testReviews = Review.objects.filter(reviewId__in=testSet)

        for review in testReviews:

            partialFeaturesVector = GetBinaryFromTf(FeaturesTfToGlobal(
                GetM2FeaturesTf(review), partialFeaturesIndex))

            reviewsPredictions[review] = classifier.predict(
                [partialFeaturesVector])

        f1scores = CalculateF1s(reviewsPredictions)

        Performance_m2.objects.create(algorithm=Algorithm.objects.get(
            algorithmId=1), size=len(reviews), binary=True, sa_f1=f1scores[1],
            og_f1=f1scores[2], vr_f1=f1scores[3], sl_f1=f1scores[4], tx_f1=f1scores[5],
            ld_f1=f1scores[6], sp_f1=f1scores[7], ck_f1=f1scores[8], rs_f1=f1scores[9],
            lg_f1=f1scores[10], it_f1=f1scores[11], tr_f1=f1scores[12], pc_f1=f1scores[13],
            ot_f1=f1scores[14])
