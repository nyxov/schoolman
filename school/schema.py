# schema.py

import graphene
import graphql_jwt
from graphql_jwt.decorators import login_required
from graphene_django.types import DjangoObjectType
from graphql import GraphQLError
from .models import Student, Teacher, Course

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

    def resolve_all_students(self, info):
        return Student.objects.all()
    
    def resolve_myteachers(self, info):
        return Teacher.objects.filter(name__startswith='A')
    
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

class Mutation(graphene.ObjectType):
    create_student = CreateStudent.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

class AuthMiddleware:
    def resolve(self, next, root, info, **kwargs):
        # Проверяем, требуется ли авторизация для запрашиваемого поля
        if hasattr(info.return_type, "auth_required") and info.return_type.auth_required:
            if not info.context.user.is_authenticated:
                raise GraphQLError("Authentication required.")
        
        return next(root, info, **kwargs)

# Создание схемы
schema = graphene.Schema(query=Query, mutation=Mutation) #, middleware = [AuthMiddleware()])

middleware = [AuthMiddleware()]

