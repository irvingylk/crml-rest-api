from crml_api.models import Review, Performance_m1, Performance_m2, Algorithm, Performance_unbalanced_learn
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from .evaluate_models import SelectTestSet, IncrementalTrainingSet, CalculateF1s

from .extract_features import GetM1GlobalFeaturesIndex, GetM2GlobalFeaturesIndex
from .extract_features import FeaturesTfToGlobal, GetBinaryFromTf
from .extract_features import ExtractFeatureFromCorpusM1, ExtractFeatureFromCorpusM2
from sklearn.feature_extraction.text import TfidfTransformer

from imblearn.under_sampling import CondensedNearestNeighbour, EditedNearestNeighbours, TomekLinks, AllKNN, RandomUnderSampler
from imblearn.under_sampling import InstanceHardnessThreshold, NearMiss, NeighbourhoodCleaningRule, OneSidedSelection, RepeatedEditedNearestNeighbours
from imblearn.over_sampling import ADASYN, SMOTE, RandomOverSampler

from imblearn.combine import SMOTEENN, SMOTETomek

import numpy

from random import shuffle


svc_with_linear_kernel = svm.SVC(kernel='linear', C=1.0)
linear_svc = svm.LinearSVC(C=1.0)
svc_with_rbf_kernel = svm.SVC(kernel='rbf', gamma=0.7, C=1.0)
svc_with_polynomial = svm.SVC(kernel='poly', degree=3, C=1.0)

svm_classifier = svc_with_linear_kernel
rf_classifier = RandomForestClassifier(max_depth=4, random_state=0)


