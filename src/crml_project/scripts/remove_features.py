from crml_api.models import *

def run(*args):

    reviews = Review.objects.filter(extracted=True)

    for r in reviews:

        try:
            Training.objects.filter(reviewId=r).delete()
        except:
            print("delete error")


        r.extracted = False
        r.save()