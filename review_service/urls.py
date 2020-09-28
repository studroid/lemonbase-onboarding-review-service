from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register(r'policy', views.PolicyAPI, basename='policy')

app_name = 'review_service'
urlpatterns = [
    path('account/sign_up/', views.sign_up, name='account_sign_up'),
    path('account/sign_in/', views.sign_in, name='account_sign_in'),
    path('account/sign_out/', views.sign_out, name='account_sign_out'),

    path('', include(router.urls)),
]