def run(*args):
    print("start")

    reviews = list(Review.objects.filter(reviewed=True))
    shuffle(reviews)
    print("get reviews done")

    print("extract done")
    trainingTestSet = SelectTestSet(reviews, 20)
    print("trainingsTestSet done")

    if trainingTestSet:

        '''
        RewriteM1TfHistoricalPerformance(
            20, 10, 1, trainingTestSet[0], trainingTestSet[1])
        RewriteM1BinaryHistoricalPerformance(
            20, 10, 1, trainingTestSet[0], trainingTestSet[1])
        RewriteM2TfHistoricalPerformance(
            20, 10, 1, trainingTestSet[0], trainingTestSet[1])
        RewriteM2BinaryHistoricalPerformance(
            20, 10, 1, trainingTestSet[0], trainingTestSet[1])
        RewriteM1TfHistoricalPerformance(
            20, 10, 2, trainingTestSet[0], trainingTestSet[1])
        RewriteM1BinaryHistoricalPerformance(
            20, 10, 2, trainingTestSet[0], trainingTestSet[1])
        RewriteM2TfHistoricalPerformance(
            20, 10, 2, trainingTestSet[0], trainingTestSet[1])
        RewriteM2BinaryHistoricalPerformance(
            20, 10, 2, trainingTestSet[0], trainingTestSet[1])
        '''
        # support vector machine
        UnbalancedLearnModel(
            1, "CNN", False, trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(
            1, "ENN", False, trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(
            1, "RENN", False, trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(1, "TOMEKLINKS", False,
                             trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(1, "ALLKNN", False,
                             trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(1, "IHT", False,
                             trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(1, "NEARMISS", False,
                             trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(1, "NCR", False,
                             trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(1, "OSS", False,
                             trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(1, "RUS", False,
                             trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(1, "ADASYN", False,
                             trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(
            1, "SMOTE", False, trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(1, "ROS", False,
                             trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(1, "SMOTEENN", False,
                             trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(1, "SMOTETOMEK", False,
                             trainingTestSet[0], trainingTestSet[1])

        UnbalancedLearnModel(
            1, "CNN", True, trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(
            1, "ENN", True, trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(
            1, "RENN", True, trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(1, "TOMEKLINKS", True,
                             trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(1, "ALLKNN", True,
                             trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(1, "IHT", True,
                             trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(1, "NEARMISS", True,
                             trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(1, "NCR", True,
                             trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(1, "OSS", True,
                             trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(1, "RUS", True,
                             trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(
            1, "ADASYN", True, trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(
            1, "SMOTE", True, trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(1, "ROS", True,
                             trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(1, "SMOTEENN", True,
                             trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(1, "SMOTETOMEK", True,
                             trainingTestSet[0], trainingTestSet[1])

        # random forest
        UnbalancedLearnModel(
            2, "CNN", False, trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(
            2, "ENN", False, trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(
            2, "RENN", False, trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(2, "TOMEKLINKS", False,
                             trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(2, "ALLKNN", False,
                             trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(2, "IHT", False,
                             trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(2, "NEARMISS", False,
                             trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(2, "NCR", False,
                             trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(2, "OSS", False,
                             trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(2, "RUS", False,
                             trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(2, "ADASYN", False,
                             trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(
            2, "SMOTE", False, trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(2, "ROS", False,
                             trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(2, "SMOTEENN", False,
                             trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(2, "SMOTETOMEK", False,
                             trainingTestSet[0], trainingTestSet[1])

        UnbalancedLearnModel(
            2, "CNN", True, trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(
            2, "ENN", True, trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(
            2, "RENN", True, trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(2, "TOMEKLINKS", True,
                             trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(2, "ALLKNN", True,
                             trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(2, "IHT", True,
                             trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(2, "NEARMISS", True,
                             trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(2, "NCR", True,
                             trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(2, "OSS", True,
                             trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(2, "RUS", True,
                             trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(
            2, "ADASYN", True, trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(
            2, "SMOTE", True, trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(2, "ROS", True,
                             trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(2, "SMOTEENN", True,
                             trainingTestSet[0], trainingTestSet[1])
        UnbalancedLearnModel(2, "SMOTETOMEK", True,
                             trainingTestSet[0], trainingTestSet[1])

    print("Done!")

# tf + tfidf


def RewriteM1TfHistoricalPerformance(min: int, inc: int, algo: int, trainingSet: [Review], testSet: [Review]):

    Performance_m1.objects.filter(binary=False, algorithm=Algorithm.objects.get(
        algorithmId=algo)).delete()
    incSets = IncrementalTrainingSet(min, inc, trainingSet)

    for reviews in incSets:

        x, y = [], []
        partialFeaturesIndex = GetM1GlobalFeaturesIndex(reviews)

        for review in reviews:

            featuresTf = ExtractFeatureFromCorpusM1(review.review_content)
            x.append(FeaturesTfToGlobal(featuresTf, partialFeaturesIndex))
            y.append(review.tag.tagId)

        transformer = TfidfTransformer(smooth_idf=False)
        tfidf_x = transformer.fit_transform(x).toarray()

        if algo == 1:
            classifier = svm_classifier
        elif algo == 2:
            classifier = rf_classifier

        classifier.fit(tfidf_x, y)

        reviewsPredictions = {}

        for review in testSet:

            partialFeaturesVector = FeaturesTfToGlobal(
                ExtractFeatureFromCorpusM1(review.review_content), partialFeaturesIndex)

            reviewsPredictions[review] = classifier.predict(
                [partialFeaturesVector])[0]

        f1scores = CalculateF1s(reviewsPredictions)

        avg_f1 = round(numpy.mean(
            [f1scores[1], f1scores[2], f1scores[9], f1scores[10], f1scores[13], f1scores[14]]), 3)

        Performance_m1.objects.create(algorithm=Algorithm.objects.get(
            algorithmId=algo), size=len(reviews), binary=False, sa_f1=f1scores[1],
            og_f1=f1scores[2], vr_f1=f1scores[3], sl_f1=f1scores[4], tx_f1=f1scores[5],
            ld_f1=f1scores[6], sp_f1=f1scores[7], ck_f1=f1scores[8], rs_f1=f1scores[9],
            lg_f1=f1scores[10], it_f1=f1scores[11], tr_f1=f1scores[12], pc_f1=f1scores[13],
            ot_f1=f1scores[14], avg_f1=avg_f1)

# binary + tfidf


def RewriteM1BinaryHistoricalPerformance(min: int, inc: int, algo: int, trainingSet: [Review], testSet: [Review]):

    Performance_m1.objects.filter(binary=True, algorithm=Algorithm.objects.get(
        algorithmId=algo)).delete()
    incSets = IncrementalTrainingSet(min, inc, trainingSet)

    for reviews in incSets:

        x, y = [], []
        partialFeaturesIndex = GetM1GlobalFeaturesIndex(reviews)

        for review in reviews:

            featuresTf = ExtractFeatureFromCorpusM1(review.review_content)
            x.append(GetBinaryFromTf(FeaturesTfToGlobal(
                featuresTf, partialFeaturesIndex)))
            y.append(review.tag.tagId)

        transformer = TfidfTransformer(smooth_idf=False)
        tfidf_x = transformer.fit_transform(x).toarray()

        if algo == 1:
            classifier = svm_classifier
        elif algo == 2:
            classifier = rf_classifier

        classifier.fit(tfidf_x, y)

        reviewsPredictions = {}

        for review in testSet:

            partialFeaturesVector = GetBinaryFromTf(FeaturesTfToGlobal(
                ExtractFeatureFromCorpusM1(review.review_content), partialFeaturesIndex))

            reviewsPredictions[review] = classifier.predict(
                [partialFeaturesVector])[0]

        f1scores = CalculateF1s(reviewsPredictions)

        avg_f1 = round(numpy.mean(
            [f1scores[1], f1scores[2], f1scores[9], f1scores[10], f1scores[13], f1scores[14]]), 3)

        Performance_m1.objects.create(algorithm=Algorithm.objects.get(
            algorithmId=algo), size=len(reviews), binary=True, sa_f1=f1scores[1],
            og_f1=f1scores[2], vr_f1=f1scores[3], sl_f1=f1scores[4], tx_f1=f1scores[5],
            ld_f1=f1scores[6], sp_f1=f1scores[7], ck_f1=f1scores[8], rs_f1=f1scores[9],
            lg_f1=f1scores[10], it_f1=f1scores[11], tr_f1=f1scores[12], pc_f1=f1scores[13],
            ot_f1=f1scores[14], avg_f1=avg_f1)

# stemming + tf + tfidf


def RewriteM2TfHistoricalPerformance(min: int, inc: int, algo: int, trainingSet: [Review], testSet: [Review]):

    Performance_m2.objects.filter(binary=False, algorithm=Algorithm.objects.get(
        algorithmId=algo)).delete()
    incSets = IncrementalTrainingSet(min, inc, trainingSet)

    for reviews in incSets:

        x, y = [], []
        partialFeaturesIndex = GetM2GlobalFeaturesIndex(reviews)

        for review in reviews:

            featuresTf = ExtractFeatureFromCorpusM2(review.review_content)
            x.append(FeaturesTfToGlobal(featuresTf, partialFeaturesIndex))
            y.append(review.tag.tagId)

        transformer = TfidfTransformer(smooth_idf=False)
        tfidf_x = transformer.fit_transform(x).toarray()

        if algo == 1:
            classifier = svm_classifier
        elif algo == 2:
            classifier = rf_classifier

        classifier.fit(tfidf_x, y)

        reviewsPredictions = {}

        for review in testSet:

            partialFeaturesVector = FeaturesTfToGlobal(
                ExtractFeatureFromCorpusM2(review.review_content), partialFeaturesIndex)

            reviewsPredictions[review] = classifier.predict(
                [partialFeaturesVector])[0]

        f1scores = CalculateF1s(reviewsPredictions)

        avg_f1 = round(numpy.mean(
            [f1scores[1], f1scores[2], f1scores[9], f1scores[10], f1scores[13], f1scores[14]]), 3)

        Performance_m2.objects.create(algorithm=Algorithm.objects.get(
            algorithmId=algo), size=len(reviews), binary=False, sa_f1=f1scores[1],
            og_f1=f1scores[2], vr_f1=f1scores[3], sl_f1=f1scores[4], tx_f1=f1scores[5],
            ld_f1=f1scores[6], sp_f1=f1scores[7], ck_f1=f1scores[8], rs_f1=f1scores[9],
            lg_f1=f1scores[10], it_f1=f1scores[11], tr_f1=f1scores[12], pc_f1=f1scores[13],
            ot_f1=f1scores[14], avg_f1=avg_f1)

# stemming + binary + tfidf


def RewriteM2BinaryHistoricalPerformance(min: int, inc: int, algo: int, trainingSet: [Review], testSet: [Review]):

    Performance_m2.objects.filter(binary=True, algorithm=Algorithm.objects.get(
        algorithmId=algo)).delete()
    incSets = IncrementalTrainingSet(min, inc, trainingSet)

    for reviews in incSets:

        x, y = [], []
        partialFeaturesIndex = GetM2GlobalFeaturesIndex(reviews)

        for review in reviews:

            featuresTf = ExtractFeatureFromCorpusM2(review.review_content)
            x.append(GetBinaryFromTf(FeaturesTfToGlobal(
                featuresTf, partialFeaturesIndex)))
            y.append(review.tag.tagId)

        transformer = TfidfTransformer(smooth_idf=False)
        tfidf_x = transformer.fit_transform(x).toarray()

        if algo == 1:
            classifier = svm_classifier
        elif algo == 2:
            classifier = rf_classifier

        classifier.fit(tfidf_x, y)

        reviewsPredictions = {}

        for review in testSet:

            partialFeaturesVector = GetBinaryFromTf(FeaturesTfToGlobal(
                ExtractFeatureFromCorpusM2(review.review_content), partialFeaturesIndex))

            reviewsPredictions[review] = classifier.predict(
                [partialFeaturesVector])[0]

        f1scores = CalculateF1s(reviewsPredictions)

        avg_f1 = round(numpy.mean(
            [f1scores[1], f1scores[2], f1scores[9], f1scores[10], f1scores[13], f1scores[14]]), 3)

        Performance_m2.objects.create(algorithm=Algorithm.objects.get(
            algorithmId=algo), size=len(reviews), binary=True, sa_f1=f1scores[1],
            og_f1=f1scores[2], vr_f1=f1scores[3], sl_f1=f1scores[4], tx_f1=f1scores[5],
            ld_f1=f1scores[6], sp_f1=f1scores[7], ck_f1=f1scores[8], rs_f1=f1scores[9],
            lg_f1=f1scores[10], it_f1=f1scores[11], tr_f1=f1scores[12], pc_f1=f1scores[13],
            ot_f1=f1scores[14], avg_f1=avg_f1)

# Stemming + tfidf + cnn (undersampling)


def UnbalancedLearnModel(algo: int, unbalanceLearnTechnique: str, binary: bool, trainingSet: [Review], testSet: [Review]):

    Performance_unbalanced_learn.objects.filter(binary=binary, algorithm=Algorithm.objects.get(
        algorithmId=algo), technique=unbalanceLearnTechnique).delete()

    reviews = trainingSet

    x, y = [], []
    partialFeaturesIndex = GetM2GlobalFeaturesIndex(reviews)

    for review in reviews:

        featuresTf = ExtractFeatureFromCorpusM2(review.review_content)

        if(binary):
            vectors = GetBinaryFromTf(FeaturesTfToGlobal(
                featuresTf, partialFeaturesIndex))
        else:
            vectors = FeaturesTfToGlobal(featuresTf, partialFeaturesIndex)

        x.append(vectors)
        y.append(review.tag.tagId)

    transformer = TfidfTransformer(smooth_idf=False)
    tfidf_x = transformer.fit_transform(x).toarray()

    classifier = None

    if algo == 1:
        classifier = svm_classifier
    elif algo == 2:
        classifier = rf_classifier

    x_res, y_res = None, None

    if unbalanceLearnTechnique == "CNN":

        cnn = CondensedNearestNeighbour(random_state=42)
        x_res, y_res = cnn.fit_sample(tfidf_x, y)

    elif unbalanceLearnTechnique == "ENN":

        enn = EditedNearestNeighbours(random_state=42)
        x_res, y_res = enn.fit_sample(tfidf_x, y)

    elif unbalanceLearnTechnique == "TOMEKLINKS":

        tl = TomekLinks(random_state=42)
        x_res, y_res = tl.fit_sample(tfidf_x, y)

    elif unbalanceLearnTechnique == "RENN":

        renn = RepeatedEditedNearestNeighbours(random_state=42)
        x_res, y_res = renn.fit_sample(tfidf_x, y)

    elif unbalanceLearnTechnique == "ALLKNN":

        allknn = AllKNN(random_state=42)
        x_res, y_res = allknn.fit_sample(tfidf_x, y)

    elif unbalanceLearnTechnique == "IHT":

        iht = InstanceHardnessThreshold(random_state=42)
        x_res, y_res = iht.fit_sample(tfidf_x, y)

    elif unbalanceLearnTechnique == "NEARMISS":

        nm = NearMiss(random_state=42)
        x_res, y_res = nm.fit_sample(tfidf_x, y)

    elif unbalanceLearnTechnique == "NCR":

        ncr = NeighbourhoodCleaningRule(random_state=42)
        x_res, y_res = ncr.fit_sample(tfidf_x, y)

    elif unbalanceLearnTechnique == "OSS":

        oss = OneSidedSelection(random_state=42)
        x_res, y_res = oss.fit_sample(tfidf_x, y)

    elif unbalanceLearnTechnique == "RUS":

        rus = RandomUnderSampler(random_state=42)
        x_res, y_res = rus.fit_sample(tfidf_x, y)

    elif unbalanceLearnTechnique == "ADASYN":

        ada = ADASYN(random_state=42)
        x_res, y_res = ada.fit_sample(tfidf_x, y)

    elif unbalanceLearnTechnique == "SMOTE":

        sm = SMOTE(random_state=42)
        x_res, y_res = sm.fit_sample(tfidf_x, y)

    elif unbalanceLearnTechnique == "ROS":

        ros = RandomOverSampler(random_state=42)
        x_res, y_res = ros.fit_sample(tfidf_x, y)

    elif unbalanceLearnTechnique == "SMOTEENN":

        sme = SMOTEENN(random_state=42)
        x_res, y_res = sme.fit_sample(tfidf_x, y)
    elif unbalanceLearnTechnique == "SMOTETOMEK":

        smt = SMOTETomek(random_state=42)
        x_res, y_res = smt.fit_sample(tfidf_x, y)

    classifier.fit(x_res, y_res)

    reviewsPredictions = {}

    for review in testSet:

        if binary:
            partialFeaturesVector = GetBinaryFromTf(FeaturesTfToGlobal(
                ExtractFeatureFromCorpusM2(review.review_content), partialFeaturesIndex))
        else:
            partialFeaturesVector = FeaturesTfToGlobal(
                ExtractFeatureFromCorpusM2(review.review_content), partialFeaturesIndex)

        reviewsPredictions[review] = classifier.predict(
            [partialFeaturesVector])[0]

    f1scores = CalculateF1s(reviewsPredictions)

    avg_f1 = round(numpy.mean(
        [f1scores[1], f1scores[2], f1scores[9], f1scores[10], f1scores[13], f1scores[14]]), 3)

    Performance_unbalanced_learn.objects.create(algorithm=Algorithm.objects.get(
        algorithmId=algo), size=len(reviews), binary=binary, technique=unbalanceLearnTechnique, sa_f1=f1scores[1],
        og_f1=f1scores[2], vr_f1=f1scores[3], sl_f1=f1scores[4], tx_f1=f1scores[5],
        ld_f1=f1scores[6], sp_f1=f1scores[7], ck_f1=f1scores[8], rs_f1=f1scores[9],
        lg_f1=f1scores[10], it_f1=f1scores[11], tr_f1=f1scores[12], pc_f1=f1scores[13],
        ot_f1=f1scores[14], avg_f1=avg_f1)
