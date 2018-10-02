from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


from . import serializers
from . import models

from scripts import extract_features, evaluate_models

from datetime import datetime


# Create your views here.

class DiscussionApiView(APIView):

    def get_object(self, id):

        try:
            discussion = models.Discussion.objects.get(discussion_id=id)
            return discussion

        except models.Discussion.DoesNotExist:
            return None
    '''
    def get(self, request, id, format=None):
        discussion = self.get_object(id)

        if discussion:

            if discussion.reviewed:

                return Response({'type': 'true_value', 'tag': discussion.tag.tag_id})

            if discussion.predicted.tag_id:

                return Response({'type': 'prediction', 'tag': discussion.tag.tagId})

            return Response({'type': 'prediction', 'tag': 4})

            # model = svm_model.GetClassifier()
            # if no predicted, use model to predict

        return Response({'tag': -1})
    '''

    def post(self, request, format=None):

        discussion = self.get_object(request.data['discussion_id'])

        if discussion:

            if discussion.reviewed:

                return Response({'type': 'true_value', 'tag': discussion.tag.tag_id})

            if discussion.predicted:

                return Response({'type': 'prediction', 'tag': discussion.predicted.tag_id})
            else:
                # use model to predict
                # update db
                return Response({'type': 'prediction', 'tag': 4})

        request.data['tag'] = -1
        serializer = serializers.DiscussionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

        '''
        discussion = models.Discussion.objects.get(
            discussion_id=request.data.get('discussion_id'))
        '''
        model = None
        # predicted_tag_id = -1

        if model:
            # use model to predict
            # update db
            return Response({'type': 'prediction', 'tag': 4})

        return Response({'type': 'prediction', 'tag': 4})

    def put(self, request, id, format=None):

        if models.Discussion.objects.filter(discussion_id=id).count() == 0:
            return Response({'res': 0})

        discussion = self.get_object(id)
        tag = models.DiscussionTag.objects.get(tag_id=request.data.get('tag'))

        if not discussion.reviewed:
            discussion.reviewed = True

        if discussion.tag != tag:
            discussion.tag = tag

        discussion.reviewed_time = datetime.now()
        discussion.save()

        return Response({'res': 1})

    def delete(self, request, id, format=None):

        if models.Discussion.objects.filter(discussion_id=id).count() == 1:

            discussion = models.Discussion.objects.get(discussion_id=id)
            unknown = models.DiscussionTag.objects.get(tag_id=-1)
            if discussion.tag != unknown:
                discussion.tag = unknown
                discussion.reviewed = False
                discussion.reviewed_time = None
                discussion.save()

                return Response({'res': 1})

        return Response({'res': 0})


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
