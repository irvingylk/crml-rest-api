from rest_framework import serializers
from . import models

class RawCommentItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.RawCommentItem
        fields = ('id','issueCommentId', 'rawCommentText', 'tag')
