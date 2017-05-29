from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.
# MVC MODEL VIEW CONTROLLER


# This fucntions changes uploaded image location by creating first folder by post_id.  
def upload_image_location(instance, filename):
	# filebase, extension = filename.split(".")
	# return "%s/%s/%s" %(instance.id, instance.id, extension)
	return "%s/%s" %(instance.id, filename)

class Post(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    image = models.ImageField(
    	upload_to=upload_image_location,
        null=True, blank=True, 
        width_field="width_field", 
        height_field="height_field")
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"id": self.id})

    class Meta:
        # In views adding order_by.('-timestamp') also performs the same but
        # its good to add ordering in Meta class.
        ordering = ['-timestamp', '-updated']
