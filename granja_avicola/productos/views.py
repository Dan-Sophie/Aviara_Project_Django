from django.shortcuts import render

def catalogo_view(request):
    return render(request, 'productos/catalogo.html')
# Create your views here.
