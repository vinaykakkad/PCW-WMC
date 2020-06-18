from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Events, Images
# Create your views here.
class EventsPageView(TemplateView):

    def get(self, request, *args, **kwargs):
        events = Events.objects.all()
        images = Images.objects.all()
        context = {'events': events, 'images': images}
        return render(request, 'events.html', context)

