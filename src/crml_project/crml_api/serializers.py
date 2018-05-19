from rest_framework import serializers
from . import models

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Review
        fields = ('reviewId', 'review_content', 'review_content_length','is_inline_review','extracted','reviewed','tag', 'project')

        



class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Tag
        fields = ('tagId', 'description')

class TrainingSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Training
        fields = ('reviewId', 'feature', 'value')

class CodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Code
        fields = ('reviewId', 'code_content')


class PeopleSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.People
        fields = ('reviewId', 'people_content')

class IssueSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Issue
        fields = ('reviewId', 'issue_content')

class LinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.link
        fields = ('reviewId', 'link_content')


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Image
        fields = ('reviewId', 'image_src', 'image_alt')