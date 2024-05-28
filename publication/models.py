from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
import datetime
import re
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

from users.models import Staff
# Create your models here.


class Section(models.Model):
    Name = models.CharField("Name", max_length=156)
    description = models.TextField(default="null", blank=False)

    def __str__(self):
        return self.Name

    class Meta:
        managed = True
        verbose_name = 'Section'
        verbose_name_plural = 'Sections'



class Article(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE,related_name="section_article")
    title = models.CharField(max_length=255)
    title_slug = models.SlugField(default="null")
    description = models.TextField()
    keywords = models.CharField(max_length=255, default="null")
    image = models.ImageField(null=True,blank=True)
    image_source = models.CharField(max_length=255, null=True, blank=True)
    image_description = models.CharField(
        max_length=255, default='image', blank=True)
    body_text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    mod_date = models.DateTimeField(auto_now=True)
    publisher = models.ManyToManyField(Staff)
    view_count = models.IntegerField(default=0)
    publish = models.BooleanField(default=False)
    still_open = models.BooleanField(default=True)

    def bodySnippet(self):
        body = self.body_text[:120]
        bodySnippet = re.sub(
            r"\s\w+$|(<strong>|</strong>|<em>|</em>|<b>|</b>|<i>|</i>|<u>|</u>|<a.+?>|</a>)", "", body)
        return f'{bodySnippet} ....'

    def __str__(self):
        return self.title

    class Meta:
        managed = True
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ['-pub_date']

    # def delete(self, *args, **kwargs):
    #     self.image.delete()
    #     super().delete(*args, **kwargs)

    def save(self, skip_md=True, *args, **kwargs):
        if skip_md:
            self.mod_date = datetime.datetime.now()
            
   

        if self.image:
            target_height = 333
            im = Image.open(self.image)
            width,height=im.size
            output = BytesIO()
            newHeight= target_height
            newWidth= int(newHeight/height*width)
            im = im.resize((newWidth,newHeight))
            im.save(output, format='JPEG', quality=100)
            output.seek(0)
            self.image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.image.name.split(
                    '.')[0], 'image/jpeg', sys.getsizeof(output), None)

        super().save(*args, **kwargs)  # Call the real save() method


@receiver(pre_save, sender=Article)
def delete_Artictle_image(sender, instance, *args, **kwargs):
    if instance.pk:
        article = Article.objects.get(pk=instance.pk)
        if article.image != instance.image:
            article.image.delete(False)


@receiver(post_delete, sender=Article)
def delete_artictle_image(sender, instance, using, *args, **kwargs):
    if instance.image:
        instance.image.delete(save=False)
