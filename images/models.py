from django.db import models
from django.conf import settings
from django.utils.text import slugify

# Create your models here.

class Image(models.Model):
    # user can post multiple images,
    # but each image is posted by a single user.
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='images_ceated',
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,
                            blank=True)
    url = models.URLField()
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    description = models.TextField(blank=True)
    # use ""db_index=True"" so that Django creates an index in the
    # database for this field.
    created = models.DateField(auto_now_add=True,
                               db_index=True)
    # how to like a image model
    # user might like multiple image
    # and each image can be loked by multiple users
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='images_liked',
                                        blank=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Image, self).save(*args, **kwargs)
        
        