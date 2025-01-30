from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Replace 'dashboard' with your desired URL
            else:
                form.add_error(None, 'Invalid credentials.')

    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return render(request, 'account/logged_out.html')



def register_view(request):
    registration_status = None
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            registration_status = 'success'
        else:
            registration_status = 'fail'
    else:
        form = UserCreationForm()
    return render(request, 'account/register.html', {
        'form': form,
        'registration_status': registration_status
    })
    
@login_required
def updatepassword_view(request):
    if request.method == 'POST':
        form = UpdatePasswordForm(request.POST)
        if form.is_valid():
            current_password = form.cleaned_data['current_password']
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']

            # Check if the current password is correct
            if not request.user.check_password(current_password):
                form.add_error('current_password', 'Incorrect current password.')
            elif new_password != confirm_password:
                form.add_error('confirm_password', 'New passwords do not match.')
            else:
                # Update the user's password
                user = request.user
                user.set_password(new_password)
                user.save()

                # Keep the user logged in after password change
                update_session_auth_hash(request, user)

                # Provide feedback to the user
                messages.success(request, 'Your password was successfully updated!')
                return redirect('home') 

    else:
        form = UpdatePasswordForm()
    return render(request, 'account/updatepassword.html', {'form': form})


@login_required
def delete_user_view(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        user.delete()
        messages.success(request, f"User '{user.name}' has been successfully deleted.")
    return redirect('dashboard')

@login_required
def add_user_view(request):
    if request.user.user_type == 'Admin':
        return redirect('add_divisionalcommissioner')
    
    elif request.user.user_type == 'DivisionalCommissioner':
        return redirect('add_deputycommissioner')
    
    elif request.user.user_type == 'DeputyCommissioner':
        return redirect('add_uno')
    
    elif request.user.user_type == 'UNO':
        return redirect('add_unionchairman')
    
    elif request.user.user_type == 'UnionChairman':
        return redirect('add_wardmember')
    
    elif request.user.user_type == 'WardMember':
        return redirect('add_house')



@login_required
def add_divisionalcommissioner_view(request):
    if request.method == 'POST':
        form = AddDivisionalCommissionerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = AddDivisionalCommissionerForm()
    return render(request, 'account/addDivisionalCommissioner.html', {'form': form})



@login_required
def add_deputycommissioner_view(request):
    if request.method == 'POST':
        form = AddDeputyCommissionerForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = AddDeputyCommissionerForm(user=request.user)

    return render(request, 'account/addDeputyCommissioner.html', {'form': form})



@login_required
def add_uno_view(request):
    if request.method == 'POST':
        form = AddUNOForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = AddUNOForm(user=request.user)
    return render(request, 'account/addUNO.html', {'form': form})


@login_required
def add_unionchairman_view(request):
    if request.method == 'POST':
        form = AddUnionChairmanForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = AddUnionChairmanForm(user=request.user)
    return render(request, 'account/addUnionChairman.html', {'form': form})



@login_required
def add_wardmember_view(request):
    if request.method == 'POST':
        form = AddWardMemberForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = AddWardMemberForm(user=request.user)
    return render(request, 'account/addWardMember.html', {'form': form})



@login_required
def add_house_view(request):
    if request.method == 'POST':
        form = AddHouseForm(request.POST)
        if form.is_valid():
            house = form.save(commit=False)  # Create the instance but don't save it yet
            house.ward = request.user.ward  # Set the ward to user's ward
            house.save()  # Now save the instance
            return redirect('dashboard')
    else:
        form = AddHouseForm()
    return render(request, 'account/addHouse.html', {'form': form})


@login_required
def delete_house_view(request, house_id):
    if request.method == 'POST':
        house = get_object_or_404(Housh, id=house_id)
        house.delete()
        messages.success(request, f"House '{house.holding_number}' has been successfully deleted.")
    return redirect('dashboard')

@login_required
def born_view(request, house_id):
    if request.method == 'POST':
        house = get_object_or_404(Housh, id = house_id)
        house.family_member += 1
        house.save()
    return redirect('dashboard')

@login_required
def death_view(request, house_id):
    if request.method == 'POST':
        house = get_object_or_404(Housh, id = house_id)
        house.family_member -= 1
        house.save()
    return redirect('dashboard')