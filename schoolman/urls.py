# school_management/urls.py
from django.contrib import admin, auth
from school.views import graphql_view
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', csrf_exempt(graphql_view)),
#    path('accounts', auth.url)
]