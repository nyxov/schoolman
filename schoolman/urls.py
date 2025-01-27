# school_management/urls.py
from django.contrib import admin
from school.views import graphql_view
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', graphql_view),
]