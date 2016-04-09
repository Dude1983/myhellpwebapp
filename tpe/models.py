from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import force_bytes
from PIL import Image

# Create your models here.
class Experience(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(unique=True)
    user = models.OneToOneField(User, blank=True, null=True)

    def __str__(self):
        return self.name

class Social(models.Model):
    SOCIAL_TYPES = (
        ('twitter', 'Twitter'),
        ('facebook', 'Facebook'),
        ('pinterest', 'Pinterest'),
        ('instagram', 'Instagram'),
    )
    network = models.CharField(max_length=255, choices=SOCIAL_TYPES)
    username = models.CharField(max_length=255)
    experience = models.ForeignKey(Experience, related_name="social_accounts")

    # Shows the
    def __str__(self):
        return force_bytes('Social Media: %s Experience: %s' % (self.network, self.experience))

    class Meta:
        verbose_name_plural = "Social media links"

def get_image_path(instance, filename):
    return '/'.join(['experience_images',instance.experience.slug, filename])

class Upload(models.Model):
    experience = models.ForeignKey(Experience, related_name="uploads")
    image = models.ImageField(upload_to=get_image_path)

    def save(self, *args, **kwargs):
        super(Upload,self).save(*args, **kwargs)
        if self.image:
            image=Image.open(self.image)
            i_width, i_height = image.size
            max_size = (250,250)
            if i_width > 250:
                image.thumbnail(max_size, Image.ANTIALIAS)
                image.save(self.image.path)

