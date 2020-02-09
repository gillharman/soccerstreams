from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm, UsernameField

from .models import User


class CustomAuthForm(AuthenticationForm):
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
        )
    )


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Old password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "password auth-form-field",
                "ng-model": "$scope.old_password",
                "autocomplete": "off",
                "aria-label": "Old password",
                "autofocus": True
            }
        )
    )

    new_password1 = forms.CharField(
        label="New password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "password auth-form-field",
                "ng-model": "$scope.new_password1",
                "autocomplete": "off",
                "aria-label": "New password",
                "aria-describedby": "passwordHelpBlock"
            }
        ),
        help_text=password_validation.password_validators_help_texts(),
    )

    new_password2 = forms.CharField(
        label="New password confirmation",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "password auth-form-field",
                "ng-model": "$scope.new_password2",
                "autocomplete": "off",
                "aria-label": "New password confirmation"
            }
        )
    )


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        label="First name",
        widget=forms.TextInput(
            attrs={
                "class": "name auth-form-field",
                "autocomplete": "off",
                "aria-label": "First name",
            }
        )
    )

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


class UserProfileForm(forms.Form):
    avatar = forms.ImageField(
        label="Click to select",
        widget=forms.ClearableFileInput(
            attrs={
                "class": "file-selector-input",
            }),
        allow_empty_file=True,
        required=False
    )

    first_name = forms.CharField(
        label="First name",
        widget=forms.TextInput(
            attrs={
                "class": "user-profile-field auth-form-field",
                "autocomplete": "off",
                "aria-label": "First name",
                "placeholder": "First name (Required)"
            }
        )
    )

    last_name = forms.CharField(
        label="Last name",
        widget=forms.TextInput(
            attrs={
                "class": "user-profile-field auth-form-field",
                "autocomplete": "off",
                "aria-label": "Last name",
                "placeholder": "Last name (Required)"
            }
        )
    )

    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "class": "user-profile-field auth-form-field",
                "autocomplete": "off",
                "aria-label": "Email",
                "placeholder": "Email address"
            }
        ),
        required=False
    )
