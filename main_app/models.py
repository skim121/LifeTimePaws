from django.db import models

# Create your models here.
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
    days_in_shelter = models.IntegerField()
    days_left = models.IntegerField()
    description = models.CharField(max_length=250) 
    img = models.ImageField(null = True, blank = True, upload_to="images/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


