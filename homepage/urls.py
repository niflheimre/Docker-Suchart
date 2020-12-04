from django.urls import path

from . import views
from django.conf.urls import include, url

urlpatterns = [
    path('', views.index, name='index'),
    path('new_case/', views.raiseCase, name='raiseCase'),
]
