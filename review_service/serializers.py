from typing import List

from rest_framework import serializers

from review_service.models import Person


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields: List[str] = ['email', 'name', 'created_at']


