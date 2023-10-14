from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from datetime import date


class Profile(models.Model):

    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.TextField(blank=True)
    age = models.PositiveIntegerField()
    biography = models.TextField(blank=True)
    owned_cars = models.IntegerField()
    issues_posted = models.IntegerField()
    issues_solved = models.IntegerField()
    """ favorite_brand = models.ManyToManyField() """
    image = models.ImageField(upload_to='images/', default='../default_profile_ponhew')

    class Meta:
        ordering = ['-issues_solved']

    def __str__(self):
        return f"{self.owner}'s profile"

def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(owner=instance)


post_save.connect(create_profile, sender=User)