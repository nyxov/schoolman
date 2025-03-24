# schema.py

import graphene
import graphql_jwt
from graphql_jwt.decorators import login_required # as original_login_required
from graphql_jwt import refresh_token
from graphene_django.types import DjangoObjectType
from graphql import GraphQLError
import graphql_jwt.refresh_token
from django.core.cache import cache
from functools import wraps
from graphql_jwt.exceptions import PermissionDenied
from graphql_jwt.refresh_token.models import RefreshToken

#from mumps import mumpsmth

def login_required_new(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        info = args[1]  # Второй аргумент — это объект info
        if info == None:
            info = args[2]
        user = info.context.user

        if not user.is_authenticated:
            raise PermissionDenied("User is not authenticated")

        #if "loggedout" in info.context.META:
        #    raise PermissionDenied("User is logged out")

        # Проверяем, находится ли токен в черном списке
        #token = info.context.META.get("HTTP_AUTHORIZATION", "").split(" ")[-1]
        token = info.context.META["HTTP_X_CSRFTOKEN"] #graphql_jwt.refresh_token()
        try:
            RefreshToken.objects.get(token=token, revoked__isnull=False)
            raise PermissionDenied("Token has been revoked")
        except RefreshToken.DoesNotExist:
            pass

        return func(*args, **kwargs)

    return wrapper


class Logout(graphene.Mutation):
    success = graphene.Boolean()

    @classmethod
    @login_required
    def mutate(cls, root, info):
        graphql_jwt.Revoke.Field()
        user = info.context.user
        #info.context.META["loggedout"] = "True"
        cache_key = f"user_token_{user.id}"
        cache.delete(cache_key)
        # Дополнительная логика (например, очистка кэша)
        return Logout(success=True)

class Query(graphene.ObjectType):
    private_data = graphene.String()


class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    delete_token_cookie = graphql_jwt.DeleteJSONWebTokenCookie.Field()
    delete_refresh_token_cookie = graphql_jwt.DeleteRefreshTokenCookie.Field()
    verify_token = graphql_jwt.Verify.Field()
    revoke_token = graphql_jwt.Revoke.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    logout = Logout.Field()


# Создание схемы
schema = graphene.Schema(query=Query, mutation=Mutation) #, middleware = [AuthMiddleware()])



