from django.contrib import admin
from .models import Person, Cosas
from .models import User

admin.site.register(Person) 
admin.site.register(Cosas) 
admin.site.register(User)
# Register your models here.
