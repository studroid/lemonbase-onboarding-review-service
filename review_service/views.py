import json

from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.http import JsonResponse, Http404
from django.views import View
from rest_framework import status, permissions, mixins, generics
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from review_service.models import Person, ReviewCycle, Question
from review_service.permissions import IsCreatorOrCreateOnly
from review_service.serializers import ReviewCycleSerializer, PersonSerializer


@api_view(['POST'])
def sign_up(request):
    serializer = PersonSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def sign_in(request):
    try:
        user = authenticate(request,
                            username=request.data['email'],
                            password=request.data['password'])
        if user is not None:
            login(request, user)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def sign_out(request):
    try:
        logout(request)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_200_OK)


class PolicyAPI(mixins.CreateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,
                generics.GenericAPIView):
    queryset = ReviewCycle.objects.all()
    serializer_class = ReviewCycleSerializer
    permission_classes = [permissions.IsAuthenticated, IsCreatorOrCreateOnly]

    @transaction.non_atomic_requests
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
