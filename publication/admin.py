from django.contrib import admin

from publication.models import Article, Section

# Register your models here.
admin.site.register(Section)
admin.site.register(Article)