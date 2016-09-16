from django.shortcuts import render

def index(request):
	return HttpResponse("Hello, world. Estas en el index del inspector")
# Create your views here.
