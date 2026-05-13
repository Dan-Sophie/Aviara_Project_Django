from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_pedidos, name='lista_pedidos'),
    path('nuevo/', views.gestionar_pedido, name='crear_pedido'),
    path('editar/<int:pk>/', views.gestionar_pedido, name='editar_pedido'),
    path('detalle/<int:pk>/', views.detalle_pedido, name='detalle_pedido'),
    path('estado/<int:pk>/<str:nuevo_estado>/', views.cambiar_estado_pedido, name='cambiar_estado_pedido'),
]