# ReliefLink/home/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'home/index.html')

def service(request):
    return render(request, 'home/service.html')

def contact(request):
    return render(request, 'home/contact.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'home/login.html', {'error': 'Invalid credentials'})
    return render(request, 'home/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    user = request.user
    if user.is_superuser:
        return redirect('superuser_dashboard')
    elif user.groups.filter(name='DC').exists():
        return redirect('dc_dashboard')
    elif user.groups.filter(name='UNO').exists():
        return redirect('uno_dashboard')
    else:
        return redirect('public_dashboard')