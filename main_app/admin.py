from django.contrib import admin
from .models import Animal, Shelter, User
from django.contrib.auth.admin import UserAdmin

# How the admin page looks 
class MyUserAdmin(UserAdmin):
    list_display = ('email', 'fullname', 'shelter_admin', 'is_superuser',)
    search_fields = ('email', 'fullname', 'shelter_admin',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    ordering = ("fullname",) #need this to override django default of username ordering and it needs to be a tuple

admin.site.register(Animal)
admin.site.register(Shelter)
admin.site.register(User, MyUserAdmin)

