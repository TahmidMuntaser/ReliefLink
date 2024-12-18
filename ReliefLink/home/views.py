from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User, Group
from .forms import SignUpForm

def index(request):
    return render(request, 'home/index.html')

def service(request):
    return render(request, 'home/service.html')

def contact(request):
    return render(request, 'home/contact.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        subject = f"New Contact Form Submission from {name}"
        message_body = (
            f"Dear Admin,\n\n"
            f"You have received a new message from the contact form on your website.\n\n"
            f"Details:\n"
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Message:\n{message}\n\n"
            f"Best regards,\n"
            f"ReliefLink Team"
        )
        from_email = settings.EMAIL_HOST_USER
        recipient_list = ['labr1t18203@gmail.com']

        try:
            send_mail(subject, message_body, from_email, recipient_list)
            return render(request, 'home/contact_success.html')
        except Exception as e:
            return render(request, 'home/contact.html', {'error': 'Error sending email. Please try again later.'})

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