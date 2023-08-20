from django import forms
from django.contrib.auth.password_validation import validate_password

class LoginForm(forms.Form):
    email = forms.EmailField(label="Enter Email",error_messages={"required": "Please enter your email"})
    password = forms.CharField(widget=forms.PasswordInput,validators=[validate_password],label="Enter Password",
                               max_length=15,min_length=8,
                error_messages={"required": "Please enter your password",
                "min_length": "Password must be atleast 8 digits"})