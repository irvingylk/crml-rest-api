from crml_api.models import Review
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from .evaluate_models import CalculateF1s
from .extract_features import GetGlobalFeaturesIndex_Temp
from .extract_features import ExtractFeatureFromCorpus
from sklearn.feature_extraction.text import TfidfTransformer
from imblearn.combine import SMOTEENN, SMOTETomek
from sklearn.model_selection import RepeatedKFold, GridSearchCV
import numpy
import pandas as pd
from . import extract_features as ef

from sklearn.metrics import accuracy_score

from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import SGDClassifier, LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
import random


from sklearn.feature_selection import GenericUnivariateSelect
from sklearn.feature_selection import chi2

from sklearn.preprocessing import LabelBinarizer
from sklearn.metrics import roc_curve, precision_recall_curve, auc, make_scorer, recall_score, precision_score, confusion_matrix

svc_with_linear_kernel = svm.SVC(kernel='linear', C=1.0)
linear_svc = svm.LinearSVC(C=1.0)
svc_with_rbf_kernel = svm.SVC(kernel='rbf', gamma=0.7, C=1.0)
svc_with_polynomial = svm.SVC(kernel='poly', degree=3, C=1.0)

svm_classifier = svc_with_linear_kernel
rf_classifier = RandomForestClassifier(
    n_estimators=300, min_samples_split=3, max_depth=25, random_state=0, n_jobs=-1)
sme = SMOTEENN(random_state=42)
smt = SMOTETomek(random_state=42)

