from django.db import models

# Create your models here.


class PullRequest(models.Model):

    pr_id = models.CharField(max_length=50)
    project = models.CharField(max_length=100)
    commit_hash = models.CharField(max_length=100)
    creation_time = models.DateTimeField(null=True, default=None)
    number = models.CharField(max_length=10)
    pr_time = models.DateTimeField(null=True, default=None)

    def __str__(self):

        return self.commit_hash + '_' + self.project


class DiscussionTag(models.Model):

    tag_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Discussion(models.Model):

    discussion_id = models.CharField(max_length=50, primary_key=True)
    pr_id = models.CharField(max_length=50)
    content = models.CharField(max_length=5000, default='')
    content_length = models.IntegerField(default=0)
    is_inline_discussion = models.BooleanField(default=False)
    reviewed = models.BooleanField(default=False)
    creation_time = models.DateTimeField()
    reviewed_time = models.DateTimeField(null=True, default=None)
    project = models.CharField(max_length=100, default='')
    tag = models.ForeignKey(DiscussionTag, related_name='tag_true')
    predicted = models.ForeignKey(
        DiscussionTag, related_name='tag_predicted', null=True, default=None)
    pr_number = models.CharField(max_length=50, default="")
    tag_desc = models.CharField(max_length=50, default="")
    pr_time = models.DateTimeField(null=True, default=None)

    def __str__(self):

        return self.discussion_id


class Tag(models.Model):

    tagId = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):

        return self.name


class Performance(models.Model):

    algorithm = models.CharField(max_length=200)
    extraction_method = models.CharField(max_length=500)
    evaluation_method = models.CharField(max_length=500)
    training_size = models.IntegerField()
    testing_size = models.IntegerField()
    avg_sa_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    avg_og_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    avg_ts_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    avg_lg_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    avg_pc_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    avg_ot_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    avg_avg_f1s = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    lower_extreme = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    lower_quartile = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    median = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    upper_quartile = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    upper_extreme = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)

    class Meta:

        unique_together = ('algorithm', 'extraction_method',
                           'evaluation_method', 'training_size', 'testing_size')

    def __str__(self):

        return self.size + '_' + self.algorithm


class Review(models.Model):

    reviewId = models.CharField(max_length=50, primary_key=True)
    review_content = models.CharField(max_length=5000, default='')
    review_content_length = models.IntegerField(default=0)
    is_inline_review = models.BooleanField(default=False)
    extracted = models.BooleanField(default=False)
    reviewed = models.BooleanField(default=False)
    changed = models.BooleanField(default=False)
    reviewed_time = models.DateTimeField(null=True, default=None)
    project = models.CharField(max_length=100, default='')
    tag = models.ForeignKey(Tag, related_name='reviews_true')
    predicted = models.ForeignKey(
        Tag, related_name='reviews_predicted', null=True, default=None)
    trainings_size = models.IntegerField(default=0)
    pr_id = models.CharField(max_length=50, default='')
    creation_time = models.DateTimeField(null=True, default=None)

    def __str__(self):

        return self.reviewId


class Training(models.Model):

    reviewId = models.ForeignKey(Review)
    feature = models.CharField(max_length=500)
    value = models.DecimalField(max_digits=10, decimal_places=5)

    class Meta:

        unique_together = ('reviewId', 'feature')

    def __str__(self):

        return self.feature


class Code(models.Model):

    reviewId = models.ForeignKey(Review)
    code_content = models.CharField(max_length=5000)

    def __str__(self):

        return self.code_content


class People(models.Model):

    reviewId = models.ForeignKey(Review)
    people_content = models.CharField(max_length=200)

    def __str__(self):

        return self.people_content


class Issue(models.Model):

    reviewId = models.ForeignKey(Review)
    issue_content = models.CharField(max_length=200)

    def __str__(self):

        return self.issue_content


class link(models.Model):

    reviewId = models.ForeignKey(Review)
    link_content = models.CharField(max_length=1000)

    def __str__(self):

        return self.link_content


class Image(models.Model):

    reviewId = models.ForeignKey(Review)
    image_src = models.CharField(max_length=1000)
    image_alt = models.CharField(max_length=200)

    def __str__(self):

        return self.image_src


class File(models.Model):

    owner = models.CharField(max_length=100)
    project = models.CharField(max_length=100)
    file_path = models.FilePathField(path="(\/[a-zA-Z0-9]+)*", max_length=200)
    prob = models.DecimalField(max_digits=4, decimal_places=3)
    reason = models.CharField(max_length=500)

    class Meta:

        unique_together = ('owner', 'project', 'file_path')

    def __str__(self):

        return self.file_path


class Commit(models.Model):

    pr = models.CharField(null=True, max_length=100)
    commit_hash = models.CharField(max_length=200, primary_key=True)
    prob = models.DecimalField(max_digits=4, decimal_places=3)
    predict_as = models.CharField(max_length=1)
    lime = models.CharField(max_length=200)
    project = models.CharField(max_length=50)
    date = models.DateField(null=True)

    def __str__(self):

        return self.commit_hash


class Release(models.Model):

    Project = models.CharField(
        verbose_name='Project', null=True, max_length=100)
    File = models.CharField(verbose_name='File', null=True, max_length=100)
    Prob = models.FloatField(verbose_name='Prob', null=True)
    Reason = models.CharField(verbose_name='Reason', null=True, max_length=255)
    Release = models.CharField(
        verbose_name='Release', null=True, max_length=100)
    Date = models.DateField(verbose_name='Date', null=True, default=None)
    COMM = models.FloatField(verbose_name='COMM', null=True, default=None)
    ADEV = models.FloatField(verbose_name='ADEV', null=True, default=None)
    DDEV = models.FloatField(verbose_name='DDEV', null=True, default=None)
    ADD = models.FloatField(verbose_name='ADD', null=True, default=None)
    DEL = models.FloatField(verbose_name='DEL', null=True, default=None)

    def __str__(self):
        return str(self.id)
