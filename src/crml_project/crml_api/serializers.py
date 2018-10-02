from rest_framework import serializers
from . import models


class DiscussionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Discussion
        fields = ('discussion_id', 'pr_id', 'content', 'content_length',
                  'is_inline_discussion', 'tag', 'project', 'creation_time')


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
