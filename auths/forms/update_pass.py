
from django import forms
from django.contrib.auth.password_validation import validate_password

class UpdatePassForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput,validators=[validate_password],
                               max_length=15,min_length=8,
                error_messages={"required": "Please enter your new password",
                "min_length": "Password must be atleast 8 digits",
                "max_length": "Password must not exceed 15 digits"}
                )

    c_password = forms.CharField(widget=forms.PasswordInput,validators=[validate_password],
                               max_length=15,min_length=8,
                error_messages={"required": "Please enter confirm password",
                "min_length": "Password must be atleast 8 digits",
                "max_length": "Password must not exceed 15 digits"}
                )