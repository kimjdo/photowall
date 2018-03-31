import re
from django.db import models
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
