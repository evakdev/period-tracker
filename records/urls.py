
from django.contrib import admin
from django.urls import path
from .views import LoggingView
 
urlpatterns = [
    path('log/<slug:date>',LoggingView.as_view())
]