from django.forms import ModelForm
from django import forms
from tpe.models import Experience
from tpe.models import Upload


class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = ('name', 'description')

class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    content = forms.CharField(required=True, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['contact_name'].label = "Your name:"
        self.fields['contact_email'].label = "Your email:"
        self.fields['content'].label = "What do you want to say?"

class ExperienceUploadForm(ModelForm):
    class Meta:
        model = Upload
        fields = ('image',)