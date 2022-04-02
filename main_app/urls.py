from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('dogs/', views.DogList.as_view(), name="dog_list"),
    path('paws/new/', views.AnimalsCreate.as_view(), name="paws_create")


]