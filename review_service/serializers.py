from typing import List

from rest_framework import serializers

from review_service.models import Person, ReviewCycle, Question


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['email', 'name', 'created_at']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['title', 'description']


class ReviewCycleSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()

    class Meta:
        model = ReviewCycle
        fields = ['creator', 'name', 'reviewees', 'question', 'created_at']

    def create(self, validated_data):
        question_data = validated_data.pop('question')
        review_cycle = ReviewCycle.objects.create(**validated_data)
        Question.objects.create(review_cycle=review_cycle, **question_data)
        return review_cycle
