from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home),
    path('graph/', views.Graph)
]
