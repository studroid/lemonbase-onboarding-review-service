import json

from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.http import JsonResponse, Http404
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView

from review_service.models import Person, ReviewCycle, Question
from review_service.serializers import ReviewCycleSerializer

__AUTH_METHOD = 'POST'


def buildJsonResponse(status, msg='', data=None):
    json = {'msg': msg}
    if data is not None:
        json.update(data)
    return JsonResponse(json, status=status)


def JsonSuccessResponse(msg='Successfully done', data=None):
    return buildJsonResponse(status=200, msg=msg, data=data)


def JsonErrorResponse(msg="Bad Request"):
    return buildJsonResponse(status=400, msg=msg)


def JsonRequest(request):
    return json.loads(request.body.decode("utf-8"))


def sign_up(request):
    if (request.method != __AUTH_METHOD):
        return JsonErrorResponse()

    data = JsonRequest(request)

    try:
        email = data['email']
        name = data['name']
        password = data['password']
        Person.objects.create_user(email, name, password)
    except:
        return JsonErrorResponse('Error occurred while signing up')
    else:
        return JsonSuccessResponse('Successfully signed up')


def sign_in(request):
    if (request.method != __AUTH_METHOD):
        return JsonErrorResponse()

    data = JsonRequest(request)

    try:
        email = data['email']
        password = data['password']

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
        else:
            return JsonErrorResponse('Incorrect email or password')

    except:
        return JsonErrorResponse('Error occurred while signing in')
    else:
        return JsonSuccessResponse('Successfully signed in')


def sign_out(request):
    if (request.method != __AUTH_METHOD):
        return JsonErrorResponse()

    try:
        logout(request)
    except:
        return JsonErrorResponse('Error occurred while signing out')
    else:
        return JsonSuccessResponse('Successfully signed out')


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

    def post(self, request):
        data = JsonRequest(request)

        try:
            rc = ReviewCycle.objects.create(creator=request.user, name=data['name'])
            Question.objects.create(review_cycle=rc, title=data['question']['title'], description=data['question']['description'])
            rc.reviewees.set(data['reviewees'])
        except:
            return JsonErrorResponse('Error occurred while creating a policy')
        else:
            return JsonSuccessResponse('Successfully created the policy')

    def put(self, request, policy_id=None):
        data = JsonRequest(request)

        try:
            rc = ReviewCycle.objects.get(pk=policy_id)
            rc.name = data['name']
            rc.question.title = data['question']['title']
            rc.question.description = data['question']['description']
            rc.question.save()
            rc.save()
            rc.reviewees.set(data['reviewees'])

        except:
            return JsonErrorResponse('Error occurred while updating a policy')
        else:
            return JsonSuccessResponse('Successfully updated the policy')

    def delete(self, request, policy_id=None):
        try:
            ReviewCycle.objects.filter(pk=policy_id).delete()
        except:
            return JsonErrorResponse('Error occurred while deleting a policy')
        else:
            return JsonSuccessResponse('Successfully deleted the policy')
