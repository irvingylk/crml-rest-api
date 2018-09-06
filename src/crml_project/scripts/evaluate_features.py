from crml_api.models import Review
from crml_api.models import Tag
from scripts.extract_features import SnowballStem, RemoveStopWords, Tokenization


def run(*args):

    sa = Tag.objects.get(tagId=1)
    og = Tag.objects.get(tagId=2)
    lg = Tag.objects.get(tagId=10)
    ts = Tag.objects.get(tagId=9)
    pr = Tag.objects.get(tagId=13)
    ot = Tag.objects.get(tagId=14)

    reviews = Review.objects.filter(reviewed=True)

    sa_reviews = reviews.filter(tag=sa)
    og_reviews = reviews.filter(tag=og)
    lg_reviews = reviews.filter(tag=lg)
    ts_reviews = reviews.filter(tag=ts)
    pr_reviews = reviews.filter(tag=pr)
    ot_reviews = reviews.filter(tag=ot)

    sa_li = []
    og_li = []
    lg_li = []
    ts_li = []
    pr_li = []
    ot_li = []

    for sa in sa_reviews:

        sa_li.extend(SnowballStem(RemoveStopWords(
            Tokenization(sa.review_content))))

    sa_li = list(set(sa_li))
    print("SA %i" % len(sa_li))

    for og in og_reviews:

        og_li.extend(SnowballStem(RemoveStopWords(
            Tokenization(og.review_content))))

    og_li = list(set(og_li))
    print("OG %i" % len(og_li))

    for lg in lg_reviews:

        lg_li.extend(SnowballStem(RemoveStopWords(
            Tokenization(lg.review_content))))

    lg_li = list(set(lg_li))
    print("LG %i" % len(lg_li))

    for ts in ts_reviews:

        ts_li.extend(SnowballStem(RemoveStopWords(
            Tokenization(ts.review_content))))

    ts_li = list(set(ts_li))
    print("TS %i" % len(ts_li))

    for pr in pr_reviews:

        pr_li.extend(SnowballStem(RemoveStopWords(
            Tokenization(pr.review_content))))

    pr_li = list(set(pr_li))
    print("PR %i" % len(pr_li))

    for ot in ot_reviews:

        ot_li.extend(SnowballStem(RemoveStopWords(
            Tokenization(ot.review_content))))

    ot_li = list(set(ot_li))
    print("OT %i" % len(ot_li))
