from django.db import models


class Person(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)


class Question(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)


class ReviewCycle(models.Model):
    creator = models.ForeignKey(Person, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name='+')
    reviewee = models.ManyToManyField(Person, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)
