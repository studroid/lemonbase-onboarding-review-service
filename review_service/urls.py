from django.urls import path

from . import views

app_name = 'review_service'
urlpatterns = [
    path('account/sign_up/', views.sign_up, name='account_sign_up'),
    path('account/sign_in/', views.sign_in, name='account_sign_in'),
    path('account/sign_out/', views.sign_out, name='account_sign_out'),

    path('policy/', views.PolicyAPI.as_view(), name='policy'),
    path('policy/<int:pk>', views.PolicyAPI.as_view(), name='policy_one_argument'),
]
