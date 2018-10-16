from __future__ import absolute_import, unicode_literals
from celery import task
# from .models import Review, Performance, Training, Tag
# from django.db.models import Max
# from scripts import extract_features, svm_model
# from decimal import Decimal
# from datetime import datetime
from pymemcache.client.base import Client
import pickle
from crml_api.models import Discussion, Performance
from sklearn.linear_model import LogisticRegression
import scripts.extract_features as ef
from imblearn.combine import SMOTETomek
from sklearn.feature_selection import GenericUnivariateSelect
from sklearn.feature_selection import chi2
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

TRAININGS_INCREMENT = 3
STARTING_SIZE = 140


@task()
def UpdateClassifier():
    print("Update Classifier")

    clf = LogisticRegression(
        random_state=0, solver='lbfgs', multi_class='multinomial')
    smt = SMOTETomek(random_state=42)

    discussions = list(Discussion.objects.filter(reviewed=True))
    globalFeaturesIndex = ef.GetGlobalFeaturesIndex(
        discussions, list(range(0, len(discussions))), ef.E19)

    X, y = [], []
    for discussion in discussions:
        featureVector = ef.ExtractFeatureFromCorpus(
            globalFeaturesIndex, discussion.content, ef.E19)
        X.append(featureVector)
        y.append(discussion.tag.tag_id)

    X, y = smt.fit_sample(X, y)
    selector = GenericUnivariateSelect(chi2, 'percentile', param=20)
    X = selector.fit_transform(X, y)

    try:
        clf.fit(X, y)
        print("fit done")
        client = Client(('localhost', 11211))
        model = (clf, globalFeaturesIndex, selector)
        client.set('model', pickle.dumps(model))
        model_in_bytes = client.get('model')
        model_from_cache = pickle.loads(model_in_bytes)
        print(len(model_from_cache))
    except:
        print("clf failed to cache...")


@task()
def UpdatePerformances():

    print("Update Performance!!")
    clf = LogisticRegression(
        random_state=0, solver='lbfgs', multi_class='multinomial')
    smt = SMOTETomek(random_state=42)

    discussions = Discussion.objects.filter(reviewed=True)
    projects = discussions.values('project').distinct()

    for project in projects:

        name = project['project']

        discussions_in_project = discussions.filter(
            project=name).order_by('reviewed_time')
        size = len(discussions_in_project)

        if size < STARTING_SIZE:
            continue

        performances = Performance.objects.filter(project=name)

        new_performances = []

        for i in range(STARTING_SIZE, size, 20):

            globalFeaturesIndex = ef.GetGlobalFeaturesIndex(
                discussions_in_project, list(range(0, i)), ef.E19)

            X, y = [], []
            for discussion in discussions_in_project:
                featureVector = ef.ExtractFeatureFromCorpus(
                    globalFeaturesIndex, discussion.content, ef.E19)
                X.append(featureVector)
                y.append(discussion.tag.tag_id)

            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.10, random_state=42)

            X_train, y_train = smt.fit_sample(X_train, y_train)
            selector = GenericUnivariateSelect(chi2, 'percentile', param=20)
            X_train = selector.fit_transform(X_train, y_train)
            clf.fit(X_train, y_train)
            X_test = selector.transform(X_test)
            y_pred = clf.predict(X_test)
            acc = accuracy_score(y_test, y_pred)

            new_performances.append(Performance(
                training_size=i, project=name, acc=acc))

        performances.delete()
        Performance.objects.bulk_create(new_performances)

    print("Done Update Performance!!")


