from django.urls import path
from . import views
urlpatterns = [
    path('', views.update_all, name='update_all'),
    
]
