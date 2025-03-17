from django.db import models
#from .basemodels import Human

class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    def __str__(self):
        return self.name

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student)
    def __str__(self):
        return self.name