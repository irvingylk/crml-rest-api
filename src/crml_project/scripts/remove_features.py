from crml_api.models import Review, Training


def run(*args):

    removeFeature()


def removeFeature():

    reviews = Review.objects.filter(extracted=True)
    Training.objects.filter(reviewId__in=reviews).delete()
    reviews.update(extracted=False)