from django.db import models

# Create your models here.

class RawCommentItem(models.Model):

    rawCommentText = models.CharField(max_length=1000)
    issueCommentId = models.CharField(max_length=100, unique=True)
    tag = models.IntegerField()

    def __str_(self):

        return self.rawCommentText
