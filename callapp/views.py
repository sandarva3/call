from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User

#online_users = []

def home_view(request):
    if request.method == "POST":

        print("Login FORM is Submitted.")
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("LOGGED In")
            msg = "You're currently Logged in."
            users = User.objects.all()
            #print(f"The users are: {users}")
            #global online_users
            #online_users.append(user.id)
            #print(f"THE ID OF THIS USER IS: {online_users}")
            #print(f"TOTAL ONLINE USERS: {online_users}")
            context = {
                'loginMsg': msg,
                'users': users
            }
            return render(request, 'homepage.html', context)
        else:
            msg = "Invalid username and password."
            return render(request, 'login.html', {'msg': msg})
    else:
        print("FORM IS NOT SUBMITTED")
        return render(request, 'login.html')



def register_view(request):
    if request.method == "POST":
        print("Register FORM is submitted.")

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        if password != confirm_password:
            msg = "Two password fields didn't matched."
            return render(request, 'register.html', {'msg': msg})
        
        if User.objects.filter(username=username).exists():
            msg = "User with that username already exists."
            return render(request, 'register.html', {'msg': msg})
        
        user = User.objects.create_user(username=username, email=email, password=password)
        print("New user created.")
        print(f"And the id is: {user.id}")
        return redirect('home')
    
    return render(request, 'register.html')


'''
this function will get executed when user clicks on logut. Here we take reqeust as parameter, and we pass it to logout() from django.contrib.auth
'''
def logout_view(request):
    logout(request)
    print("LOGGING OUT User")
    return redirect('home')