from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # get
    path('status/', views.get_server_status, name='server_status'),
    path('errors/', views.get_errors, name='all_errors'),
    path('error/<int:code>/', views.get_error_from_code, name='error_detail'),
    
    # post
    path('create/', views.create_error, name='create_error'),
    
    # actu y borrar de put y delete
    path('update/<int:code>/', views.object_update, name='update_error'),
]