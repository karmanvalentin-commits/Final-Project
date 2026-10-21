"""Головні адреси сайту: усе, що не admin, передаємо в наш застосунок predictor."""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("predictor.urls")),
]
