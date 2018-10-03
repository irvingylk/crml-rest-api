from django.db import models

# Create your models here.


class Commit(models.Model):
    Project = models.CharField(
        verbose_name='Project', null=True, max_length=100)
    PR = models.CharField(verbose_name='PR', null=True, max_length=100)
    CommitHash = models.CharField(
        verbose_name='CommitHash', null=True, max_length=100)
    Prob = models.FloatField(verbose_name='Prob', null=True)
    Reason = models.CharField(verbose_name='Reason', null=True, max_length=255)
    Date = models.DateField(verbose_name='Date', null=True)

    def __str__(self):
        return str(self.id)


class Release(models.Model):
    Project = models.CharField(
        verbose_name='Project', null=True, max_length=100)
    File = models.CharField(verbose_name='File', null=True, max_length=100)
    Prob = models.FloatField(verbose_name='Prob', null=True)
    Reason = models.CharField(verbose_name='Reason', null=True, max_length=255)
    Release = models.CharField(
        verbose_name='Release', null=True, max_length=100)
    Date = models.DateField(verbose_name='Date', null=True)
    COMM = models.FloatField(verbose_name='COMM', null=True)
    ADEV = models.FloatField(verbose_name='ADEV', null=True)
    DDEV = models.FloatField(verbose_name='DDEV', null=True)
    ADD = models.FloatField(verbose_name='ADD', null=True)
    DEL = models.FloatField(verbose_name='DEL', null=True)
    SCTR = models.FloatField(verbose_name='SCTR', null=True)
    OWN = models.FloatField(verbose_name='OWN', null=True)
    MINOR = models.FloatField(verbose_name='MINOR', null=True)
    NCOMM = models.FloatField(verbose_name='NCOMM', null=True)
    NADEV = models.FloatField(verbose_name='NADEV', null=True)
    NDDEV = models.FloatField(verbose_name='NDDEV', null=True)
    NSCTR = models.FloatField(verbose_name='NSCTR', null=True)
    NS = models.FloatField(verbose_name='NS', null=True)
    ND = models.FloatField(verbose_name='ND', null=True)
    NF = models.FloatField(verbose_name='NF', null=True)
    Entropy = models.FloatField(verbose_name='Entropy', null=True)
    LA = models.FloatField(verbose_name='LA', null=True)
    LD = models.FloatField(verbose_name='LD', null=True)
    LT = models.FloatField(verbose_name='LT', null=True)
    FIX = models.FloatField(verbose_name='FIX', null=True)
    NDEV = models.FloatField(verbose_name='NDEV', null=True)
    AGE = models.FloatField(verbose_name='AGE', null=True)
    NUC = models.FloatField(verbose_name='NUC', null=True)
    EXP = models.FloatField(verbose_name='EXP', null=True)
    REXP = models.FloatField(verbose_name='REXP', null=True)
    SEXP = models.FloatField(verbose_name='SEXP', null=True)

    def __str__(self):
        return str(self.id)


class Pr(models.Model):
    project = models.CharField(
        verbose_name='Project', null=True, max_length=100)
    pr = models.CharField(verbose_name='PR', null=True, max_length=100)
    commithash = models.CharField(
        verbose_name='CommitHash', null=True, max_length=100)
    date = models.DateField(verbose_name='Date', null=True)

    def __str__(self):
        return str(self.id)


class ReviewComment(models.Model):
    project = models.CharField(
        verbose_name='Project', null=True, max_length=100)
    pr = models.CharField(verbose_name='PR', null=True, max_length=100)
    commentid = models.CharField(
        verbose_name='CommentID', null=True, max_length=100)
    reviewmsg = models.CharField(
        verbose_name='ReviewMSG', null=True, max_length=255)
    reviewtag = models.CharField(
        verbose_name='ReviewTag', null=True, max_length=100)
    date = models.DateField(verbose_name='Date', null=True)

    def __str__(self):
        return str(self.id)
