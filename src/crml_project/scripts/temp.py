from crml_api.models import PullRequest, Discussion
from django_app.models import ReviewComment, Pr
from django_bulk_update.helper import bulk_update
from crml_api.models import Release as CRelease
from django_app.models import Release as DRelease
from crml_api.models import Commit as CCommit
from django_app.models import Commit as DCommit
import random
import pandas as pd


def run(*args):

    reviews = ReviewComment.objects.all()
    print(len(reviews))
    prIds = list(set([d['pr']
                      for d in reviews.values('pr')]))
    print(len(prIds))
    prs = PullRequest.objects.filter(number__in=prIds)
    print(len(prs))
    hashs = list(set([d.commit_hash for d in prs]))
    print(len(hashs))

    raw_data = {'commit_hash': hashs}
    df = pd.DataFrame(raw_data, columns=['commit_hash'])
    df.to_csv("request_commits.csv", sep=',', encoding='utf-8', index=False)

    '''
    reviews = ReviewComment.objects.all()
    prIds = list(set([d['pr']
                      for d in reviews.values('pr')]))
    commits = DCommit.objects.all()

    for c in commits:

        i = random.randint(0, len(prIds)-1)
        c.PR = prIds[i]

    bulk_update(commits)
    '''

    # DCommit.objects.all().update(Project="django/django")
    '''
    ccs = CCommit.objects.exclude(pr=None)
    DCommit.objects.all().delete()

    cs = []

    for cc in ccs:

        cs.append(DCommit(Project=cc.project, PR=cc.pr, CommitHash=cc.commit_hash,
                          Prob=cc.prob, Reason=cc.lime, Date=cc.date))

    DCommit.objects.bulk_create(cs)
    '''
    '''
    crs = CRelease.objects.all()
    DRelease.objects.all().delete()

    rs = []

    for cr in crs:

        rs.append(DRelease(Project=cr.Project, File=cr.File, Prob=cr.Prob, Reason=cr.Reason,
                           Release=cr.Release, Date=cr.Date, COMM=cr.COMM, ADEV=cr.ADEV, ADD=cr.ADD, DEL=cr.DEL, DDEV=cr.DDEV))

    DRelease.objects.bulk_create(rs)
    '''

    '''
    cds = Discussion.objects.filter(reviewed=True)
    ReviewComment.objects.all().delete()

    ds = []
    for cd in cds:

        ds.append(ReviewComment(project=cd.project, pr=cd.pr_number,
                                commentid=cd.discussion_id, reviewmsg=cd.content,
                                reviewtag=cd.tag_desc, date=str(cd.pr_time)[:10]))

    ReviewComment.objects.bulk_create(ds)
    '''

    '''
    cPrs = PullRequest.objects.all()

    prs = []
    for cpr in cPrs:

        prs.append(Pr(project=cpr.project, pr=cpr.number,
                      commithash=cpr.commit_hash, date=str(cpr.pr_time)[:10]))

    Pr.objects.bulk_create(prs)
    '''

    '''
    prs = PullRequest.objects.all()
    commit_hashs = [d["commit_hash"] for d in prs.values("commit_hash")]

    commits = Commit.objects.filter(commit_hash__in=commit_hashs)

    for c in commits:

        pr = prs.filter(commit_hash=c.commit_hash)[0]

        c.pr = pr.number
        c.date = pr.creation_time.date()

    bulk_update(commits)
    '''
    '''
    ds = Discussion.objects.all()
    ids = [d["pr_id"] for d in ds.values("pr_id")]
    prs = PullRequest.objects.filter(pr_id__in=ids)

    for d in ds:

        pr = prs.filter(pr_id=d.pr_id)[0]
        d.pr_number = pr.number
        d.pr_time = pr.pr_time

        tag = d.tag.tag_id

        if tag == 1:

            d.tag_desc = "Solution Approach"

        elif tag == 2:

            d.tag_desc = "Organization"

        elif tag == 3:

            d.tag_desc = "Logic"

        elif tag == 4:

            d.tag_desc = "Test"

        elif tag == 5:

            d.tag_desc = "Process"

        elif tag == 6:

            d.tag_desc = "Others"

    bulk_update(ds)
    '''
    '''
    prs = PullRequest.objects.all()
    commit_hashs = [d["commit_hash"] for d in prs.values("commit_hash")]

    print("Commits_in_PRs: {}".format(len(commit_hashs)))

    commits = Commit.objects.filter(commit_hash__in=commit_hashs)

    print("Predicted_Commits_PRs: {}".format(len(commits)))

    cs = Commit.objects.exclude(pr=None)

    print("cs: {}".format(len(cs)))
    '''

    print("Done!")
