from django.contrib import admin
# import your model
from tpe.models import Experience

# set up automated slug creation
class ExperienceAdmin(admin.ModelAdmin):
    model = Experience
    list_display = ('name', 'description', 'user')
    prepopulated_fields = {'slug': ('name',)}

# Register your models here.
admin.site.register(Experience, ExperienceAdmin)
