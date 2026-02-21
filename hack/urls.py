# spaces/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('space/<int:space_id>/', views.space_detail, name='space_detail'),
    path('update_occupancy/<int:space_id>/', views.update_occupancy, name='update_occupancy'),
]