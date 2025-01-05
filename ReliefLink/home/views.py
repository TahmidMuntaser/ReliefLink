# home/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import Housh
from django.contrib.auth import get_user_model
from .forms import *

User = get_user_model()

def can_add_user(user):
    return user.has_perm('home.can_add_user')

def can_remove_user(user):
    return user.has_perm('home.can_remove_user')


def index(request):
    return render(request, 'home/index.html')

def service(request):
    return render(request, 'home/service.html')

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


@login_required
def dashboard(request):
    user = request.user
    role = user.user_type
    if role == 'DivisionalCommissioner':
        return redirect('divisionalcommissioner_dashboard')
    
    elif role == 'Admin':
        return redirect('admin_dashboard')
    
    elif role == 'DeputyCommissioner':
        return redirect('deputycommissioner_dashboard')
    
    elif role == 'UNO':
        return redirect('uno_dashboard')
    
    elif role == 'UnionChairman':
        return redirect('unionchairman_dashboard')
    
    elif role == 'WardMember':
        return redirect('wardmember_dashboard')
    
    elif role == 'Public':
        return redirect('public_dashboard')
    
@login_required
def admin_dashboard(request):
    data = User.objects.filter(user_type='DivisionalCommissioner')
    return render(request, 'home/admin_dashboard.html', {'data': data})

@login_required
def divisionalcommissioner_dashboard(request):
    data = User.objects.filter(user_type='DeputyCommissioner', district__division = request.user.division)

    return render(request, 'home/divisionalcommissioner_dashboard.html', {'data':data})

@login_required
def deputycommissioner_dashboard(request):
    data = User.objects.filter(user_type='UNO', upazila__district = request.user.district)

    return render(request, 'home/deputycommissioner_dashboard.html', {'data':data})


@login_required
def uno_dashboard(request):
    data = User.objects.filter(user_type='UnionChairman', union__upazila = request.user.upazila)

    return render(request, 'home/uno_dashboard.html', {'data':data})

@login_required
def unionchairman_dashboard(request):
    data = User.objects.filter(user_type='WardMember', ward__union = request.user.union)

    return render(request, 'home/unionchairman_dashboard.html', {'data':data})

@login_required
def wardmember_dashboard(request):
    houses = Housh.objects.filter(ward = request.user.ward)

    return render(request, 'home/wardmember_dashboard.html', {'houses': houses})

@login_required
def public_dashboard(request):
    return render(request, 'home/public_dashboard.html')


def get_house_details(house_id):
    house = get_object_or_404(Housh.objects.select_related(
        'ward__union__upazila__district__division'
    ), id=house_id)
    return {
        "holding_number": house.holding_number,
        "ward": house.ward.name,
        "division": house.ward.union.upazila.district.division.name,
    }
