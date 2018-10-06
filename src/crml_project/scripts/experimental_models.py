from crml_api.models import Review
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from .evaluate_models import CalculateF1s
from .extract_features import GetGlobalFeaturesIndex
from .extract_features import ExtractFeatureFromCorpus
from sklearn.feature_extraction.text import TfidfTransformer
from imblearn.combine import SMOTEENN, SMOTETomek
from sklearn.cross_validation import ShuffleSplit
import numpy
import pandas as pd
from . import extract_features as ef
import random

from sklearn.metrics import accuracy_score


svc_with_linear_kernel = svm.SVC(kernel='linear', C=1.0)
linear_svc = svm.LinearSVC(C=1.0)
svc_with_rbf_kernel = svm.SVC(kernel='rbf', gamma=0.7, C=1.0)
svc_with_polynomial = svm.SVC(kernel='poly', degree=3, C=1.0)

svm_classifier = svc_with_linear_kernel
rf_classifier = RandomForestClassifier(max_depth=40, random_state=0)
sme = SMOTEENN(random_state=42)
smt = SMOTETomek(random_state=42)

SVM = "support vector machine"
RF = "random forest"


def run(*args):
    print("start")

    reviews = list(Review.objects.filter(
        reviewed=True).order_by('reviewed_time'))

    random.seed(0)
    # random.shuffle(reviews)

    # reviews = reviews[:249]

    print("get reviews done")

    EvaluatePerformance(SVM, ef.E5, reviews)

    print("Done!")


def EvaluatePerformance(algo: str, extractionMethod: str, reviews: [Review]):

    review_size = len(reviews)
    rs = ShuffleSplit(n=review_size, n_iter=100, test_size=0.4, random_state=0)
    classifier = None

    if algo == SVM:
        classifier = svm_classifier
    elif algo == RF:
        classifier = rf_classifier

    if classifier is None:
        return

    avg_f1s = []
    sa_f1s = []
    og_f1s = []
    ts_f1s = []
    lg_f1s = []
    pc_f1s = []
    ot_f1s = []

    avg_accs = []

    for train_index, test_index in rs:

        global_features_index = GetGlobalFeaturesIndex(
            reviews, train_index, extractionMethod)

        x, y = [], []

        for index in train_index:

            featuresVector = ExtractFeatureFromCorpus(
                global_features_index, reviews[index].review_content, extractionMethod)
            x.append(featuresVector)
            y.append(reviews[index].tag.tagId)

        if extractionMethod in ef.USE_TFIDF:
            x = TfidfTransformer(smooth_idf=False).fit_transform(
                x).toarray().tolist()

        if extractionMethod in ef.USE_SMOTEENN:
            x, y = sme.fit_sample(x, y)
        elif extractionMethod in ef.USE_SMOTETOMEK:
            x, y = smt.fit_sample(x, y)

        classifier.fit(x, y)
        reviewsPredictions = {}

        for index in test_index:

            featuresVector = ExtractFeatureFromCorpus(
                global_features_index, reviews[index].review_content, extractionMethod)
            reviewsPredictions[reviews[index]] = classifier.predict([featuresVector])[
                0]

        y_true = []
        y_pred = []
        for review in reviewsPredictions:

            y_true.append(review.tag.tagId)
            y_pred.append(reviewsPredictions[review])

        f1scores = CalculateF1s(reviewsPredictions)
        sa_f1s.append(f1scores[1])
        og_f1s.append(f1scores[2])
        ts_f1s.append(f1scores[9])
        lg_f1s.append(f1scores[10])
        pc_f1s.append(f1scores[13])
        ot_f1s.append(f1scores[14])
        avg_f1 = round(numpy.mean(
            [f1scores[1], f1scores[2], f1scores[9], f1scores[10], f1scores[13], f1scores[14]]), 3)

        avg_f1s.append(avg_f1)

        avg_accs.append(accuracy_score(y_true, y_pred))

    boxplot_data = {'Solution_Approach': sa_f1s,
                    'Organization': og_f1s,
                    'Test': ts_f1s,
                    'Logic': lg_f1s,
                    'Process': pc_f1s,
                    'Others': ot_f1s,
                    'Average': avg_f1s}

    df = pd.DataFrame(boxplot_data, columns=[
                      'Solution_Approach', 'Organization', 'Test', 'Logic', 'Process', 'Others', 'Average'])

    df.to_csv("model_boxplot.csv", sep=',', encoding='utf-8', index=False)

    overall_data = {'Solution_Approach': [round(numpy.mean(sa_f1s), 3)],
                    'Organization': [round(numpy.mean(og_f1s), 3)],
                    'Test': [round(numpy.mean(ts_f1s), 3)],
                    'Logic': [round(numpy.mean(lg_f1s), 3)],
                    'Process': [round(numpy.mean(pc_f1s), 3)],
                    'Others': [round(numpy.mean(ot_f1s), 3)],
                    'Average': [round(numpy.mean(avg_f1s), 3)]}

    df = pd.DataFrame(overall_data, columns=[
                      'Solution_Approach', 'Organization', 'Test', 'Logic', 'Process', 'Others', 'Average'])

    df.to_csv("model_overall.csv", sep=',', encoding='utf-8', index=False)

    print(numpy.mean(avg_accs))
