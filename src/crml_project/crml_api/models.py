from django.db import models

# Create your models here.


class Tag(models.Model):

    tagId = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):

        return self.name


class Algorithm(models.Model):

    algorithmId = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):

        return self.name


class Performance(models.Model):

    algorithm = models.ForeignKey(Algorithm)
    size = models.IntegerField()
    accuracy = models.DecimalField(max_digits=4, decimal_places=3)

    class Meta:

        unique_together = ('algorithm', 'size')

    def __str__(self):

        return self.size + '_' + self.algorithm.name


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

# tf + stopwords


class Training_m1(models.Model):

    reviewId = models.ForeignKey(Review)
    feature = models.CharField(max_length=500)
    value = models.PositiveIntegerField()

    class Meta:

        unique_together = ('reviewId', 'feature')

    def __str__(self):

        return self.feature


class Performance_m1(models.Model):

    algorithm = models.ForeignKey(Algorithm)
    size = models.IntegerField()
    binary = models.BooleanField(default=False)
    sa_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    og_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    vr_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    sl_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    tx_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    ld_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    sp_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    ck_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    rs_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    lg_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    it_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    tr_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    pc_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    ot_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    avg_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)

    class Meta:

        unique_together = ('algorithm', 'size', 'binary')

    def __str__(self):

        return self.size + '_' + self.algorithm.name

# tf + stopwords + stemming


class Training_m2(models.Model):

    reviewId = models.ForeignKey(Review)
    feature = models.CharField(max_length=500)
    value = models.PositiveIntegerField()

    class Meta:

        unique_together = ('reviewId', 'feature')

    def __str__(self):

        return self.feature


class Performance_m2(models.Model):

    algorithm = models.ForeignKey(Algorithm)
    size = models.IntegerField()
    binary = models.BooleanField(default=False)
    sa_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    og_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    vr_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    sl_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    tx_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    ld_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    sp_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    ck_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    rs_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    lg_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    it_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    tr_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    pc_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    ot_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    avg_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)

    class Meta:

        unique_together = ('algorithm', 'size', 'binary')

    def __str__(self):

        return self.size + '_' + self.algorithm.name


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


class PullRequest(models.Model):

    owner = models.CharField(max_length=100)
    project = models.CharField(max_length=100)
    pull_request = models.CharField(max_length=100)
    commit = models.CharField(max_length=100)
    prob = models.DecimalField(max_digits=4, decimal_places=3)
    reason = models.CharField(max_length=500)

    class Meta:

        unique_together = ('owner', 'project', 'pull_request', 'commit')

    def __str__(self):

        return self.file_path


class Performance_unbalanced_learn(models.Model):

    algorithm = models.ForeignKey(Algorithm)
    size = models.IntegerField()
    binary = models.BooleanField(default=False)
    technique = models.CharField(max_length=100, default='')
    sa_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    og_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    vr_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    sl_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    tx_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    ld_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    sp_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    ck_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    rs_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    lg_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    it_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    tr_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    pc_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    ot_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)
    avg_f1 = models.DecimalField(
        max_digits=4, decimal_places=3, null=True, default=None)

    class Meta:

        unique_together = ('algorithm', 'size', 'binary', 'technique')

    def __str__(self):

        return self.size + '_' + self.algorithm.name
