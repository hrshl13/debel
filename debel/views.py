from django.shortcuts import render
# Create your views here.

def home(request):
    return render(request, 'debel/home.html')

def about(request):
    return render(request, 'debel/about.html', {'title': 'About'})

def layman(request):
    return render(request, 'debel/layman.html', {'title': "Layman's Corner"})

def virtuoso(request):
    return render(request, 'debel/virtuoso.html', {'title': "Virtuoso's Studio"})

def expert(request):
    return render(request, 'debel/expert.html', {'title': "Expert's Lab"})


