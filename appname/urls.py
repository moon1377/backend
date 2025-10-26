from django.urls import path
from . import views


app_name = 'prueba'

urlpatterns = [
    path('', views.appname_home, name="home"),
    path('<slug:slug>/', views.personalizado, name='person'),
]