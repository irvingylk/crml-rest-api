from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


from . import serializers
from . import models
from .tasks import NoticeReviewed, NoticeRemove

from scripts import extract_features, evaluate_models, svm_model


# Create your views here.

class ReviewApiView(APIView):

    def get_object(self, id):

        try:
            review = models.Review.objects.get(reviewId=id)
            return review

        except models.Review.DoesNotExist:
            return None

    def get(self, request, id, format=None):
        review = self.get_object(id)

        if review:

            if review.reviewed:

                return Response({'type': 'true_value', 'tag': review.tag.tagId})

            model = svm_model.GetClassifier()

            if model and review.trainings_size < model[svm_model.TRAININGS_SIZE_POSITION]:

                return Response({'tag': -1})

            return Response({'type': 'prediction', 'tag': review.tag.tagId})

        return Response({'tag': -1})

    def put(self, request, id, format=None):

        if models.Review.objects.filter(reviewId=id).count() == 0:
            return Response({'res': 0}, status=status.HTTP_400_BAD_REQUEST)

        NoticeReviewed.delay(reviewId=id, tagId=request.data.get('tag'))
        return Response({'res': 1}, status=status.HTTP_200_OK)

    def delete(self, request, id, format=None):

        if models.Review.objects.filter(reviewId=id).count() == 1:

            NoticeRemove.delay(reviewId=id)
            return Response({'res': 1}, status=status.HTTP_200_OK)

        return Response({'res': 0}, status=status.HTTP_400_BAD_REQUEST)


def MLModels(request):

    extract_features.extractFeatures()
    result = evaluate_models.evaluateModels()
    tags = list(models.Tag.objects.values_list('description', flat=True))

    return render(request, 'models.html', {'result': result, 'tags': tags})


def ReviewsStatAnalysis(request):

    return None


@api_view(['GET'])
def ModelsEvolution(request):

    evolutions = evaluate_models.ModelsEvolutions()

    return Response(evolutions, status=status.HTTP_200_OK)


@api_view(['POST'])
def Predict(request):

    save(request)

    try:
        review = models.Review.objects.get(
            reviewId=request.data.get('reviewId'))
    except:
        review = None

    tag = None

    if review:
        tag = svm_model.MakePrediction(review)

    if tag:

        if tag[1]:
            review.trainings_size = tag[1]
            review.predicted = models.Tag.objects.get(tagId=tag[0])
            review.save()

        return Response({'res': 1, 'tag': tag[0]}, status=status.HTTP_200_OK)
    return Response({'res': 0}, status=status.HTTP_400_BAD_REQUEST)


def save(request):

    if models.Review.objects.filter(reviewId=request.data.get('reviewId')).count() == 1:
        return

    request.data['tag'] = -1

    reviewSerializer = serializers.ReviewSerializer(data=request.data)

    if reviewSerializer.is_valid():

        reviewSerializer.save()

        codeSerializer = serializers.CodeSerializer(
            data=request.data.get('codes'), many=True)
        if codeSerializer.is_valid():
            codeSerializer.save()

        peopleSerializer = serializers.PeopleSerializer(
            data=request.data.get('people'), many=True)
        if peopleSerializer.is_valid():
            peopleSerializer.save()

        issueSerializer = serializers.IssueSerializer(
            data=request.data.get('issues'), many=True)
        if issueSerializer.is_valid():
            issueSerializer.save()

        linkSerializer = serializers.LinkSerializer(
            data=request.data.get('links'), many=True)
        if linkSerializer.is_valid():
            linkSerializer.save()

        imageSerializer = serializers.ImageSerializer(
            data=request.data.get('images'), many=True)
        if imageSerializer.is_valid():
            imageSerializer.save()
