from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def index(request):
    return render(request, 'ecosphere/index.html')

def login_view(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            error_message = 'Invalid username or password'
    return render(request, 'ecosphere/index.html', {'error_message': error_message})
# Create your views here.
