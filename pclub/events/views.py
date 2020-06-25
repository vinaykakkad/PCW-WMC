from datetime import datetime

from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from django.utils import timezone

from .models import Events, Images
# Create your views here.


class EventsPageView(TemplateView):

    def get(self, request, *args, **kwargs):
        events = Events.objects.order_by('-start_date')
        current_time = timezone.now()
        filtered = False
        a = b = c = 0 

        x = request.GET.get('clear')
        # Clearing all the filters
        try:
            a = 2
            if request.GET.get('clear') == '1':
                request.session['when'] = None
                request.session['month'] = None
                request.session['title'] = None
        except Exception as identifier:
            pass

        # If filters are received/valid, store them in session
        try:
            if request.GET.get('when') is not None:
                request.session['when'] = request.GET.get('when')
        except Exception as identifier:
            pass
        try:
            if request.GET.get('month') is not None and request.GET.get('month') != "":
                request.session['month'] = request.GET.get('month')
        except Exception as identifier:
            pass
        try:
            if request.GET.get('title') is not None and request.GET.get('title') != "":
                request.session['title'] = request.GET.get('title')
                b = 1
        except Exception as identifier:
            pass

        # If session variables aren't initialized, initialize as None
        try:
            if request.session['when'] is not None:
                pass
        except Exception as identifier:
            request.session['when'] = None
        try:
            if request.session['month'] is not None:
                pass
        except Exception as identifier:
            request.session['when'] = None
        try:
            if request.session['title'] is not None:
                pass
        except Exception as identifier:
            request.session['title'] = None
            c = 1

        # Filtering data as per requirement
        if request.session['when'] is not None:
            if request.session['when'] == "past":
                filtered = True
                events = events.filter(end_date__lt=current_time)
            if request.session['when'] == "current":
                filtered = True
                events = events.filter(
                    end_date__gt=current_time, start_date__lt=current_time)
            if request.session['when'] == "future":
                filtered = True
                events = events.filter(start_date__gt=current_time)

        if request.session['month'] is not None:
            filtered = True
            filter_whole = request.session['month']
            filter_month = int(filter_whole[5:])
            filter_year = int(filter_whole[:4])
            events = events.filter(
                start_date__month__exact=filter_month, start_date__year__exact=filter_year)

        if request.session['title'] is not None:
            filtered = True
            d = a
            filter_title = request.session['title']
            events = events.filter(title__icontains=filter_title)

        paginator = Paginator(events, 3)
        page = request.GET.get('page')
        events = paginator.get_page(page)

        context = {'page_object': events,
                   'filtered': filtered, 'page_name': events}
        return render(request, 'events/events.html', context)
