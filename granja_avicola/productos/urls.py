from django.urls import path
from .views import catalogo_view

urlpatterns = [
    path('catalogo/', catalogo_view, name='catalogo'),
]