from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "p-2 border rounded"}),
            "email": forms.EmailInput(attrs={"class": "p-2 border rounded"}),
            "first_name": forms.TextInput(attrs={"class": "p-2 border rounded"}),
            "last_name": forms.TextInput(attrs={"class": "p-2 border rounded"}),
        }


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "password1",
            "password2",
        ]
