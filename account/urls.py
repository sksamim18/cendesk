from django.urls import path
from account import views


urlpatterns = [
    path('login/', views.authentication, name='login'),
    path('register/', views.registration, name='register'),
    path('confirm_otp/', views.confirm_otp, name='confirm_otp'),
    path('upload_docs/', views.upload_docs, name='upload_docs'),
    path('logout/', views.sign_out, name='sign_out')
]
