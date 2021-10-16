
from django.contrib import admin
from django.urls import path
from .views import LoggingView
 
urlpatterns = [
    path('log',LoggingView.as_view())
]