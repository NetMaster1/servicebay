from django.urls import path
from . import views
urlpatterns = [
    path('', views.workshop_reports, name='workshop_reports'),
  
]

