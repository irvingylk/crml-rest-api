from scripts import rfmodel, extract_features
from crml_api.models import *


def run(*args):

    stat = statAnalyze(args[0])

    for i in range(len(stat)):

        try:
            desc = Tag.objects.get(tagId=i).description
        except:
            continue

        print('%s : %d' % (desc, stat[i]))


def statAnalyze(project) -> []:

    stat = [0]*13

    model = rfmodel.classifier()

    if not model:

        return stat

    classifier = model['classifier']
    featuresIndex = model['featuresIndex']

    reviews = Review.objects.filter(project=project)

    for r in reviews:

        if r.reviewed:
            stat[r.tag.tagId] += 1
            continue

        content = r.review_content
        featuresVector = extract_features.extractFeaturesFromCorpus(content)

        if not featuresVector:
            continue

        x = extract_features.featuresVectorToGlobal(
            featuresVector, featuresIndex)

        prediction = classifier.predict([x])[0]

        stat[prediction] += 1

    return stat
