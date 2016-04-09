from django.forms import ModelForm
from tpe.models import Experience

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = ('name', 'description')