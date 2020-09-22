from django.urls import path
from UserApp import views

urlpatterns = [
    path('login/', views.login, name='login'),

    path('vcore/', views.phone_vcore, name='vcore'),

]
