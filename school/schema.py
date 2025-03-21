# schema.py

import graphene
import graphql_jwt
from graphql_jwt.decorators import login_required
from graphql_jwt import refresh_token
from graphene_django.types import DjangoObjectType
from graphql import GraphQLError
from .models import Student, Teacher, Course
from django.core.cache import cache

#from mumps import mumpsmth

class StudentType(DjangoObjectType):
    class Meta:
        model = Student

class TeacherType(DjangoObjectType):
    class Meta:
        model = Teacher

class CourseType(DjangoObjectType):
    class Meta:
        model = Course



class Query(graphene.ObjectType):

    private_data = graphene.String()

    @login_required
    def resolve_private_data(self, info):
        # Проверяем, авторизован ли пользователь
        if not info.context.user.is_authenticated:
            raise GraphQLError("You must be logged in to access this data.")
        
        # Если пользователь авторизован, возвращаем данные
        return "This is private data for authenticated users only."

    all_students = graphene.List(StudentType)
    all_teachers = graphene.List(TeacherType)
    
    all_courses = graphene.List(CourseType)
    myteachers = graphene.List(TeacherType)

    @login_required
    def resolve_all_students(self, info):
        return Student.objects.all()
    
    @login_required
    def resolve_myteachers(self, info):
        return Teacher.objects.filter(name__startswith='A')
    
    @login_required
    def resolve_all_teachers(self, info):
        return Teacher.objects.all()

    @login_required
    def resolve_all_courses(self, info):
        return Course.objects.all()

class CreateStudent(graphene.Mutation):
    student = graphene.Field(StudentType)

    class Arguments:
        name = graphene.String(required=True)
        age = graphene.Int(required=True)

    def mutate(self, info, name, age):
        student = Student.objects.create(name=name, age=age)
        return CreateStudent(student=student)

class Logout(graphene.Mutation):
    success = graphene.Boolean()

    @classmethod
    @login_required
    def mutate(cls, root, info):
        graphql_jwt.Revoke.Field()
        user = info.context.user
        cache_key = f"user_token_{user.id}"
        cache.delete(cache_key)
        # Дополнительная логика (например, очистка кэша)
        return Logout(success=True)

class Mutation(graphene.ObjectType):
    create_student = CreateStudent.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
#    delete_token_cookie = graphql_jwt.DeleteJSONWebTokenCookie.Field()
#    delete_refresh_token_cookie = graphql_jwt.DeleteRefreshTokenCookie.Field()
    verify_token = graphql_jwt.Verify.Field()
    revoke_token = graphql_jwt.Revoke.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    logout = Logout.Field()


# Создание схемы
schema = graphene.Schema(query=Query, mutation=Mutation) #, middleware = [AuthMiddleware()])



