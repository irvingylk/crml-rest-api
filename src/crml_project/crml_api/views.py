from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import HttpResponse
import time


from . import serializers
from . import models

from scripts import extract_features, evaluate_models, rfmodel


# Create your views here.

class ReviewApiView(APIView):


    def get_object(self, id):

        try:
            
            return models.Review.objects.get(reviewId=id)

        except models.Review.DoesNotExist:
            return None


    def get(self, request, id, format=None):

        review = self.get_object(id)

        if(review == None):

            return Response({'tag':-1})

        else:

            return Response({'tag':review.tag.tagId})

    def post(self, request, format=None):

        reviewSerializer = serializers.ReviewSerializer(data=request.data)

        if reviewSerializer.is_valid():

            reviewSerializer.save()


            codeSerializer = serializers.CodeSerializer(data=request.data.get('codes'), many=True)
            if codeSerializer.is_valid():
                codeSerializer.save()

            peopleSerializer = serializers.PeopleSerializer(data=request.data.get('people'), many=True)
            if peopleSerializer.is_valid():
                peopleSerializer.save()

            issueSerializer = serializers.IssueSerializer(data=request.data.get('issues'), many=True)
            if issueSerializer.is_valid():
                issueSerializer.save()
            
            linkSerializer = serializers.LinkSerializer(data=request.data.get('links'), many=True)
            if linkSerializer.is_valid():
                linkSerializer.save()

            imageSerializer = serializers.ImageSerializer(data=request.data.get('images'), many=True)
            if imageSerializer.is_valid():
                imageSerializer.save()
         
            return Response({'res':1}, status=status.HTTP_200_OK)

        return Response({'res':0}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id, format=None):

        review = self.get_object(id)
        serializer = serializers.ReviewSerializer(review, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'res':1},status=status.HTTP_200_OK)

        return Response({'res':0}, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id, format=None):

        review = models.Review.objects.get(reviewId=id)

        if review != None:
            
            review.delete()
            return Response({'res':1},status=status.HTTP_200_OK)

        return Response({'res':0},status=status.HTTP_400_BAD_REQUEST)


def MLModels(request):

    extract_features.extractFeatures()
    result = evaluate_models.evaluateModels()
    tags = list(models.Tag.objects.values_list('description', flat=True))
    
    return render(request, 'models.html', {'result' :result, 'tags':tags})


@api_view(['POST'])
def Predict(request):


    model = rfmodel.classifier()

    if model:

        classifier = model['classifier']
        featuresGlobalIndex = model['featuresIndex']
        featuresVector = extract_features.extractFeaturesFromCorpus('i am use and _reviewer')

        x = extract_features.featuresVectorToGlobal(featuresVector, featuresGlobalIndex)

        y = classifier.predict([x])
        tagPredicted = y[0]
        
        return Response({'res':1,'Tag':tagPredicted}, status=status.HTTP_200_OK)
    
    return Response({'res':0}, status=status.HTTP_400_BAD_REQUEST)

    

    