from django.shortcuts import render
from django.http import JsonResponse
from graphene_django.views import GraphQLView
from .schema import schema

def graphql_view(request):
    view = GraphQLView.as_view(schema=schema, graphiql=True)
    return view(request)
