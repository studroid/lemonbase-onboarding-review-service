import json

from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.http import JsonResponse, Http404
from django.views import View
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from review_service.models import Person, ReviewCycle, Question
from review_service.serializers import ReviewCycleSerializer, PersonSerializer


def buildJsonResponse(status, msg='', data=None):
    json = {'msg': msg}
    if data is not None:
        json.update(data)
    return JsonResponse(json, status=status)


def JsonErrorResponse(msg="Bad Request"):
    return buildJsonResponse(status=400, msg=msg)


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


class PolicyAPI(APIView):
    def get_object(self, pk):
        try:
            return ReviewCycle.objects.get(pk=pk)
        except ReviewCycle.DoesNotExist:
            raise Http404

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonErrorResponse('Authentication required')

        # Authorization: A policy can only be accessed by the creator
        if request.method != 'POST' and 'policy_id' in kwargs:
            try:
                rc = ReviewCycle.objects.get(pk=kwargs['policy_id'])
                if not request.user.has_perm(rc):
                    return JsonErrorResponse('Permission denied')
            except:
                return JsonErrorResponse('Exception occurred while getting a ReviewCycle object')

        return super(PolicyAPI, self).dispatch(request, *args, **kwargs)

    @transaction.non_atomic_requests
    def get(self, request, policy_id=None, format=None):
        rc = self.get_object(policy_id)
        serializer = ReviewCycleSerializer(rc)
        return Response(serializer.data)

    def post(self, request, format=None):
        request.data['creator'] = request.user.id
        serializer = ReviewCycleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, policy_id=None, format=None):
        request.data['creator'] = request.user.id
        rc = self.get_object(policy_id)
        serializer = ReviewCycleSerializer(rc, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, policy_id=None, format=None):
        rc = self.get_object(policy_id)
        rc.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
