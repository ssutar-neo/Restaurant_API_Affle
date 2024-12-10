from django.contrib import admin
from django.urls import path
from .views import RestaurantQueryView

urlpatterns = [
    path("api/restaurants/",RestaurantQueryView.as_view(),name='restaurant-query'),
]