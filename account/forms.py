from django import forms
from .models import Account

class RegisterForm(forms.ModelForm):

    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter Password',
        'class':'form-control'
    }))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Confirm Password',
        'class':'form-control'
    }))
    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter Password',
        'class':'form-control'
    }))
    email=forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder':'Enter Email',
        'class':'form-control'
    }))
    first_name=forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Enter first name',
        'class':'form-control'
    }))
    last_name=forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Enter last name',
        'class':'form-control'
    }))
    phone_number=forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Enter Phone Number',
        'class':'form-control'
    }))

    
    class Meta:
        model = Account
        fields = ("first_name",'last_name','email',"phone_number",'password')

    class UserForm(forms.ModelForm):
        class Meta:
            model=Account
            fields=['first_name','last_name','phone_number']

