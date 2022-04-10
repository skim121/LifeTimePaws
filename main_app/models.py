from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from ckeditor.fields import RichTextField


#This is repeatitive on purpose - there is a shorter way to write this (with base function and other functions to pass in data) but it is not advisable to pass in password information directly. Passing in password would make it bypass encryption and make the user account less secure.
class MyUserManager(BaseUserManager): 
    def create_user(self, email, fullname, shelter_admin, password=None): 
        if not email: 
            raise ValueError("Users must enter an email address")
        if not fullname: 
            raise ValueError("Users must enter a name")
        user = self.model(
            email=self.normalize_email(email),
            fullname = fullname, 
            shelter_admin = False,
        )
        user.set_password(make_password(password))
        user.save(using=self._db)
        return user
    
    def create_shelter_user(self, email, fullname, shelter_admin, password=None): 
        if not email: 
            raise ValueError("Users must enter an email address")
        if not fullname: 
            raise ValueError("Users must enter a name")
        user = self.model(
            email=self.normalize_email(email),
            fullname = fullname, 
            shelter_admin = True,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
        
    def create_superuser(self, email, fullname, shelter_admin, is_admin, is_staff, is_superuser, password=None): 
        if not email: 
            raise ValueError("Users must enter an email address")
        if not fullname: 
            raise ValueError("Users must enter a name")
        user = self.model(
            email=self.normalize_email(email),
            fullname = fullname, 
            shelter_admin = True,
            is_admin = True, 
            is_staff = True,
            is_superuser = True,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser): 
    email = models.EmailField(verbose_name = "email", max_length=250, unique = True) 
    fullname = models.CharField(max_length = 250)
    shelter_admin = models.BooleanField(default=False, blank=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname', 'shelter_admin', 'is_admin', 'is_staff', 'is_superuser']

    def __str__(self): 
        return self.fullname
    
    def has_perm(self, perm, obj=None): 
        return self.is_admin

    def has_module_perms(self, app_label): 
        return True
    


KILL_CHOICES = (
    ("kill", "kill"),
    ("no-kill", "no-kill"),
)

class Shelter(models.Model):
    name = models.CharField(max_length=250)
    location = models.CharField(max_length=250)
    kill = models.CharField(max_length=10, choices = KILL_CHOICES)
    website = models.CharField(max_length=250)
    image = models.ImageField(null = True, blank = True, upload_to="images/")
    

    def __str__(self):
        return self.name


TYPE_CHOICES = (
    ("dog", "dog"),
    ("cat", "cat"),
)

SEX_CHOICES = (
    ("female", "female"),
    ("male", "male")
)

class Animal(models.Model):
    type = models.CharField(max_length=100, choices = TYPE_CHOICES)
    name = models.CharField(max_length=250)
    breed = models.CharField(max_length=250)
    age = models.IntegerField()
    sex = models.CharField(max_length=10, choices = SEX_CHOICES)
    weight = models.IntegerField()
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE)
    day_entered = models.DateField()
    due_date = models.DateField(blank=True)
    # description = models.CharField(max_length=250, blank=True) 
    description = RichTextField(blank=True, null=True)
    image = models.ImageField(null = True, blank = True, upload_to="images/")
    created_at = models.DateTimeField(auto_now_add=True)
    favorites = models.ManyToManyField(User, default=None, blank=True )

    def __str__(self):
        return self.name


