from crml_api.models import *

def run(*args):

    Review.objects.all().delete()
