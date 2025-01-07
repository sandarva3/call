from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import User

def home_view(request):
    if request.method == "POST":
        print("FORM is Submitted.")
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"The username is: {username}")
        print(f"The password is: {password}")
        
    else:
        print("FORM IS NOT SUBMITTED")
    return render(request, 'login.html')


def register_view(request):
    return render(request, 'register.html')