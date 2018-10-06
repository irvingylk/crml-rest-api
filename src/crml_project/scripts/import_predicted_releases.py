import csv
import io
from crml_api.models import Release


def run(*args):

    releases = []

    with open('Release_Prediction_django_1.9.csv', 'rb') as csvfile:

        lines = csvfile.read().decode("utf-8")
        io_string = io.StringIO(lines)
        next(io_string)

        for l in csv.reader(io_string, delimiter=','):
            if len(l):

                releases.append(
                    Release(Project='django/djang0', File=l[0], Prob=l[1], Reason=l[3], Release='v1.9'))

    for i in range(1, len(releases), 500):

        Release.objects.bulk_create(releases[i:i+500])
