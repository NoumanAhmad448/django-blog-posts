from django import forms
from django.contrib.auth.password_validation import validate_password

class RegisterationForm(forms.Form):
    email = forms.EmailField(label="Enter Email",error_messages={"required": "Please enter your email"})
    first_name = forms.CharField(label="Enter First Name", max_length=300,error_messages={"required": "Please enter your first name"})
    last_name = forms.CharField(label="Enter Last Name", max_length=300,error_messages={"required": "Please enter your last name"})
    terms = forms.BooleanField(error_messages={"required": "Please accept our terms and conditions"})
    password = forms.CharField(widget=forms.PasswordInput,validators=[validate_password],label="Enter Password",
                               max_length=15,min_length=8,
                error_messages={"required": "Please enter your password",
                "min_length": "Password must be atleast 8 digits"})