from django import forms 
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import authenticate
from .models import User

# class SignUpForm(UserCreationForm): 
#     email = forms.EmailField(max_length = 250, help_text = "Required")
#     shelter_admin = forms.BooleanField()

#     class Meta: 
#         model = User
#         fields = ('email', 'fullname', 'password1', 'password2', 'shelter_admin' )

#     def clean_email(self):
#         email = self.cleaned_data['email'].lower() #greenemail matches html tag name 
#         try:
#             user = User.objects.get(email=email)
        
#         except Exception as e: 
#             return email
#         raise forms.ValidationError(f"Email {email} is already in use")

class SignUpForm(forms.ModelForm): 
    password = forms.CharField(label = 'Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta: 
        model = User
        fields = ['email', 'fullname', 'shelter_admin', 'password', 'password2']
    
    def clean_email(self):
        #verify email is available 
        email = self.cleaned_data.get('email').lower()
        emailsearch = User.objects.filter(email=email)
        if emailsearch.exists(): 
            raise forms.ValidationError("Email is already in use")
        return email 
    
    def clean(self):
        #Verify passwords match
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password is not None and password != password2: 
            self.add_error("password2", "Passwords must match")
        return cleaned_data


class LogInForm(forms.ModelForm): 
    password = forms.CharField(label = 'Password', widget=forms.PasswordInput)

    class Meta: 
        model = User
        fields = ['email', 'password']
    
    def clean(self): 
        if self.is_valid(): 
            email = self.cleaned_data.get('email').lower()
            password = self.cleaned_data.get('password')
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Email or password not correct")