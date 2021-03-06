from django.shortcuts import render, get_object_or_404
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
from .forms import SignUpForm, LogInForm, AnimalCreationForm, AnimalUpdateForm

User = get_user_model()

class Home(TemplateView):
    template_name = "home.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["paws"] = Animal.objects.order_by('due_date')[:5]
    
        return context

class About(TemplateView):
    template_name="about.html"


class DogList(TemplateView): 
    template_name = "doglist.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name")
        if name!=None: 
            context["dogs"] = Animal.objects.filter(type="dog", name__icontains=name)
            context["header"]=f"Search results for {name}..."
        else: 
            context["dogs"] = Animal.objects.filter(type='dog')
            context["header"] = "Available Dogs"
        return context

class CatList(TemplateView): 
    template_name = "catlist.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name")
        if name!=None: 
            context["cats"] = Animal.objects.filter(type="cat", name__icontains=name)
            context["header"]=f"Search results for {name}..."
        else: 
            context["cats"] = Animal.objects.filter(type='cat')
            context["header"] = "Available Cats"
        return context

@method_decorator(login_required, name='dispatch')
class AnimalCreate(CreateView):
    model = Animal
    form_class = AnimalCreationForm 
    template_name = 'animal_create.html'
    def get_success_url(self): 
        return reverse('paws_detail', kwargs={'id': self.object.id})

def AnimalDetail(request, id):
    animal = get_object_or_404(Animal, id=id)
    animals  = Animal.objects.filter( favorites = request.user.id)
    is_fav = False
    if animal in animals:
        is_fav = True
    return render(request, 'paws_detail.html', {'animal': animal, 'is_fav': is_fav}) 


@method_decorator(login_required, name='dispatch')
class AnimalUpdate(UpdateView): 
    model = Animal
    form_class = AnimalUpdateForm
    # fields = ['name', 'type', 'breed', 'age', 'sex', 'weight', 'shelter', 'day_entered', 'due_date', 'description', 'image']
    template_name = "animal_update.html"
    def get_success_url(self): 
        return reverse('paws_detail', kwargs={'id': self.object.id})

@method_decorator(login_required, name='dispatch')
class AnimalDelete(DeleteView): 
    model = Animal
    template_name = "animal_delete_confirm.html"
    success_url = "/"
    # def get(self,request, *args, **kwargs): 
    #     return self.post(request, *args, **kwargs)



class ShelterList(TemplateView):
    template_name = "shelter_list.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name")
        if name!=None: 
            context["shelters"] = Shelter.objects.filter(name__icontains=name)
            context["header"]=f"Search results for {name}..."
        else: 
            context["shelters"] = Shelter.objects.all()
            context["header"] = "Shelters Participating"
        return context


# class ShelterDetail(DetailView): 
#     model = Shelter
#     template_name = "shelter_detail.html"

def ShelterDetail(request, id):
    shelter = get_object_or_404(Shelter, id=id)
    animals  = Animal.objects.filter( shelter = shelter)
    return render(request, 'shelter_detail.html', {'shelter': shelter, 'animals': animals}) 

@method_decorator(login_required, name='dispatch')
class ShelterCreate(CreateView): 
    model = Shelter
    fields = ['name', 'location', 'kill', 'website', 'image']
    template_name = 'shelter_create.html'
    def get_success_url(self): 
        return reverse('shelter_detail', kwargs={'id': self.object.id})

@method_decorator(login_required, name='dispatch')
class ShelterUpdate(UpdateView): 
    model = Shelter
    fields = ['name', 'location', 'kill', 'website', 'image']
    template_name = "shelter_update.html"
    def get_success_url(self): 
        return reverse('shelter_detail', kwargs={'id': self.object.id})

@method_decorator(login_required, name='dispatch')
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

def signup_view(request, backend='django.contrib.auth.backends.ModelBackend'):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return HttpResponseRedirect('/login/') 
            #login function not working therefore have to redirect user to login again after signing up 
        else:
            return render(request, 'signup.html', {'form': form})

    else:
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})

def logout_view(request): 
    logout(request)
    return HttpResponseRedirect('/')

def login_view(request): 
    # if POST, then authenticate the user (submitting the username and password)
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            e = form.cleaned_data.get('email')
            p = form.cleaned_data.get('password')
            user = authenticate(email = e, password = p)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    print('The account has been disabled')
                    return HttpResponseRedirect('/login')
        else: 
            return render(request, 'login.html', {'form': form})     

    else:
        # user is going to the login page
        form = LogInForm()
        return render(request, 'login.html', {'form': form})    

@login_required
def profile(request, id):
    # user = User.objects.get(id=id)
    fav_list = Animal.objects.filter(favorites=request.user)
    return render(request, 'profile.html', {'fav':fav_list, 'id' : request.user.id})

@login_required
def favorite_add(request, id): 
    animal = get_object_or_404(Animal, id=id)
    if animal.favorites.filter(id=request.user.id).exists():
        animal.favorites.remove(request.user)   
    else:
        animal.favorites.add(request.user)
    # return HttpResponseRedirect('/user/'+str(request.user.id))
    return HttpResponseRedirect('/paws/'+str(animal.id))

