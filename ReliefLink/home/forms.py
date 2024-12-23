# home/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import DeputyCommissionar, DivisionalCommissionar, District

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class AssignDeputyCommissionarForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=True, label='Enter Name')

    email = forms.EmailField(required=True, label='Enter Mail')
    district = forms.ModelChoiceField(
        queryset=District.objects.all(),
        label="Select District"
    )
    class Meta:
        model = DeputyCommissionar
        fields = ['district', 'name', 'email']


class UpdatePasswordForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password != confirm_password:
            raise forms.ValidationError("New passwords do not match.")
