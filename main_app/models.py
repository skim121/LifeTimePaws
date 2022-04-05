from django.db import models
from django.contrib.auth.models improt AbstractBaseUser, BaseUserManager

class User(AbstractBaseUser): 
    email = models.EmailField(verbose_name = "email", max_length=250, unique = True) 
    fullname = models.CharField(max_length = 250)
    shelter_admin = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname']

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
    days_in_shelter = models.IntegerField()
    days_left = models.IntegerField()
    description = models.CharField(max_length=250) 
    image = models.ImageField(null = True, blank = True, upload_to="images/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


