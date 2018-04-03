from django.conf.urls import url
from . import views



urlpatterns = [

    url(r'^rawcomment-view/$', views.RawCommentItemApiView.as_view()),
    url(r'^rawcomment-view/(?P<id>[a-zA-Z0-9]+)$', views.RawCommentItemApiView.as_view())
]
