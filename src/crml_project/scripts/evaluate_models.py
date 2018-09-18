

def CalculateF1s(predictions: dict) -> dict:

    labels = {
        1: [],
        2: [],
        3: [],
        4: [],
        5: [],
        6: [],
        7: [],
        8: [],
        9: [],
        10: [],
        11: [],
        12: [],
        13: [],
        14: []
    }

    for review in predictions:

        trueValue = int(review.tag.tagId)
        predictedAs = int(predictions[review])

        for label in labels:

            if predictedAs == label == trueValue:
                labels[label].append(2)
            elif predictedAs == label != trueValue:
                labels[label].append(1)
            elif predictedAs != label == trueValue:
                labels[label].append(-1)
            elif predictedAs != label != trueValue:
                labels[label].append(0)
            else:
                print("Bug")

    f1scores = {}

    for label in labels:

        temp = labels[label]
        truePositive = 0
        falsePositive = 0
        falseNegative = 0

        for v in temp:

            if v == 2:
                truePositive += 1
            elif v == 1:
                falsePositive += 1
            elif v == -1:
                falseNegative + 1

        precision = truePositive / \
            (truePositive+falsePositive) if truePositive != 0 else 0
        recall = truePositive / \
            (truePositive+falseNegative) if truePositive != 0 else 0

        temp2 = precision + recall
        f1score = (2*precision*recall)/(precision+recall) if temp2 != 0 else 0

        f1scores[label] = round(f1score, 3)

    return f1scores


def GetFalsePositionAndFalseNegative(predictions: dict) -> dict:

    badPredictedReviews = {}

    for review in predictions:

        trueValue = int(review.tag.tagId)
        predictedAs = int(predictions[review])

        if trueValue != predictedAs:

            badPredictedReviews[review.reviewId] = predictedAs

    return badPredictedReviews