'''
@shared_task
def NoticeReviewed(reviewId: str, tagId: int):
    pass
    
    review = Review.objects.get(reviewId=reviewId)
    tag = Tag.objects.get(tagId=tagId)

    changed = False

    if not review.reviewed:
        review.reviewed = True
        review.reviewed_time = datetime.now()
        changed = True

    if review.tag != tag:
        review.tag = tag
        changed = True

    if not changed:
        return

    review.save()

    if not review.extracted:
        featuresTf = extract_features.ExtractFeatureFromCorpusM1(review.review_content)
        review.extracted = True
        review.save()

        if featuresTf:

            for key in featuresTf:

                try:
                    Training.objects.create(
                        reviewId=review, feature=key, value=Decimal(featuresTf[key]))
                except:
                    continue

    Monitor.Training_Review_Changed = True
    print("Notice Reviewed Executed")
    


@shared_task
def NoticeRemove(reviewId: str):
    pass
    
    review = Review.objects.get(reviewId=reviewId)

    unknown_tag = Tag.objects.get(tagId=-1)

    if review.tag == unknown_tag:
        return

    review.tag = unknown_tag
    review.reviewed = False
    review.reviewed_time = None

    if review.extracted:

        Training.objects.filter(reviewId=review).delete()
        review.extracted = False

    review.save()

    Monitor.Training_Review_Changed = True
    print("Notice Remove Executed")
    


@task
def RefreshClassifierHistoricalPerformance():
    pass
    
    extracted_reviews = Review.objects.filter(extracted=True)
    size = extracted_reviews.count()
    ordered_extracted_reviews = extracted_reviews.order_by('reviewed_time')

    for i in range(2, size + 1):

        partial_reviews_list = list(ordered_extracted_reviews[:i])
        model = svm_model.GetClassifierWithSpecificReviews(
            partial_reviews_list)
        acc = 0

        if model:

            positive = 0
            classifier = model[0]
            global_features_index = model[1]

            for r in partial_reviews_list:

                features_vector = extract_features.GetFeaturesVector(r)
                global_features_vector = extract_features.FeaturesVectorToGlobal(
                    features_vector, global_features_index)
                prediction = classifier.predict([global_features_vector])
                predicted_tag = Tag.objects.get(tagId=prediction[0])

                if i == size:
                    r.predicted = predicted_tag
                    r.trainings_size = size
                    r.save()

                if r.tag == predicted_tag:
                    positive += 1

            acc = round(positive / i, 3)

        try:
            p = Performance.objects.get(size=i)
            p.accuracy = acc
            p.save()
        except Performance.DoesNotExist:
            Performance.objects.create(algorithm=Algorithm.objects.get(
                algorithmId=1), size=i, accuracy=acc)

    Monitor.Periodic_Task_Exe_Count += 1

    print("Periodic Task Execute %i" % (Monitor.Periodic_Task_Exe_Count))
    



def UpdateClassifier():

    new_reviews = Review.objects.filter(reviewed=True, extracted=False)
    new_reviews_count = new_reviews.count()

    if new_reviews_count >= TRAININGS_INCREMENT:

        ten_new_reviews = new_reviews.order_by(
            'reviewed_time')[:TRAININGS_INCREMENT]

        for r in ten_new_reviews:

            featuresTf = extract_features.extractFeaturesFromCorpus(
                r.review_content)
            r.extracted = True
            r.save()

            if featuresTf is None:
                continue

            for key in featuresTf:

                try:
                    Training.objects.create(
                        reviewId=r, feature=key, value=Decimal(featuresTf[key].item()))
                except:
                    continue

        svm_model.CacheClassifier()

        extracted_reviews = Review.objects.filter(extracted=True)
        new_max_size = extracted_reviews.count()
        positive = 0

        # comment
        max_size_in_performances = Performance.objects.all().aggregate(Max('size'))[
            'size__max']

        if max_size_in_performances is None:
            max_size_in_performances = 0

        new_max_size = max_size_in_performances + TRAININGS_INCREMENT
        # comment

        for i in range(new_max_size):

            review = extracted_reviews[i]
            prediction = svm_model.MakePrediction(review)

            if prediction:
                prediction_tag = Tag.objects.get(tagId=prediction[0])
                review.predicted = prediction_tag
                review.training_size = prediction[1]
                review.save()

            if review.tag == review.predicted:
                positive += 1

        num_reviews = len(extracted_reviews)
        acc = round(positive / num_reviews, 3)

        Performance.objects.create(algorithm=Algorithm.objects.get(
            algorithmId=1), size=new_max_size, accuracy=acc)
'''
