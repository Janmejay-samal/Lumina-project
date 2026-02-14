from django.db import models

class Student(models.Model):
    name=models.CharField(max_length=100)
    age=models.IntegerField()
    sec=models.CharField(max_length=10)
    branch=models.CharField(max_length=10)


class register(models.Model):
    username=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.IntegerField()
    password=models.CharField(max_length=20)
