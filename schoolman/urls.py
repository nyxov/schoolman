# school_management/urls.py
from django.contrib import admin, auth
from school.views import graphql_view
from auth.views import graphql_view as auth_view
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphql_jwt.decorators import jwt_cookie

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', jwt_cookie(csrf_exempt(graphql_view))),
    path('auth/', jwt_cookie(csrf_exempt(auth_view))),
#    path('accounts', auth.url)
]