from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from crml_api.models import *
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.metrics import f1_score
import numpy as np
from random import shuffle


def run(*args):
    evaluateModels()

def evaluateModels():
    
    evalResult = {}

    evalResult['msg'] = ''
    evalResult['numReviews'] = 0
    evalResult['numFeatures'] = 0
    evalResult['svmAcc'] = 0
    evalResult['rfAcc'] = 0
    evalResult['svmF1s'] = []
    evalResult['rfF1s'] = []
    evalResult['svmF1sMean'] = 0
    evalResult['rfF1sMean'] = 0

    CONST_FOLDS = 5

    features = Training.objects.values('feature').distinct()
    reviews = Review.objects.filter(extracted=True)

    if len(reviews) < CONST_FOLDS:

        evalResult['msg'] = 'Too less or no extracted review in DB!'

        return evalResult

    dic = {}
    for i in range(len(features)):
        dic[features[i]['feature']] = i
    
    x, y, xy = [], [], []
    
    for r in reviews:
        rsfs = Training.objects.filter(reviewId=r)
        n = [0] * len(features)
        
        for rf in rsfs:
            index = dic[rf.feature]
            n[index] = float(rf.value)
        
        x.append(n)
        y.append(r.tag.tagId)

    for i in range(len(y)):
        xy.append([x[i], y[i]])

    shuffle(xy)

    x, y = [], []

    for i in range(len(xy)):
        x.append(xy[i][0])
        y.append(xy[i][1])

    evalResult['numReviews'] = len(y)
    evalResult['numFeatures'] = len(features)
    print('\nNumber of features : %d'%(len(features)))
    print('\nNumber of reviews : %d'%(len(y)))

    svmModel = svm.SVC(decision_function_shape='ovo')
    svmScores = cross_val_score(svmModel, x, y, cv=CONST_FOLDS, scoring='accuracy')
    print("\nSVM :")
    print('Accuracy : %.3f'%(svmScores.mean()))

    rfModel = RandomForestClassifier()
    rfScores = cross_val_score(rfModel, x, y, cv=CONST_FOLDS, scoring='accuracy')
    print("\nRandom Forest :")
    print('Accuracy : %.3f'%(rfScores.mean()))

    evalResult['svmAcc'] = round(svmScores.mean(), 3)
    evalResult['rfAcc'] = round(rfScores.mean(), 3)


    xSplit = np.array_split(x, CONST_FOLDS)
    ySplit = np.array_split(y, CONST_FOLDS)
    f1RFAverage = np.zeros(12)
    f1SVMAverage = np.zeros(12)

    for i in range(CONST_FOLDS):

        xTest = xSplit[i]
        yTest = ySplit[i]
        xTrain, yTrain  = [], []

        for i2 in range(CONST_FOLDS):

            if i2 != i:

                xTrain += xSplit[i2].tolist()
                yTrain += ySplit[i2].tolist()
        
        rfModel.fit(xTrain, yTrain)
        yPred = rfModel.predict(xTest)
        f1Tags = f1_score(yTest, yPred, labels=[1,2,3,4,5,6,7,8,9,10,11,12], average=None)
        f1RFAverage += f1Tags

        svmModel.fit(xTrain, yTrain)
        yPred = svmModel.predict(xTest)
        f1Tags = f1_score(yTest, yPred, labels=[1,2,3,4,5,6,7,8,9,10,11,12], average=None)
        f1SVMAverage += f1Tags
        

    f1SVMAverage /= CONST_FOLDS
    print("\nSVM:\nF1 of every class:")
    print(f1SVMAverage)
    print('\nAverage f1 :%.3f'%(f1SVMAverage.mean()))

    f1RFAverage /= CONST_FOLDS
    print("\nRandom Forest:\nF1 of every class:")
    print(f1RFAverage)
    print('\nAverage f1 :%.3f'%(f1RFAverage.mean()))

    evalResult['svmF1s'] = f1SVMAverage.round(decimals=3).tolist()
    evalResult['rfF1s'] = f1RFAverage.round(decimals=3).tolist()
    evalResult['svmF1sMean'] = round(f1SVMAverage.mean(), 3)
    evalResult['rfF1sMean'] = round(f1RFAverage.mean(), 3)

    evalResult['msg'] = 'Success'


    return evalResult






