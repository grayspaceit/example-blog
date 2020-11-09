from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

# Create your models here.


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    REQUIRED_FIELDS = []
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("profile", kwargs={ "pk": self.pk })
