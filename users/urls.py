from django.urls import path

from .views import SignInPage, SignUpPage, ProfilePage

urlpatterns=[
    path('signup',SignUpPage.as_view()),
    path('profile',ProfilePage.as_view()),
    path('signin',SignInPage.as_view()),
]