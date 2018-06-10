from crml_api.models import *


def run(*args):


    tags = ['Solution Approach', 'Organization', 'Visual Representation', 'Supported by Language', 'Textual', 'Larger Defects', 'Support', 'Check', 'Resource', 'Logic', 'Interface', 'Traceability', 'Process', 'Others']

    for i in range(len(tags)):

        try:
            Tag.objects.create(tagId=i+1, description=tags[i])
        except:
            print('error%d'%(i+1))

    Tag.objects.create(tagId=-1, description='Unknown')