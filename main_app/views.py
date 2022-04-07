from django.shortcuts import render
from django.views import View 
from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse 
from .models import Animal, Shelter
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.backends import ModelBackend
from django.utils.decorators import method_decorator 
from django.shortcuts import render, redirect
from .forms import SignUpForm

class Home(TemplateView):
    template_name = "home.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["paws"] = Animal.objects.all()
        return context

class DogList(TemplateView): 
    template_name = "doglist.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dogs"] = Animal.objects.filter(type='dog')
        return context

class CatList(TemplateView): 
    template_name = "catlist.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["paws"] = Animal.objects.filter(type='cat')
        return context

class AnimalCreate(CreateView):
    model = Animal
    fields = ['name', 'type', 'breed', 'age', 'sex', 'weight', 'shelter', 'days_in_shelter', 'days_left', 'description', 'image']
    template_name = 'animal_create.html'
    # success_url = "/dogs/"
    def get_success_url(self): 
        return reverse('paws_detail', kwargs={'pk': self.object.pk})
    
class AnimalDetail(DetailView):
    model = Animal
    template_name = "paws_detail.html"

class AnimalUpdate(UpdateView): 
    model = Animal
    fields = ['name', 'type', 'breed', 'age', 'sex', 'weight', 'shelter', 'days_in_shelter', 'days_left', 'description', 'image']
    template_name = "animal_update.html"
    def get_success_url(self): 
        return reverse('paws_detail', kwargs={'pk': self.object.pk})

class AnimalDelete(DeleteView): 
    model = Animal
    template_name = "animal_delete_confirm.html"
    success_url = "/"

class ShelterList(TemplateView):
    template_name = "shelter_list.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["shelters"] = Shelter.objects.all()
        return context
class ShelterDetail(DetailView): 
    model = Shelter
    template_name = "shelter_detail.html"

class ShelterCreate(CreateView): 
    model = Shelter
    fields = ['name', 'location', 'kill', 'website', 'image']
    template_name = 'shelter_create.html'
    def get_success_url(self): 
        return reverse('shelter_detail', kwargs={'pk': self.object.pk})


class ShelterUpdate(UpdateView): 
    model = Shelter
    fields = ['name', 'location', 'kill', 'website', 'image']
    template_name = "shelter_update.html"
    def get_success_url(self): 
        return reverse('shelter_detail', kwargs={'pk': self.object.pk})

class ShelterDelete(DeleteView): 
    model = Shelter
    template_name = "shelter_delete_confirm.html"
    success_url = "/shelters/"

#logging into admin site with case insensitive email 
class CaseInsensitiveModelBackend(ModelBackend): 
    def authenticate(self, request, username = None, password = None, **kwargs):
        UserModel = get_user_model()
        if username is None: 
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try: 
            case_insensitive_username_field = '{}__iexact'.format(UserModel.USERNAME_FIELD)
            user = UserModel._default_manager.get(**{case_insensitive_username_field:username})
        except UserModel.DoesNotExist: 
            UserModel().set_password(password)
        else: 
            if user.check_password(password) and self.user_can_authenticate(user): 
                return user

def signup_view(request, *args, **kwargs): 
    user = request.user
    if user.is_authenticated:
        return HttpResponse (f"You are already authenticated")
    context = {}

    if request.POST:
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email= email, password = raw_password)
            login(request, user)
            destination = kwargs.get("next")
            if destination: 
                return redirect (destination)
            return redirect ('home')
        else: 
            context['signup_form'] = form

    return render(request, 'signup.html', context) 

