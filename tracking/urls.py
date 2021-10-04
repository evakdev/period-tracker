
from django.urls import path

from .views import *

urlpatterns = [
    path('categories',CategoryListView.as_view(),name ='category_list'),
    path('categories/<int:pk>', CategoryDetailView.as_view(), name = 'category_details'),
    path('categories/create',CreateCategoryView.as_view(),name ='create_category'),
    path('categories/edit/<int:pk>',UpdateCategoryView.as_view(),name ='update_category'),
    path('categories/delete/<int:pk>',DeleteCategoryView.as_view(),name ='delete_category'),
    path('categories/<int:category_pk>/create_trackable',CreateTrackableView.as_view(),name = 'create_trackable'),
    path('trackables/<int:pk>',TrackableDetailView.as_view(),name= 'trackable_details'),
    path('trackables/edit/<int:pk>',UpdateTrackableView.as_view(),name = 'update_trackable'),
    path('trackables/move/<int:pk>',MoveTrackableView.as_view(), name = 'move_trackable'),
    path('trackables/delete/<int:pk>',DeleteTrackableView.as_view(),name = 'delete_trackable'),
    
]
