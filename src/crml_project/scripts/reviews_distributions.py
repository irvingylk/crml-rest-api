from crml_api.models import Review, Tag


def run(*args):

    dic = {}

    reviews = Review.objects.filter(reviewed=True)

    total = 0

    for review in reviews:

        label = review.tag.tagId
        if label != -1:

            if label not in dic:

                dic[label] = 1
            else:
                dic[label] += 1

            total += 1

    for label in dic:

        print(("Test" if Tag.objects.get(tagId=label).name == "Resource" else Tag.objects.get(
            tagId=label).name) + " : " + str(dic[label]) +
            " (" + str(round(dic[label]/total * 100, 2)) + "%)")

        print("Total" + str(total))
