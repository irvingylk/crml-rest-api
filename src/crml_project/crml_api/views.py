from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import time


from . import serializers
from . import models

# Create your views here.

class RawCommentItemApiView(APIView):


    def get_object(self, id):

        try:
            print(id)
            return models.RawCommentItem.objects.get(issueCommentId=id)

        except models.RawCommentItem.DoesNotExist:
            return None


    def get(self, request, id, format=None):

        rawCommentObj = self.get_object(id)
        if(rawCommentObj == None):

            return Response({'tag':-1})

        else:

            return Response({'tag':rawCommentObj.tag})

    def post(self, request, format=None):

        serializer = serializers.RawCommentItemSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id, format=None):

        rawCommentObj = self.get_object(id)
        serializer = serializers.RawCommentItemSerializer(rawCommentObj, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id, format=None):

        rawCommentObj = self.get_object(id)

        if rawCommentObj != None:

            rawCommentObj.delete()
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)

class RawCommentItemsApiView(APIView):

    def get(self, request, format=None):

        serializer = serializers.RawCommentItemSerializer(models.RawCommentItem.objects.all(), many=True)

        return Response(serializer.data)