from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('appointment/',views.create_appointment, name='appointment')
]