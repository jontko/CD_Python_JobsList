from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^handy$', views.index),
    url(r'^handy/validate$', views.validate),
    url(r'^handy/success$', views.success),
    url(r'^handy/login$', views.login),
    url(r'^handy/logout$', views.logout),
    url(r'^handy/newJob$', views.newJob),
    url(r'^handy/jobin$', views.job_page),
    url(r'^handy/dashboard$', views.dashboard),
    url(r'^handy/(?P<id>\d+)$', views.detail),
    url(r'^handy/(?P<id>\d+)/delete$', views.destroy),
    url(r'^handy/(?P<id>\d+)/edit$', views.jobEdit)
]