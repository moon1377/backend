from django.shortcuts import render
from .models import Person, User


def appname_home(request):
    person_list = Person.objects.all()
    user_list = User.objects.all()
    return render(request, 'appname/appname.html', {'persons' : person_list, 'users' : user_list})

def personalizado(request, slug):
    person = Person.objects.get(slug=slug)
    return render(request, 'appname/person.html', {'person' : person})


