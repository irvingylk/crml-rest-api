from crml_api.models import Tag, Review, Algorithm


def run(*args):

    Review.objects.all().delete()
    Tag.objects.all().delete()
    Algorithm.objects.all().delete()

    tags = ['Solution Approach', 'Organization', 'Visual Representation', 'Supported by Language', 'Textual',
            'Larger Defects', 'Support', 'Check', 'Resource', 'Logic', 'Interface', 'Traceability', 'Process', 'Others']

    for i in range(len(tags)):

        Tag.objects.create(tagId=i + 1, name=tags[i])

    Tag.objects.create(tagId=-1, name='Unknown')

    algorithms = ['Support Vector Machine']

    for i in range(len(algorithms)):

        Algorithm.objects.create(algorithmId=i + 1, name=algorithms[i])