gnb_classifier = GaussianNB()
mlpc_classifier = MLPClassifier(
    solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
SGD_classifier = SGDClassifier(loss="hinge", penalty="l2", max_iter=5)
LR_classifier = LogisticRegression(
    random_state=0, solver='lbfgs', multi_class='multinomial')
DT_classifier = DecisionTreeClassifier(random_state=23)
KNN_classifier = KNeighborsClassifier(n_neighbors=3)

percentile_selector = 'percentile'
k_best_selector = 'k_best'
fpr_selector = 'fpr'
fdr_selector = 'fdr'
fwe_selector = 'fwe'


def run(*args):
    print("start")

    # classifier = LR_classifier

    reviews = list(Review.objects.filter(
        reviewed=True).order_by('reviewed_time'))

    print("get reviews done")

    EvaluatePerformance(LR_classifier, ef.E19, reviews,
                        "LR_E19_percentile", percentile_selector, 20)

    # EvaluatePerformance(rf_classifier, ef.E20, reviews,
    #                    "rf_E20_percentile", percentile_selector, 20)
    '''
    EvaluatePerformance(LR_classifier, ef.E19, reviews,
                        "LR_E19_percentile", percentile_selector, 20)
    EvaluatePerformance(svm_classifier, ef.E19, reviews,
                        "svm_E19_percentile", percentile_selector, 20)
    EvaluatePerformance(rf_classifier, ef.E20, reviews,
                        "rf_E20_percentile", percentile_selector, 20)
    EvaluatePerformance(gnb_classifier, ef.E3, reviews,
                        "gnb_E3_percentile", percentile_selector, 20)
    EvaluatePerformance(mlpc_classifier, ef.E19, reviews,
                        "mlpc_E19_percentile", percentile_selector, 20)
    EvaluatePerformance(SGD_classifier, ef.E19, reviews,
                        "sgd_E19_percentile", percentile_selector, 20)
    EvaluatePerformance(DT_classifier, ef.E7, reviews,
                        "dt_E7_percentile", percentile_selector, 20)
    EvaluatePerformance(KNN_classifier, ef.E7, reviews,
                        "knn_E7_percentile", percentile_selector, 20)
    '''
    '''
    random.seed(111)
    random.shuffle(reviews)
    EvaluatePerformance(classifier, ef.E19, reviews[0:150], "140")
    EvaluatePerformance(classifier, ef.E19, reviews[0:170], "170")
    EvaluatePerformance(classifier, ef.E19, reviews[0:190], "190")
    EvaluatePerformance(classifier, ef.E19, reviews[0:210], "210")
    EvaluatePerformance(classifier, ef.E19, reviews[0:230], "230")
    EvaluatePerformance(classifier, ef.E19, reviews[0:250], "250")
    '''

    '''
    EvaluatePerformance(classifier, ef.E1, reviews, "E1")
    EvaluatePerformance(classifier, ef.E2, reviews, "E2")
    EvaluatePerformance(classifier, ef.E3, reviews, "E3")
    EvaluatePerformance(classifier, ef.E4, reviews, "E4")
    EvaluatePerformance(classifier, ef.E5, reviews, "E5")
    EvaluatePerformance(classifier, ef.E6, reviews, "E6")
    EvaluatePerformance(classifier, ef.E7, reviews, "E7")
    EvaluatePerformance(classifier, ef.E8, reviews, "E8")
    EvaluatePerformance(classifier, ef.E9, reviews, "E9")
    EvaluatePerformance(classifier, ef.E10, reviews, "E10")
    EvaluatePerformance(classifier, ef.E11, reviews, "E11")
    EvaluatePerformance(classifier, ef.E12, reviews, "E12")
    EvaluatePerformance(classifier, ef.E13, reviews, "E13")
    EvaluatePerformance(classifier, ef.E14, reviews, "E14")
    EvaluatePerformance(classifier, ef.E15, reviews, "E15")
    EvaluatePerformance(classifier, ef.E16, reviews, "E16")
    EvaluatePerformance(classifier, ef.E17, reviews, "E17")
    EvaluatePerformance(classifier, ef.E18, reviews, "E18")
    EvaluatePerformance(classifier, ef.E19, reviews, "E19")
    EvaluatePerformance(classifier, ef.E20, reviews, "E20")
    EvaluatePerformance(classifier, ef.E21, reviews, "E21")
    EvaluatePerformance(classifier, ef.E22, reviews, "E22")
    EvaluatePerformance(classifier, ef.E23, reviews, "E23")
    EvaluatePerformance(classifier, ef.E24, reviews, "E24")
    '''
    print("Done!")


def EvaluatePerformance(classifier, extractionMethod: str, reviews: [Review], label: str, featuresSelector, selectorParam):

    rkf = RepeatedKFold(n_splits=10, n_repeats=10, random_state=2652124)

    avg_f1s = []
    sa_f1s = []
    og_f1s = []
    ts_f1s = []
    lg_f1s = []
    pc_f1s = []
    ot_f1s = []

    avg_accs = []

    for train_index, test_index in rkf.split(reviews):

        global_features_index = GetGlobalFeaturesIndex_Temp(
            reviews, train_index, extractionMethod)

        x, y = [], []

        for index in train_index:

            featuresVector = ExtractFeatureFromCorpus(
                global_features_index, reviews[index].review_content, extractionMethod)
            addExtraFeatures(featuresVector, reviews[index])
            x.append(featuresVector)
            y.append(reviews[index].tag.tagId)

        transformer = None

        if extractionMethod in ef.USE_TFIDF:
            transformer = TfidfTransformer(smooth_idf=False)
            x = transformer.fit_transform(x, y).toarray().tolist()

        if extractionMethod in ef.USE_SMOTEENN:
            x, y = sme.fit_sample(x, y)
        elif extractionMethod in ef.USE_SMOTETOMEK:
            x, y = smt.fit_sample(x, y)

        selector = GenericUnivariateSelect(
            chi2, featuresSelector, param=selectorParam)
        print(len(x[0]))
        x = selector.fit_transform(x, y)
        print(len(x[0]))

        classifier.fit(x, y)
        reviewsPredictions = {}

        for index in test_index:

            featuresVector = ExtractFeatureFromCorpus(
                global_features_index, reviews[index].review_content, extractionMethod)

            addExtraFeatures(featuresVector, reviews[index])

            if transformer:
                featuresVector = transformer.transform(
                    [featuresVector]).toarray().tolist()[0]

            featuresVector = selector.transform(
                [featuresVector]).tolist()[0]

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

    df.to_csv("model_boxplot_{}.csv".format(label),
              sep=',', encoding='utf-8', index=False)

    overall_data = {'Solution_Approach': [round(numpy.mean(sa_f1s), 3)],
                    'Organization': [round(numpy.mean(og_f1s), 3)],
                    'Test': [round(numpy.mean(ts_f1s), 3)],
                    'Logic': [round(numpy.mean(lg_f1s), 3)],
                    'Process': [round(numpy.mean(pc_f1s), 3)],
                    'Others': [round(numpy.mean(ot_f1s), 3)],
                    'Average': [round(numpy.mean(avg_f1s), 3)],
                    'ACC': [round(numpy.mean(avg_accs), 3)],
                    'Conf': [extractionMethod]}

    df = pd.DataFrame(overall_data, columns=[
                      'Solution_Approach', 'Organization', 'Test', 'Logic', 'Process', 'Others', 'Average', 'ACC', 'Conf'])

    df.to_csv("model_overall_{}.csv".format(label),
              sep=',', encoding='utf-8', index=False)


def addExtraFeatures(X, review: Review):
    '''
    size = review.review_content_length

    X.append(size)

    if review.is_inline_review:

        X.append(1)
    else:

        X.append(0)
    '''
