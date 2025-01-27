# schema.py

import graphene
from graphene_django.types import DjangoObjectType
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
    all_students = graphene.List(StudentType)
    all_teachers = graphene.List(TeacherType)
    all_courses = graphene.List(CourseType)

    def resolve_all_students(self, info):
        return Student.objects.all()

    def resolve_all_teachers(self, info):
        return Teacher.objects.all()

    def resolve_all_courses(self, info):
        return Course.objects.all()

schema = graphene.Schema(query=Query)