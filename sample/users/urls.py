from django.contrib import admin
from django.urls import path
from users import views

urlpatterns = [
   path('auth/',views.UserCreate.as_view()),
   path('authverify/',views.USERAuth.as_view())
]
