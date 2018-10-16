from crml_api.models import Review
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from .evaluate_models import CalculateF1s
from .extract_features import GetGlobalFeaturesIndex
from .extract_features import ExtractFeatureFromCorpus
from sklearn.feature_extraction.text import TfidfTransformer
from imblearn.combine import SMOTEENN, SMOTETomek
from sklearn.model_selection import RepeatedKFold, GridSearchCV, StratifiedKFold
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
from sklearn.metrics import roc_curve, precision_recall_curve, auc, make_scorer, recall_score, precision_score, confusion_matrix, f1_score

svc_with_linear_kernel = svm.SVC(kernel='linear', C=1.0)
linear_svc = svm.LinearSVC(C=1.0)
svc_with_rbf_kernel = svm.SVC(kernel='rbf', gamma=0.7, C=1.0)
svc_with_polynomial = svm.SVC(kernel='poly', degree=3, C=1.0)

svm_classifier = svc_with_linear_kernel
rf_classifier = RandomForestClassifier(n_jobs=-1)
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

rf_param_grid = {
    'min_samples_split': [3, 5, 10],
    'n_estimators': [100, 300],
    'max_depth': [3, 5, 15, 25]
}

lg_param_grid = {

    'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000]
}


scorers = {
    'precision_score': make_scorer(precision_score, average="micro"),
    'recall_score': make_scorer(recall_score, average="micro"),
    'accuracy_score': make_scorer(accuracy_score),
    'f1_score': make_scorer(f1_score, average="micro")
}


def run(*args):
    print("start")

    reviews = list(Review.objects.filter(
        reviewed=True).order_by('reviewed_time'))

    print("get reviews done")

    EvaluatePerformance(LR_classifier, ef.E19, reviews,
                        "LR_E19_percentile", percentile_selector, 20)

    # EvaluatePerformance(rf_classifier, ef.E20, reviews,
    #                    "rf_E20_percentile", percentile_selector, 20)

    print("Done!")


def EvaluatePerformance(classifier, extractionMethod: str, reviews: [Review], label: str, featuresSelector, selectorParam):

    skf = StratifiedKFold(n_splits=10)

    global_features_index = GetGlobalFeaturesIndex(
        reviews, list(range(0, len(reviews))), extractionMethod)

    x, y = [], []

    for review in reviews:

        featuresVector = ExtractFeatureFromCorpus(
            global_features_index, review.review_content, extractionMethod)

        x.append(featuresVector)
        y.append(review.tag.tagId)

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

    x = selector.fit_transform(x, y)

    print("here1")
    grid_search = GridSearchCV(classifier, lg_param_grid, scoring=scorers, refit='accuracy_score',
                               cv=skf, return_train_score=True, n_jobs=-1)
    print("here2")
    grid_search.fit(x, y)
    print("here3")

    # make the predictions
    y_pred = grid_search.predict(x)

    print('Best params for {}'.format('accuracy_score'))
    print(grid_search.best_params_)
