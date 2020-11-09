from django.db import models
from django.utils import timezone
from django.urls import reverse

from authentication.models import *

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse("post_detail",kwargs={'pk':self.pk})

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post , related_name='comments',on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse("post_detail",kwargs={'pk':self.post.pk})

    def __str__(self):
        return self.text
