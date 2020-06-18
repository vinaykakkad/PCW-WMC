from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Resources, Tags

# Create your views here.
class ResourcesView(TemplateView):
    def get(self, request, *args, **kwargs):
        tags = Tags.objects.all()
        resources = Resources.objects.all() 
        context = {'resources': resources, 'tags':tags}
        return render(request, 'resources.html', context)

    def post(self, request, *args, **kwargs):
        tags = Tags.objects.all()
        all_resources = Resources.objects.all() 
        filter_tags= set(request.POST.getlist('tags'))
        resources = [] 
        for i in all_resources:
            if filter_tags.issubset(i.get_tags()):
                resources.append(i)
        context = {'resources': resources, 'tags':tags}
        return render(request, 'resources.html', context)
