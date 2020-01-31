from django.shortcuts import render

# Create your views here.

def create(request):
    return render(request, 'usuarios/create.html')

def confirm(request):
    return render(request, 'usuarios/confirm.html')
