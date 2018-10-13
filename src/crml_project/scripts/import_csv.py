from crml_api.models import PullRequest
import pandas as pd


def run(*args):

    pullrequests = []
    data = pd.read_csv("commits_all.csv")

    for index, columns in data.iterrows():

        r = PullRequest(pr_id=columns[0], pr_time=columns[1], project=columns[2],
                        commit_hash=columns[3], creation_time=columns[4], number=columns[5])
        pullrequests.append(r)

    PullRequest.objects.bulk_create(pullrequests)

    print("Done!")
