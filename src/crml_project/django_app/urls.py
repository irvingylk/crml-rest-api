# Qihua Zhu

from django.conf.urls import url
from django_app import views
urlpatterns = [
    url(r'^getprobs$', views.get_probs, name='get_probs'),
    url(r'^getprs$', views.get_prs, name='get_prs'),
    url(r'^getcommits$', views.get_commits, name='get_commits'),


    url(r'^getcleanpercent$', views.get_clean_percent, name='get_clean_percent'),
    url(r'^getlatestfile1$', views.get_latest_file1, name='get_latest_file1'),
    url(r'^getlatestfile2$', views.get_latest_file2, name='get_latest_file2'),
    url(r'^getmetricplot1$', views.get_metric_plot1, name='get_metric_plot1'),
    url(r'^getmetricplot2$', views.get_metric_plot2, name='get_metric_plot2'),
    url(r'^getprchart$', views.get_pr_chart, name='get_pr_chart'),
    url(r'^getreviewtag$', views.get_review_tag, name='get_review_tag'),
]
