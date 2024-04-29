from django.contrib import admin
from article import models

admin.site.register(models.Article)
admin.site.register(models.Comment)
