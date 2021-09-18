from django.urls import path
from .views import *
urlpatterns=[
    path('signup',SignUpPage),
    path('signin',SignInPage),
    path('profile',profilePage)
]