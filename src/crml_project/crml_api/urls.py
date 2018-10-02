from django.conf.urls import url
from . import views


urlpatterns = [

    url(r'^discussion/$', views.DiscussionApiView.as_view()),
    url(r'^discussion/(?P<id>[a-zA-Z0-9]+)$',
        views.DiscussionApiView.as_view()),
    url(r'^models/$', views.MLModels),
    url(r'^evolutions/$', views.ModelsEvolution)

]
