from rest_framework import serializers

from review_service.models import Person


class PersonSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=255)
    name = serializers.CharField(max_length=100)
    created_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Person.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
