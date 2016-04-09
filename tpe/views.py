from django.shortcuts import render, redirect
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

def edit_experience(request, slug):
    # grab the object
    experience = Experience.objects.get(slug=slug)

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
        form = form_class(instance=experience)
    return render(request, 'experiences/edit_experience.html', { 'experience': experience, 'form': form })
