from django.shortcuts import render
from django.views import View 
from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse 
from .models import Animal
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator 

class Home(TemplateView):
    template_name = "home.html"

class DogList(TemplateView): 
    template_name = "doglist.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dogs"] = Animal.objects.filter(type='dog')
        return context

class AnimalsCreate(CreateView):
    model = Animal
    fields = ['name', 'type', 'breed', 'age', 'sex', 'weight', 'days_in_shelter', 'days_left', 'description', 'img']
    template_name = 'animal_create.html'
    success_url = "/dogs/"
    