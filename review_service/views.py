import json

from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views import View

from review_service.models import Person

__AUTH_METHOD = 'POST'


def __buildJsonResponse(status, msg=''):
    json = {'msg': msg}
    return JsonResponse(json, status=status)


def __JsonSuccessResponse(msg='Successfully done'):
    return __buildJsonResponse(status=200, msg=msg)


def __JsonErrorResponse(msg="Bad Request"):
    return __buildJsonResponse(status=400, msg=msg)


def __JsonRequest(request):
    return json.loads(request.body.decode("utf-8"))


def sign_up(request):
    if (request.method != __AUTH_METHOD):
        return __JsonErrorResponse()

    data = __JsonRequest(request)

    try:
        email = data['email']
        name = data['name']
        password = data['password']
        Person.objects.create_user(email, name, password)
    except:
        return __JsonErrorResponse('Error occurred while signing up')
    else:
        return __JsonSuccessResponse('Successfully signed up')


def sign_in(request):
    if (request.method != __AUTH_METHOD):
        return __JsonErrorResponse()

    data = __JsonRequest(request)

    try:
        email = data['email']
        password = data['password']

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
        else:
            return __JsonErrorResponse('Incorrect email or password')

    except:
        return __JsonErrorResponse('Error occurred while signing in')
    else:
        return __JsonSuccessResponse('Successfully signed in')


def sign_out(request):
    if (request.method != __AUTH_METHOD):
        return __JsonErrorResponse()

    dummy_data = {'request': "SIGN OUT"}
    return JsonResponse(dummy_data)


class PolicyAPI(View):
    def get(self, request):
        dummy_data = {'request': "PolicyAPI GET"}
        return JsonResponse(dummy_data)

    def post(self, request):
        dummy_data = {'request': "PolicyAPI POST"}
        return JsonResponse(dummy_data)

    def put(self, request):
        dummy_data = {'request': "PolicyAPI PUT"}
        return JsonResponse(dummy_data)

    def delete(self, request):
        dummy_data = {'request': "PolicyAPI DELETE"}
        return JsonResponse(dummy_data)
