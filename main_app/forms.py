from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import User

class SignUpForm(UserCreationForm): 
    email = forms.EmailField(max_length = 250, help_text = "Required")
    shelter_admin = forms.BooleanField()

    class Meta: 
        model = User
        fields = ('email', 'fullname', 'password1', 'password2', 'shelter_admin' )

    def clean_email(self):
        email = self.cleaned_data['email'].lower() #greenemail matches html tag name 
        try:
            user = User.objects.get(email=email)
        
        except Exception as e: 
            return email
        raise forms.ValidationError(f"Email {email} is already in use")