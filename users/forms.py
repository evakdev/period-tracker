
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from datetime import datetime

class RegisterForm(UserCreationForm):
    date_widget = forms.SelectDateWidget(years=range(datetime.now().year -100,datetime.now().year-10))
    date_of_birth = forms.DateField(widget=date_widget)
    class Meta:
        model=get_user_model()
        fields=('email','username','password1','password2', 'date_of_birth')
        #field_classes={'email':forms.EmailField}
    
class LoginForm(AuthenticationForm):
    ...