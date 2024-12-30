from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


CustomUser = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser  # Use the custom user model
        fields = ("name", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.name = self.cleaned_data["name"]
        user.user_type = 'Public'
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}) 
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    

class UpdatePasswordForm(forms.Form):
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Current Password'}),
        label="Current Password",
        required=True
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}),
        label="New Password",
        required=True
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm New Password'}),
        label="Confirm New Password",
        required=True
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password != confirm_password:
            raise forms.ValidationError("New passwords do not match.")

        return cleaned_data
