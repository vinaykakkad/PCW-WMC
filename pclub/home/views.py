from django.shortcuts import render

from .models import Announcements
# Create your views here.


def home_page_view(request, *args, **kwargs):
    announcements = Announcements.objects.all()
    context = {'announcements': announcements}
    return render(request, 'home/home.html', context)
