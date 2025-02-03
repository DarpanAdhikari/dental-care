from django.db import models
from django.contrib.auth.models import User
import os

class AvailableDay(models.Model):
    day = models.CharField(max_length=10, choices=[
        ('sun', 'Sunday'),
        ('mon', 'Monday'),
        ('tue', 'Tuesday'),
        ('wed', 'Wednesday'),
        ('thu', 'Thursday'),
        ('fri', 'Friday'),
        ('sat', 'Saturday')
    ])
    def __str__(self):
        return self.get_day_display()
    
class Doctor(models.Model):
    QUALIFICATION_CHOICES = [
        ('bds', 'BDS'),
        ('mds', 'MDS'),
        ('dds', 'DDS'),
        ('dmd', 'DMD')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    qualification = models.CharField(max_length=100, choices=QUALIFICATION_CHOICES)
    specialization = models.CharField(max_length=100)
    contact = models.BigIntegerField()
    profile_img = models.ImageField(upload_to='profile_img/',blank=True, null=True)
    available_days = models.ManyToManyField(AvailableDay, blank=True) 
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.pk: 
            try:
                old_image = Doctor.objects.get(pk=self.pk).profile_img
                if old_image and self.profile_img != old_image: 
                    if os.path.isfile(old_image.path):
                        os.remove(old_image.path) 
            except Doctor.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    def __str__(self):
        days = ', '.join([day.get_day_display() for day in self.available_days.all()])
        return f'{self.user.get_full_name()} ({days})'
    
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.BigIntegerField()
    address = models.CharField(max_length=150)
    medical_history = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} {self.user.get_full_name()}"