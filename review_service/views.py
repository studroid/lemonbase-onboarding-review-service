from django.http import JsonResponse
from django.shortcuts import render
from django.views import View


def sign_up(request):
    dummy_data = {'request': "SIGN UP"}
    return JsonResponse(dummy_data)


def sign_in(request):
    dummy_data = {'request': "SIGN IN"}
    return JsonResponse(dummy_data)


def sign_out(request):
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
