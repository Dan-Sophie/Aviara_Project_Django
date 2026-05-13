from django.urls import path
from . import views

urlpatterns = [
    path('produccion/', views.lista_produccion, name='lista_produccion'),
    path('produccion/registrar/', views.registrar_produccion, name='registrar_produccion'),
    path('produccion/editar<int:pk>/', views.editar_produccion, name='editar_produccion'),
    path('lotes/', views.lista_lotes, name='lista_lotes'),
    path('lotes/nuevo', views.crear_lote, name='crear_lote'),
    path('lotes/editar<int:pk>/', views.editar_lote, name='editar_lote'),
]