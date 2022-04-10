from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('about/', views.About.as_view(), name="about"),
    path('dogs/', views.DogList.as_view(), name="dog_list"),
    path('cats/', views.CatList.as_view(), name="cat_list"),
    path('paws/new/', views.AnimalCreate.as_view(), 
    name="paws_create"),
    path('paws/<int:pk>', views.AnimalDetail.as_view(), name="paws_detail"),
    path('paws/<int:pk>/update', views.AnimalUpdate.as_view(), name="animal_update"),
    path('paws/<int:pk>/delete', views.AnimalDelete.as_view(), name="animal_delete"),
    path('shelters/', views.ShelterList.as_view(), name="shelter_list"),
    path('shelter/new/', views.ShelterCreate.as_view(), name="shelter_create"),
    path('shelter/<int:pk>', views.ShelterDetail.as_view(), name="shelter_detail"),
    path('shelter/<int:pk>/update', views.ShelterUpdate.as_view(), name="shelter_update"),
    path('shelter/<int:pk>/delete', views.ShelterDelete.as_view(), name="shelter_delete"),
    path('signup/', views.signup_view, name="signup"), 
    path('login/', views.login_view, name="login"), 
    path('logout/', views.logout_view, name="logout"), 
    path('user/<int:id>/', views.profile, name="profile"),
    # path('profile/favorites/', views.favorite_list, name = "favorite_list"),
    path('fav/<int:id>/', views.favorite_add, name="favorite_add"), 



]