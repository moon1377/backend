from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=50)
    birth = models.DateField()
    slug = models.SlugField()
    
    def __str__(self):
        return self.name
    
class Cosas(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(Person, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

class User(models.Model):
    name = models.CharField(max_length=50)
    mail = models.CharField(max_length=100)
    propic = models.ImageField(upload_to='users/', default='def_user.png', blank=True)
    
    def __str__(self):
        return self.name
    