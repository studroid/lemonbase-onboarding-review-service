from django.db import models


class Person(models.Model):
    id = models.EmailField()
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)


class ReviewCycle(models.Model):
    # TODO: Add creator (1:N relationship to Person)
    name = models.CharField(max_length=50)
    # TODO: Add question (1:1 relationship to Question)
    # TODO: Add reviewee (N:N relationship to Person)
    created_at = models.DateTimeField(auto_now_add=True)


class Question(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
