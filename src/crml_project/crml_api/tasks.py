from __future__ import absolute_import, unicode_literals
from celery import shared_task, task
# from .models import Review, Performance, Training, Tag
# from django.db.models import Max
# from scripts import extract_features, svm_model
# from decimal import Decimal
# from datetime import datetime

TRAININGS_INCREMENT = 3

'''
class Monitor:
    Training_Review_Changed = False
    Periodic_Task_Exe_Count = 0
'''


@shared_task
def NoticeReviewed(reviewId: str, tagId: int):
    pass
    '''
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
    '''


@shared_task
def NoticeRemove(reviewId: str):
    pass
    '''
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
    '''


@task
def UpdateClassifier():
    pass
    '''
    if Monitor.Training_Review_Changed:
        svm_model.CacheClassifier()
        Monitor.Training_Review_Changed = False
    '''


@task
def RefreshClassifierHistoricalPerformance():
    pass
    '''
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
    '''


'''
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
