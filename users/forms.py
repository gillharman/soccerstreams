from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField

from .models import User


class customAuthForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(
        attrs={
            "class": "username auth-form-field",
            "autocomplete": "off",
            "aria-label": "Username",
            "autofocus": True
        }
    ))
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
        attrs={
            "class": "password auth-form-field",
            "autocomplete": "off",
            "aria-label": "Password"
        }
    ))


class customUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        label="First name",
        widget=forms.TextInput(
        attrs={
            "class": "name auth-form-field",
            "autocomplete": "off",
            "aria-label": "First name",
        }
    ))

    last_name = forms.CharField(
        label="Last name",
        widget=forms.TextInput(
            attrs={
                "class": "name auth-form-field",
                "autocomplete": "off",
                "aria-label": "Last name"
            }
        )
    )

    username = UsernameField(
        widget=forms.TextInput(
            attrs={
                "class": "username auth-form-field",
                "autocomplete": "off",
                "aria-label": "Username",
                "aria-describedby": "usernameHelpBlock",
                "autofocus": True
            }
        ),
        help_text="You can use letters, numbers and @/./+/-/_ characters"
    )

    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "password auth-form-field",
                "autocomplete": "off",
                "aria-label": "Password",
                "aria-describedby": "passwordHelpBlock"
            }
        ),
        help_text=password_validation.password_validators_help_texts()
    )

    password2 = forms.CharField(
        label="Confirm password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "password auth-form-field",
                "autocomplete": "off",
                "aria-label": "Confirm password"
            }
        ),
        help_text="Enter the same password as before, for verification."
    )

    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}


class UserProfileForm(forms.ModelForm):
    avatar = forms.ImageField()
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']