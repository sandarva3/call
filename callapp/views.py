from django.shortcuts import render, HttpResponse

# Create your views here.

def http(request):
    print("HELLo")
    return render(request, 'index.html')