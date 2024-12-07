# home/forms.py
from django import forms
from django.contrib.auth.models import User

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=[('DC', 'District Commissioner'), ('UNO', 'UNO'), ('Public', 'Public User')])

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']