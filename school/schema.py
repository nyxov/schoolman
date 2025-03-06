# schema.py

import graphene
from graphene_django.types import DjangoObjectType
from .models import Student, Teacher, Course
import yottadb
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

# Создание схемы
schema = graphene.Schema(query=Query, mutation=Mutation)



