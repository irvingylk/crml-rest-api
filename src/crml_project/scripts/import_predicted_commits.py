import csv
import io
from crml_api.models import Commit


def run(*args):

    commits = []

    with open('Change_prediction_all.csv', 'rb') as csvfile:

        lines = csvfile.read().decode("utf-8")
        io_string = io.StringIO(lines)
        next(io_string)

        for l in csv.reader(io_string, delimiter=','):
            if len(l):

                commits.append(
                    Commit(commit_hash=l[0], prob=float(l[1]), predict_as=l[2], lime=l[3]))

    Commit.objects.all().delete()

    for i in range(1, len(commits), 500):
        
        Commit.objects.bulk_create(commits[i:i+500])
