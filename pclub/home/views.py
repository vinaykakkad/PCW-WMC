from django.shortcuts import render
from .models import Thoughts, Announcements
# Create your views here.

def home_page_view(request, *args, **kwargs):
    thoughts = Thoughts.objects.all()
    announcements = Announcements.objects.all()
    context = {'thoughts': thoughts, 'announcements':announcements}
    return render(request, 'home/home.html', context)