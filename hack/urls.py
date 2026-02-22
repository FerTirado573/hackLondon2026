# spaces/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('space/<int:space_id>/', views.space_detail, name='space_detail'),
    path("book/<int:space_id>/", views.book_space, name="book_space"),
    path('update_occupancy/<int:space_id>/', views.update_occupancy, name='update_occupancy'),
]