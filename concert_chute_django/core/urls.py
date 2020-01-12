from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('view_venue/<str:pk>/', views.view_venue, name='view_venue'),
]
