from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('dogs/', views.DogList.as_view(), name="dog_list"),
    path('cats/', views.CatList.as_view(), name="cat_list"),
    path('paws/new/', views.AnimalsCreate.as_view(), 
    name="paws_create"),
    path('paws/<int:pk>', views.AnimalDetail.as_view(), name="paws_detail"),
    path('paws/<int:pk>/update', views.AnimalUpdate.as_view(), name="animal_update"),
    path('paws/<int:pk>/delete', views.AnimalDelete.as_view(), name="animal_delete"),



]