from django.db import models

# Create your models here.

class Tag(models.Model):

    tagId = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=50)

    def __str__(self):

        return self.description


class Review(models.Model):

    reviewId = models.CharField(max_length=50, primary_key=True)
    review_content = models.CharField(max_length=5000)
    review_content_length = models.IntegerField()
    is_inline_review = models.BooleanField(default=False)
    extracted = models.BooleanField(default=False)

    def __str_(self):

        return self.reviewId

class ReviewTag(models.Model):

    reviewId = models.ForeignKey(Review, unique=True)
    tag = models.ForeignKey(Tag)

    def __str__(self):

        return self.reviewId

class Reviewed(models.Model):

    reviewId = models.ForeignKey(Review, unique=True)
    reviewed = models.BooleanField(default=False)

    def __str__(self):

        return self.reviewId


class Training(models.Model):

    reviewId = models.ForeignKey(Review)
    feature = models.CharField(max_length=500)
    value = models.IntegerField()

    class Meta:

        unique_together = ('reviewId', 'feature')

    def __str__(self):

        return self.reviewId


class Code(models.Model):

    reviewId = models.ForeignKey(Review)
    code_content = models.CharField(max_length=5000)

    def __str_(self):

        return self.reviewId

class People(models.Model):

    reviewId = models.ForeignKey(Review)
    people_content = models.CharField(max_length=200)

    def __str_(self):

        return self.reviewId

class Issue(models.Model):

    reviewId = models.ForeignKey(Review)
    issue_content = models.CharField(max_length=200)

    def __str_(self):

        return self.reviewId

class link(models.Model):

    reviewId = models.ForeignKey(Review)
    link_content = models.CharField(max_length=1000)

    def __str_(self):

        return self.reviewId


class Image(models.Model):

    reviewId = models.ForeignKey(Review)
    image_src = models.CharField(max_length=1000)
    image_alt = models.CharField(max_length=200)

    def __str_(self):

        return self.reviewId

