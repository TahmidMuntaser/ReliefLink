from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from .forms import SignUpForm

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
            return redirect('dashboard')  
        else:
            return render(request, 'home/login.html', {'error': 'Invalid credentials'})
    return render(request, 'home/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')  

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  
            user.set_password(form.cleaned_data['password'])
            user.save()
            role = form.cleaned_data['role']
            group = Group.objects.get(name=role)
            user.groups.add(group)
    
            return redirect('signup_success')
    else:
        form = SignUpForm()
    return render(request, 'home/signup.html', {'form': form})

def signup_success(request):
    return render(request, 'home/signup_success.html')

@login_required
def dashboard(request):
    user = request.user
    if user.groups.filter(name='DC').exists():
        return redirect('dc_dashboard')
    elif user.groups.filter(name='UNO').exists():
        return redirect('uno_dashboard')
    else:
        return redirect('public_dashboard')

@login_required
def dc_dashboard(request):
    return render(request, 'home/dc_dashboard.html')

@login_required
def uno_dashboard(request):
    return render(request, 'home/uno_dashboard.html')

@login_required
def public_dashboard(request):
    return render(request, 'home/public_dashboard.html')