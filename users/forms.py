
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class SignUpForm(UserCreationForm):
    date_of_birth=forms.CharField()

    class Meta:
        model=get_user_model()
        fields=('email','username','password1','password2', 'date_of_birth')
        field_classes={'email':forms.EmailField}
    
class SignInForm(AuthenticationForm):
    ...