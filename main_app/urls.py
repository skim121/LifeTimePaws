from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('dogs/', views.DogList.as_view(), name="dog_list"),
    path('cats/', views.CatList.as_view(), name="cat_list"),
    path('paws/new/', views.AnimalsCreate.as_view(), 
    name="paws_create"),
    # path('dogs/<int:pk>', views.DogsDetail.as_view(), name="dogs_detail")



]