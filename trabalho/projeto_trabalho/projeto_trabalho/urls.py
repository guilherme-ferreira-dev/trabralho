from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cadastro/', include('cadastro.urls')),
]

# arquivo: cadastro/urls.py
from django.urls import path
from . import views

app_name = 'cadastro'

urlpatterns = [
    path('', views.home, name='home'),
    path('listar/', views.listar_urls, name='listar_urls'),
    path('incluir/', views.incluir_url, name='incluir_url'),
    path('alterar/<int:url_id>/', views.alterar_url, name='alterar_url'),
    path('excluir/<int:url_id>/', views.excluir_url, name='excluir_url'),
    path('validar/<int:url_id>/', views.validar_url, name='validar_url'),
    path('validar-todos/', views.validar_todos, name='validar_todos'),
]


from django.db import models

class EnderecoWeb(models.Model):
    url = models.URLField(unique=True)
    validado = models.BooleanField(default=False)

    def _str_(self):
        return self.url


from django import forms
from .models import EnderecoWeb

class EnderecoWebForm(forms.ModelForm):
    class Meta:
        model = EnderecoWeb
        fields = ['url']


from django.shortcuts import render, redirect, get_object_or_404
from .models import EnderecoWeb
from .forms import EnderecoWebForm

def home(request):
    return render(request, 'cadastro/home.html')

def listar_urls(request):
    urls = EnderecoWeb.objects.all()
    return render(request, 'cadastro/listar_urls.html', {'urls': urls})

def incluir_url(request):
    if request.method == 'POST':
        form = EnderecoWebForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cadastro:listar_urls')
    else:
        form = EnderecoWebForm()
    return render(request, 'cadastro/incluir_url.html', {'form': form})

def alterar_url(request, url_id):
    url = get_object_or_404(EnderecoWeb, pk=url_id)
    if request.method == 'POST':
        form = EnderecoWebForm(request.POST, instance=url)
        if form.is_valid():
            form.save()
            return redirect('cadastro:listar_urls')
    else:
        form = EnderecoWebForm(instance=url)
    return render(request, 'cadastro/alterar_url.html', {'form': form})

def excluir_url(request, url_id):
    url = get_object_or_404(EnderecoWeb, pk=url_id)
    url.delete()
    return redirect('cadastro:listar_urls')

def validar_url(request, url_id):
    url = get_object_or_404(EnderecoWeb, pk=url_id)
    # Lógica de validação da URL
    url.validado = True
    url.save()
    return redirect('cadastro:listar_urls')

def validar_todos(request):
    urls = EnderecoWeb.objects.all()
    # Lógica de validação de todas as URLs
    for url in urls:
        url.validado = True
        url.save()
    return redirect('cadastro:listar_urls')