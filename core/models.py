from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.db.models.signals import post_save


class Profile(models.Model):

    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.TextField(blank=True, null=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    biography = models.TextField(blank=True, null=True)
    owned_cars = models.IntegerField(null=True, blank=True)
    issues_posted = models.IntegerField(null=True, blank=True)
    issues_solved = models.IntegerField(null=True, blank=True)
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

""" This sections holds the models for the Issues posted by the user:  """
class Issue(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    car = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    year = models.IntegerField(null=True, blank=True)
    engine_size = models.DecimalField(max_digits=3, decimal_places=1)
    description = models.TextField(blank=True)
    is_solved = models.BooleanField(default=True)
    image = models.ImageField(
        upload_to='images/', default='../default_post_rgq6aq', blank=True, null=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.title}'


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    comment_area = models.TextField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.comment_area


""" Here follows the Like and Dislike Models: """

class Like(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(
        Comment, related_name='likes', on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'comment']

    def __str__(self):
        return f'{self.owner} {self.post}'


class DisLike(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(
        Comment, related_name='dislikes', on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'comment']

    def __str__(self):
        return f'{self.owner} {self.post}'