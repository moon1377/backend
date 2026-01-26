from django.contrib import admin

# Register your models here.

from .models import ErrorReport

admin.site.register(ErrorReport)
