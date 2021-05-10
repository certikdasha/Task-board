from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        CustomToken.objects.create(user=instance)


class CustomUser(AbstractUser):

    year = models.PositiveSmallIntegerField(null=True, blank=True)


class Cards(models.Model):

    STATUS_CHOICE = [
        (1, 'New'),
        (2, 'In Progress'),
        (3, 'In QA'),
        (4, 'Ready'),
        (5, 'Done'),
    ]

    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='creator')
    executor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='executor')
    status = models.IntegerField(choices=STATUS_CHOICE, default=1)
    text = models.TextField()
    change_time = models.DateTimeField(blank=True, null=True)


class CustomToken(Token):
    last_action = models.DateTimeField(null=True)
