from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt


#online_users = []
signaling_data = {}
'''
startcall function
Takes calleID as parameter. Check If the request method is post and if the user is authenticated. get the Callee form passed id. If callee is found then 
Return some json response(not needed compulsorily though.), else return message with calle not found.
'''
@csrf_exempt
def start_call_view(request, calle_id):
    if request.method == "POST" and request.user.is_authenticated:
        callee = User.objects.filter(id=calle_id).first()
        if callee:
            # Save the caller's SDP offer
            data = json.loads(request.body)
            signaling_data[calle_id] = {"sdp": data.get("sdp"), "caller_id": request.user.id}
            return JsonResponse({"msg": "Call initiated"})
        return JsonResponse({"msg": "Callee not found"}, status=404)
    return JsonResponse({"msg": "Bad request"}, status=400)
'''
signaling server. We get json request here.
chec if the request is post and user is authenticated. get the data by loading it from json data from request.body. the data will contain the calleID, get the 
callee through that id. Get sdp and iceCandidate as well. Just sent the jsonResponse saying anything.
'''
@csrf_exempt
def signaling_server_view(request):
    global signaling_data

    if request.method == "POST" and request.user.is_authenticated:
        data = json.loads(request.body)
        callee_id = data.get("calleeID")
        caller_id = data.get("callerID")
        sdp = data.get("sdp")
        ice_candidate = data.get("iceCandidate")

        # Handle ICE Candidates
        if callee_id and ice_candidate:
            if callee_id not in signaling_data:
                signaling_data[callee_id] = {}
            if "ice_candidates" not in signaling_data[callee_id]:
                signaling_data[callee_id]["ice_candidates"] = []
            signaling_data[callee_id]["ice_candidates"].append(ice_candidate)

        # Handle SDP Exchange
        if callee_id and sdp:
            if callee_id not in signaling_data:
                signaling_data[callee_id] = {}
            signaling_data[callee_id]["sdp"] = sdp
            signaling_data[callee_id]["caller_id"] = request.user.id

        # Return data for polling
        if caller_id:
            response_data = signaling_data.get(str(caller_id), {})
            # Clear the data after sending
            if str(caller_id) in signaling_data:
                del signaling_data[str(caller_id)]
            return JsonResponse(response_data)

        return JsonResponse({'msg': 'Signaling data processed.'})
    return JsonResponse({'msg': 'Bad request.'}, status=400)


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