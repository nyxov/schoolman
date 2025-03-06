from django.db import models
from .basemodels import Human

class Student(Human):
    interestas = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Teacher(Human):
    skill = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student)
    def __str__(self):
        return self.name