from django.shortcuts import render

from .models import Committee
# Create your views here.


def about_page_view(request, *args, **kwargs):
    committee = Committee.objects.all()
    context = {'committee': committee}
    return render(request, 'about/about.html', context)