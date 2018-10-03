# Qihua Zhu

import json
from datetime import timedelta
from collections import Counter

from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

from .models import Commit, Release, Pr, ReviewComment


# Solve cross-domain problems
def ctxWraped(ctx):
    response = JsonResponse(ctx)
    response["Access-Control-Allow-Headers"] = "content-type"
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    return response


# request and get table data(top 10 file+prob) on the home page
@csrf_exempt
def get_probs(request):
    ctx = {}
    prostr = request.POST.get('prostr', '')
    currentPage = request.POST.get('currentPage', '')
    try:
        prob_list = getAllProbs(prostr, currentPage)
        ctx["status"] = "success"
    except:
        ctx["status"] = "false"
        ctx["message"] = "Server Exception"
        prob_list = []
    ctx["probs"] = prob_list

    return ctxWraped(ctx)


# request and get prob data on PR page
@csrf_exempt
def get_prs(request):
    ctx = {}
    prostr = request.POST.get('prostr', '')
    try:
        max_prob_list = getAllPrs(prostr)
        ctx["status"] = "success"
    except:
        ctx["status"] = "false"
        ctx["message"] = "Server Exception"
        max_prob_list = []
    ctx["max_prob_list"] = max_prob_list

    return ctxWraped(ctx)


# request and get prob data on commit page
@csrf_exempt
def get_commits(request):
    ctx = {}
    res = {}
    prostr = request.POST.get('prostr', '')
    prnum = request.POST.get('prnum', '')
    try:
        res = getAllCommits(prostr, prnum)
        ctx["status"] = "success"
    except Exception as e:
        myex = e
        ctx["status"] = "false"
        ctx["message"] = "Server Exception"
        res["list"] = []
    ctx["prob_list"] = res["list"]
    ctx["max_prob"] = res["max_prob"]

    return ctxWraped(ctx)


# Select the top 10 risky files and prob data on the home page
def getAllProbs(prostr, currentPage):
    result = []
    with connection.cursor() as cursor:
        cursor.execute("SELECT File,Prob FROM django_app_release WHERE Project=%s ORDER BY Pro b DESC  limit %s",
                       [prostr, int(currentPage)])
        rows = cursor.fetchall()

    for prob in rows:
        prob_tem = {}
        prob_tem["file_name"] = prob[0]
        prob_tem["prob"] = prob[1]
        result.append(prob_tem)
    return result


# Select Max(prob) data for each PR on PR page
def getAllPrs(prostr):
    result = []
    with connection.cursor() as cursor:
        cursor.execute("SELECT PR,MAX(Prob) as max_probs FROM django_app_commit WHERE Project=%s GROUP BY PR",
                       [prostr])
        rows = cursor.fetchall()

    for prob in rows:
        prob_tem = {}
        prob_tem["pr_num"] = prob[0]
        prob_tem["max_probs"] = prob[1]
        result.append(prob_tem)
    return result


# Select prob data on commit page
def getAllCommits(prostr, prnum):
    result = []
    ret = {}
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT Prob,CommitHash FROM django_app_commit WHERE (PR=%s AND Project=%s)", [prnum, prostr])
        rows = cursor.fetchall()
        cursor.execute("SELECT MAX(Prob) as max_prob FROM django_app_commit WHERE (PR=%s AND Project=%s)",
                       [prnum, prostr])
        rows_max = cursor.fetchone()

    for prob in rows:
        prob_tem = {}
        prob_tem["prob"] = prob[0]
        prob_tem["commit_hash"] = prob[1]
        result.append(prob_tem)

    ret["max_prob"] = rows_max[0]
    ret["list"] = result
    return ret


# Func1
def get_clean_percent(request):
    """
    Method: POST
    Data Type: JSON
    Data e.g: {"prostr": "django/django"}
    URL: doamin/github/getcleanpercent
    """
    # get project
    prostr = json.loads(request.body.decode('utf-8')).get('prostr')
    # select latest date
    latest_date = Release.objects.filter(
        Project=prostr).order_by('-Date').first().Date
    # select the number of files according to the latest date
    release_count = Release.objects.filter(Date=latest_date).count()
    # select the number of files according to the latest date and Prob=0
    release_prob_count = Release.objects.filter(
        Date=latest_date, Prob=0).count()
    # release_count cannot be zero
    try:
        percent = round(release_prob_count / release_count * 100)
    except ZeroDivisionError:
        return JsonResponse(data={'message': 'Not found', 'percent': 0}), 404
    return JsonResponse(data={'message': '', 'percent': percent})


