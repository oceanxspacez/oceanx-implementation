from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import AbstractUser

class UserCreateForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        fields = ('username','email','password1','password2')
        # model = get_user_model()
        model = User

    def clean_email(self):
        email = self.cleaned_data.get("email")
        user_count = User.objects.filter(email=email).count()
        if user_count > 0 :
            raise forms.ValidationError("This email has already been register please reset your password.")
        return email




    # def __init__(self,*args,**kwargs):
    #     super().__init__(*args,**kwargs)
    #     self.fields['username'].label = 'Display Name'
    #     self.fields['email'].label = 'Email Address'
