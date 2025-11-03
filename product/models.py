from django.db import models
from django.contrib.auth.models import User

CASAS = [
    ('CAS', 'Casa'),
    ('DEP', 'Departamento'),
    ('TER', 'Terreno'),
]

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()
    category = models.CharField(max_length=3, choices=CASAS)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}, by {self.user}"