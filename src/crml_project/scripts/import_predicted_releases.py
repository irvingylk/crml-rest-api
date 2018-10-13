import pandas as pd
from crml_api.models import Release


def run(*args):

    releases = []
    version = "2.0"
    data = pd.read_csv("release_v{}.csv".format(version))

    for index, row in data.iterrows():

        r = Release(Project=row['project'], File=row['FileName'], Prob=row['Prob'], Reason=row['Lime'], Release=row['Release'],
                    Date=row['release_time'][:10], COMM=row['COMM'], ADEV=row['ADEV'], DDEV=row['DDEV'], ADD=row['ADD'], DEL=row['DEL'])
        releases.append(r)

    for i in range(1, len(releases), 500):

        Release.objects.bulk_create(releases[i:i+500])
