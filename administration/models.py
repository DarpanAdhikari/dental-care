import os
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.
import os
from django.utils.text import slugify
from django.db import models

class DentalPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    slug = models.SlugField(blank=True, null=True)
    keywords = models.TextField()
    meta_description = models.TextField()
    content = models.TextField()
    feature_img = models.ImageField(upload_to='posts_img/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.pk: 
            try:
                old_image = DentalPost.objects.get(pk=self.pk).feature_img
                if old_image and self.feature_img != old_image: 
                    if os.path.isfile(old_image.path):
                        os.remove(old_image.path) 
            except DentalPost.DoesNotExist:
                pass
        super().save(*args, **kwargs)
