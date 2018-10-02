from crml_api.models import PullRequest
import csv
import io


def run(*args):

    pullrequests = []
    with open('commits.csv', 'rb') as csvfile:
        data_set = csvfile.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)

        for columns in csv.reader(io_string, delimiter=','):

            pullrequests.append(PullRequest(
                pr_id=columns[0], project=columns[1], commit_hash=columns[2], creation_time=columns[3]))

    PullRequest.objects.all().delete()
    PullRequest.objects.bulk_create(pullrequests)
