import re
from django.db import models
from django.urls import reverse
from django.conf import settings
from django import forms

# Create your models here.
def lnglat_validator(value):
    if not re.match(r'^[+-]?\d+\.?\d*,[+-]?\d+\.?\d*$', value):
        raise forms.ValidationError('위도/경도를 입력해 주세요.')

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    photo = models.ImageField()
    lnglat = models.CharField(max_length=40, blank=True, validators=[lnglat_validator])
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.pk])

    @property
    def lng(self):
        if self.lnglat:
            return self.lnglat.split(',')[0]
        return None
    @property
    def lat(self):
        if self.lnglat:
            return self.lnglat.split(',')[1]
        return None

class Comment(models.Model):
    # Post : Comment = 1 : N
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class meta:
        ordering = ['-id']

    def get_edit_url(self):
        return reverse('comment_edit', args=[self.post.pk, self.pk])

    def get_delete_url(self):
        return reverse('comment_delete', args=[self.post.pk, self.pk])
