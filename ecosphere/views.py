from django.shortcuts import render

def index(request):
    return render(request, 'ecosphere/index.html')


# Create your views here.