# Func2-1
def get_latest_file1(request):
    """
    Method: POST
    Data Type: JSON
    Data e.g: {"prostr": "django/django"}
    URL: domain/github/getlatestfile1
    """
    # get project
    prostr = json.loads(request.body.decode('utf-8')).get('prostr')
    # select all the releases
    releases = Release.objects.filter(Project=prostr).all()
    # select latest 10 releases => set(remove repeating ones) => sorted => get latest 10
    release_list = sorted(set([release.Release for release in releases]))[-10:]
    # select the default release(the most left one)
    release_list_0 = releases.filter(Release=release_list[0])
    level_0 = release_list_0.filter(Prob__gte=0, Prob__lt=0.2).count()
    level_1 = release_list_0.filter(Prob__gte=0.2, Prob__lt=0.4).count()
    level_2 = release_list_0.filter(Prob__gte=0.4, Prob__lt=0.6).count()
    level_3 = release_list_0.filter(Prob__gte=0.6, Prob__lt=0.8).count()
    level_4 = release_list_0.filter(Prob__gte=0.8, Prob__lte=1.0).count()
    return JsonResponse(data={'message': '',
                              'stepItems': release_list,
                              'level_data': [level_0, level_1, level_2, level_3, level_4]})


# Func2-2
def get_latest_file2(request):
    """
    Method: POST
    Data Type: JSON
    Data e.g: {"prostr": "django/django", "release": "v2.1"}
    URL: domain/github/getlatestfile2
    """
    # get project and release
    req_data = json.loads(request.body.decode('utf-8'))
    prostr = req_data.get('prostr')
    release = req_data.get('release')
    # select all the releases according to the certain release
    releases = Release.objects.filter(Project=prostr, Release=release).all()
    # select the number of files respectively in different prob levels
    level_0 = releases.filter(Prob__gte=0, Prob__lt=0.2).count()
    level_1 = releases.filter(Prob__gte=0.2, Prob__lt=0.4).count()
    level_2 = releases.filter(Prob__gte=0.4, Prob__lt=0.6).count()
    level_3 = releases.filter(Prob__gte=0.6, Prob__lt=0.8).count()
    level_4 = releases.filter(Prob__gte=0.8, Prob__lte=1.0).count()

    return JsonResponse(data={'message': '',
                              'level_data': [level_0, level_1, level_2, level_3, level_4]})


# Func3-1
def get_metric_plot1(request):
    """
    Method: POST
    Data Type: JSON
    Data e.g: {"prostr": "django/django"}
    URL: domain/github/getmetricplot1
    """
    # get project
    prostr = json.loads(request.body.decode('utf-8')).get('prostr')
    # select all the releases
    releases = Release.objects.filter(Project=prostr).all()
    # select latest 5 releases => set(remove repeating ones) => sorted => get latest 5
    # default set checkboxes
    release_list = sorted(set([release.Release for release in releases]))[-5:]

    plots = []
    for release in release_list:
        plot = {}
        plot['name'] = release
        plot['type'] = 'scatter'
        plot['data'] = []
        rels = Release.objects.filter(Release=release).all()
        for rel in rels:
            # default set selectoption
            plot['data'].append([rel.COMM, rel.Prob])
            # plot['data'].append([rel.LOC, rel.Prob])
            # plot['data'].append([rel.ADEV, rel.Prob])
            # plot['data'].append([rel.OEXP, rel.Prob])
            # plot['data'].append([rel.OWN, rel.Prob])
        plots.append(plot)

    return JsonResponse(data={'message': '',
                              'releases': release_list,
                              'plots': plots})


# Func3-2
def get_metric_plot2(request):
    """
    Method: POST
    Data Type: JSON
    Data e.g: {"prostr": "django/django", "plot_on_x": "COMM", "releases": ["v2.0", "v2.5"]}
    URL: domain/github/getmetricplot2
    """
    # get project & release & plot_on_x
    req_data = json.loads(request.body.decode('utf-8'))
    prostr = req_data.get('prostr')
    releases = req_data.get('releases')
    plot_on_x = req_data.get('plot_on_x')

    plots = []
    for release in releases:
        plot = {}
        plot['name'] = release
        plot['type'] = 'scatter'
        plot['data'] = []
        rels = Release.objects.filter(Release=release, Project=prostr).all()
        for rel in rels:
            print(rel.__dict__[plot_on_x])
            plot['data'].append([rel.__dict__[plot_on_x], rel.Prob])
        plots.append(plot)

    return JsonResponse(data={'message': '',
                              'plots': plots})


