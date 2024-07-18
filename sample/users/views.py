from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.
class UserCreate(APIView):
    def post(self,request):
        username=request.data['username']
        password=request.data['passw']
        password=str(password)
        print(username,password)
        datas=User.objects.create_user(username=username,password=password)
        return HttpResponse("complete")

class USERAuth(APIView):
    def post(self,request):
        user=authenticate(username=request.data['username'],password=request.data['passw'])
        print(user)
        login(request,user)
        logout(request)
        return HttpResponse("verify")

