from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.template import Context
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from django.template.defaultfilters import slugify
from tpe.forms import (ExperienceForm, ContactForm)
from tpe.models import Experience
from tpe.forms import ExperienceUploadForm
from tpe.models import Upload

# Create your views here.
def index(request):
    experiences = Experience.objects.all().order_by('name')
    return render(request, 'index.html', { 'experiences': experiences })

def experience_detail(request, slug):
    # grab the object
    experience = Experience.objects.get(slug=slug)
    social_accounts = experience.social_accounts.all()
    uploads = experience.uploads.all()
    return render(request, 'experiences/experience_detail.html', { 'experience': experience, 'social_accounts': social_accounts, 'uploads': uploads, })

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
            messages.success(request, 'Experience details updated.')
            return redirect('experience_detail', slug=experience.slug)
    else:
        form = form_class(instance=experience)
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

def contact(request):
    form_class = ContactForm

    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_name = form.cleaned_data['contact_name']
            contact_email = form.cleaned_data['contact_email']
            form_content = form.cleaned_data['content']

            template = get_template('contact_template.txt')
            context = Context({
                'contact_name': contact_name,
                'contact_email': contact_email,
                'form_content': form_content})
            content = template.render(context)
            email = EmailMessage('New contact form submission', content, 'Your website <hi@weddinglovely.com>', ['youremail@gmaiul.com'], headers = {'Reply-To': contact_email })
            email.send()
            return redirect('contact')
    return render(request, 'contact.html', { 'form': form_class})

@login_required
def edit_experience_uploads(request, slug):
    experience = Experience.objects.get(slug=slug)

    if experience.user != request.user:
        raise Http404

    form_class = ExperienceUploadForm
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES,instance=experience)
        if form.is_valid():
            Upload.objects.create(image=form.cleaned_data['image'], experience=experience,)
            return redirect('edit_experience_uploads', slug=experience.slug )
    else:
        form = form_class(instance=experience)
        uploads = experience.uploads.all()
    return render(request, 'experiences/edit_experience_uploads.html', {'experience': experience, 'form':form, 'uploads':uploads, })

@login_required
def delete_upload(request, id):
    upload = Upload.objects.get(id=id)
    if upload.experience.user != request.user:
        raise Http404

    upload.delete()
    return redirect('edit_experience_uploads',slug=upload.experience.slug)