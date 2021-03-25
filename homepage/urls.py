from django.urls import path

from . import views, webhooks
from django.conf.urls import include, url

urlpatterns = [
    path('', views.index, name='index'),
    path('new_case/', views.raiseCase, name='raiseCase'),
    path('twitter_search/', views.twitterSearch, name='twitterSearch'),
    path('predict/', views.modelSite, name='Predict'),
    path('api/query', views.caseExist),
    path('api/model', views.MLmodel),
    path('webhook', webhooks.dialogflow)
]