# Func4
def get_pr_chart(request):
    """
    Method: POST
    Data Type: JSON
    Data e.g: {"prostr": "django/django"}
    URL: domain/github/getprchart
    """
    # get project
    prostr = json.loads(request.body.decode('utf-8')).get('prostr')

    # select latest date
    latest_date = Commit.objects.filter(
        Project=prostr).all().order_by('-Date').first().Date

    # one week
    week = timedelta(days=7)
    # one day
    day = timedelta(days=1)

    # commits list based on one week
    commits = []
    time_line = []
    for i in range(10):

        commit = Commit.objects.filter(
            Date__range=(latest_date-((i+1) * week), latest_date-(i * week))
        ).all()
        commits.append(commit)
        time_line.append('{}~{}'.format(
            latest_date-((i+1) * week), latest_date-(i * week)))
        latest_date -= day

    # calculate prob=0 & prob!=0 pr number
    clean_data = []
    risky_data = []
    pr_list = []
    for commit in commits:
        clean = 0
        risky = 0
        for c in commit:
            if c.PR not in pr_list:
                comms = Commit.objects.filter(PR=c.PR).all()
                for com in comms:
                    if com.Prob != 0:
                        risky += 1
                        break
                else:
                    clean += 1
                pr_list.append(c.PR)
        clean_data.append(clean)
        risky_data.append(risky)

    # select no review comment pr
    no_review_prs = []
    for p in Pr.objects.all():
        if p.pr not in pr_list:
            pr = ReviewComment.objects.filter(pr=p.pr)
            if not pr:
                no_review_prs.append(p)

    # remove repeating prs from no review comment list
    no_review_prs_set = []
    no_review_pr_set = []
    for no_review in no_review_prs:
        if no_review.pr not in no_review_pr_set:
            no_review_pr_set.append(no_review.pr)
            no_review_prs_set.append(no_review)

    # calculate no review comment pr number
    # select latest date
    latest_date = Commit.objects.filter(
        Project=prostr).all().order_by('-Date').first().Date
    no_review_data = []
    for i in range(10):

        n_data = 0
        for n_rev in no_review_prs_set:
            if latest_date-((i+1) * week) <= n_rev.date <= latest_date-(i * week):

                n_data += 1

        latest_date -= day
        no_review_data.append(n_data)

    data = [
        {
            'name': 'Clean PR(P = 0)',
            'type': 'bar',
            'data': clean_data[::-1]
        },
        {
            'name': 'Risky PR(P > 0)',
            'type': 'bar',
            'data': risky_data[::-1]
        },
        {
            'name': 'No Review Comments',
            'type': 'line',
            'data': no_review_data[::-1]
        }
    ]
    return JsonResponse(data={'chart_data': data, 'time_line': time_line[::-1]})


# Func5
def get_review_tag(request):
    """
    Method: POST
    Data Type: JSON
    Data e.g: {"prostr": "django/django"}
    URL: domain/github/getreviewtag
    """
    # get project
    prostr = json.loads(request.body.decode('utf-8')).get('prostr')
    commits = Commit.objects.filter(Project=prostr).all()

    level_0 = commits.filter(Prob__gte=0, Prob__lt=0.2).all()
    level_1 = commits.filter(Prob__gte=0.2, Prob__lt=0.4).all()
    level_2 = commits.filter(Prob__gte=0.4, Prob__lt=0.6).all()
    level_3 = commits.filter(Prob__gte=0.6, Prob__lt=0.8).all()
    level_4 = commits.filter(Prob__gte=0.8, Prob__lte=1.0).all()

    l0_tags = []
    for l0 in level_0:
        pr_comment = ReviewComment.objects.filter(pr=l0.PR).first()
        l0_tags.append(pr_comment.reviewtag)

    l1_tags = []
    for l1 in level_1:
        pr_comment = ReviewComment.objects.filter(pr=l1.PR).first()
        l1_tags.append(pr_comment.reviewtag)

    l2_tags = []
    for l2 in level_2:
        pr_comment = ReviewComment.objects.filter(pr=l2.PR).first()
        l2_tags.append(pr_comment.reviewtag)

    l3_tags = []
    for l3 in level_3:
        pr_comment = ReviewComment.objects.filter(pr=l3.PR).first()
        l3_tags.append(pr_comment.reviewtag)

    l4_tags = []
    for l4 in level_4:
        pr_comment = ReviewComment.objects.filter(pr=l4.PR).first()
        l4_tags.append(pr_comment.reviewtag)

    tags = ['Solution Approach', 'Organization',
            'Logic', 'Test', 'Process', 'Others']

    val_data = [[], [], [], [], []]
    for i, tag in enumerate(tags):

        val_data[0].append({'value': Counter(l0_tags)[tag], 'name': tags[i]})
        val_data[1].append({'value': Counter(l1_tags)[tag], 'name': tags[i]})
        val_data[2].append({'value': Counter(l2_tags)[tag], 'name': tags[i]})
        val_data[3].append({'value': Counter(l3_tags)[tag], 'name': tags[i]})
        val_data[4].append({'value': Counter(l4_tags)[tag], 'name': tags[i]})

    return JsonResponse(data={'val_data': val_data})
