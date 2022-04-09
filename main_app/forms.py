from django import forms 
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import authenticate
from .models import User, Animal, Shelter
from django.contrib.auth.hashers import make_password

class SignUpForm(UserCreationForm): 
    email = forms.EmailField(max_length = 250)
    fullname = forms.CharField(max_length=250)

    class Meta: 
        model = User
        fields = ('email', 'fullname', 'password1', 'password2', 'shelter_admin' )
        labels = {'shelter_admin': "Click here if you are a shelter employee",}

    def clean_email(self):
        email = self.cleaned_data['email'].lower() #greenemail matches html tag name 
        try:
            user = User.objects.get(email=email)
        
        except Exception as e: 
            return email
        raise forms.ValidationError(f"Email {email} is already in use")


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

class DateInput(forms.DateInput): 
    input_type='date'

class AnimalCreationForm(forms.ModelForm): 

    class Meta: 
        model = Animal
        fields = ['name', 'type', 'breed', 'age', 'sex', 'weight', 'shelter', 'day_entered', 'due_date', 'description', 'image']
        widgets = {
            'day_entered': DateInput(),
            'due_date': DateInput(),
        }
     
    
   