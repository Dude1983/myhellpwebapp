from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.template.defaultfilters import slugify
from tpe.forms import ExperienceForm
from tpe.models import Experience

# Create your views here.
def index(request):
    experiences = Experience.objects.all().order_by('name')
    return render(request, 'index.html', { 'experiences': experiences })

def experience_detail(request, slug):
    # grab the object
    experience = Experience.objects.get(slug=slug)
    return render(request, 'experiences/experience_detail.html', { 'experience': experience })

@login_required()
def edit_experience(request, slug):
    # grab the object
    experience = Experience.objects.get(slug=slug)
    if experience.user != request.user:
        raise Http404
    # set the form we're using
    form_class = ExperienceForm

    # if we're coming to this view from a submitted form
    if request.method == 'POST':
        # grab the data from the submitted form and apply to the form
        form = form_class(data=request.POST, instance=experience)
        if form.is_valid():
            # save the data
            form.save()
            return redirect('experience_detail', slug=experience.slug)
    else:
        form = form_class(instance=experiences)
    return render(request, 'experiences/edit_experience.html', { 'experience': experience, 'form': form })

def create_experience(request):
    form_class = ExperienceForm
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.user = request.user
            experience.slug = slugify(experience.name)
            experience.save()
            return redirect('experience_detail', slug=experience.slug)
    else:
        form = form_class()
    return render(request, 'experiences/create_experience.html', {'form': form,})

def browse_by_name(request, initial=None):
    if initial:
        experiences = Experience.objects.filter(name__istartswith=initial)
        experiences = experiences.order_by('name')
    else:
        experiences = Experience.objects.all().order_by('name')
    return render(request, 'search/search.html', { 'experiences': experiences, 'initial': initial, })