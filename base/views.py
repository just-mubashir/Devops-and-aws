from django.shortcuts import render



def home(request):
    context = "Mubashir-Django"
    return render(request , 'base/home.html' )