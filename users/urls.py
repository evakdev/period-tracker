from django.urls import path

from .views import SignInPage, SignUpPage, profilePage

urlpatterns=[
    path('signup',SignUpPage),
    path('profile',profilePage),
    path('signin',SignInPage.as_view()),
]