from django.contrib import admin
# import your model
from tpe.models import Experience, Upload
from tpe.models import Social

# set up automated slug creation
class ExperienceAdmin(admin.ModelAdmin):
    model = Experience
    list_display = ('name', 'description', 'user')
    prepopulated_fields = {'slug': ('name',)}

# Register your models here.
admin.site.register(Experience, ExperienceAdmin)

class SocialAdmin(admin.ModelAdmin):
    model = Sociallist_display = ('network', 'username',)

admin.site.register(Social,SocialAdmin)

class UploadAdmin(admin.ModelAdmin):
    list_display = ('experience', )
    list_display_links = ('experience',)

admin.site.register(Upload, UploadAdmin)