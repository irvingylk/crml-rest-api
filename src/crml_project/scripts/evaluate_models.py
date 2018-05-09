from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from crml_api.models import *
from sklearn.model_selection import cross_val_score


def run(*args):
    features = Training.objects.values('feature').distinct()
    reviews = Review.objects.all()
    dic = {}
    for i in range(len(features)):
        dic[features[i]['feature']] = i
    
    x = []
    y = []
    
    for r in reviews:
        rsfs = Training.objects.filter(reviewId=r)
        n = [0] * len(features)
        
        for rf in rsfs:
            index = dic[rf.feature]
            n[index] = int(rf.value)
        
        x.append(n)
        y.append(r.tag.tagId)

    svmModel = svm.SVC(decision_function_shape='ovo')
    svmModel.fit(x,y)
    scores = cross_val_score(svmModel, x, y, cv=2, scoring='f1_micro')
    print("\nSVM :")
    print(svmModel)
    print('F1 : %.3f'%(scores.mean()))

    rfModel = RandomForestClassifier()
    rfModel.fit(x,y)
    scores = cross_val_score(rfModel, x, y, cv=2, scoring='f1_micro')

    print("\nRandom Forest :")
    print(rfModel)
    print('F1 : %.3f'%(scores.mean()))

