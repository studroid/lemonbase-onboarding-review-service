from typing import List

from rest_framework import serializers
from rest_framework.fields import HiddenField, IntegerField, CurrentUserDefault

from review_service.models import Person, ReviewCycle, Question


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['email', 'name', 'password', 'created_at']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return Person.objects.create_user(email=validated_data['email'],
                                          name=validated_data['name'],
                                          password=validated_data['password'])


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['title', 'description']


class ReviewCycleSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()

    class Meta:
        model = ReviewCycle
        fields = ['id', 'creator', 'name', 'reviewees', 'question', 'created_at']
        read_only_fields = ['id', 'creator']

    def create(self, validated_data):
        question_data = validated_data.pop('question')
        reviewees_data = validated_data.pop('reviewees')

        review_cycle = ReviewCycle.objects.create(**validated_data)
        Question.objects.create(review_cycle=review_cycle, **question_data)
        review_cycle.reviewees.set(reviewees_data)
        return review_cycle

    def update(self, instance, validated_data):
        question_data = validated_data.pop('question')
        reviewees_data = validated_data.pop('reviewees')

        instance.name = validated_data.get('name', instance.name)
        instance.question.title = question_data['title']
        instance.question.description = question_data['description']
        instance.question.save()
        instance.save()
        instance.reviewees.set(reviewees_data)
        return instance
