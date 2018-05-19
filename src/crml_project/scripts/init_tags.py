from crml_api.models import *


def run(*args):


    tags = ['Check', 'Solution Approach', 'Organization', 'Support By Language', 'Textual', 'Larger Defects', 'Support', 'Resource', 'Logic', 'Interface', 'Traceability', 'Process']

    for i in range(len(tags)):

        try:
            Tag.objects.create(tagId=i+1, description=tags[i])
        except:
            print('error%d'%(i+1))

    Tag.objects.create(tagId=-1, description='Unknown')