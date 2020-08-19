import json

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views import View

from review_service.models import Person, ReviewCycle, Question

__AUTH_METHOD = 'POST'


def buildJsonResponse(status, msg=''):
    json = {'msg': msg}
    return JsonResponse(json, status=status)


def JsonSuccessResponse(msg='Successfully done'):
    return buildJsonResponse(status=200, msg=msg)


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


class PolicyAPI(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonErrorResponse('Authentication required')
        return super(PolicyAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        dummy_data = {'request': "PolicyAPI GET"}
        return JsonResponse(dummy_data)

    def post(self, request):
        data = JsonRequest(request)

        try:
            q = Question.objects.create(title=data['question']['title'], description=data['question']['description'])
            rc = ReviewCycle.objects.create(creator=request.user, name=data['name'], question=q)
            rc.reviewees.set(data['reviewees'])
        except:
            return JsonErrorResponse('Error occurred while creating a policy')
        else:
            return JsonSuccessResponse('Successfully created the policy')

    def put(self, request):
        dummy_data = {'request': "PolicyAPI PUT"}
        return JsonResponse(dummy_data)

    def delete(self, request):
        dummy_data = {'request': "PolicyAPI DELETE"}
        return JsonResponse(dummy_data)
