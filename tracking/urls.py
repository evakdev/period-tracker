from django.urls import include, path

from .views import *

urlpatterns = [
    path('track/', tracking),
    path('trackables/manage', trackable_manage),
    path('track/addcycle/', add_cycle),
    path('db/', database),
    path('addcat/',add_categories),
]
