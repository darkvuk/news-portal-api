from django.db import models
from django.conf import settings
from django.utils import timezone


class Article(models.Model):
    POSITION_CHOICES = [
        (0, 'Position 0'),
        (1, 'Position 1'),
        (2, 'Position 2'),
        (3, 'Position 3'),
    ]

    author_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    headline = models.CharField(max_length=255)
    text1 = models.TextField()
    picture1 = models.ImageField(upload_to='article_pictures/', null=True, blank=True)
    pic_description1 = models.CharField(max_length=255, null=True, blank=True)
    text2 = models.TextField(null=True, blank=True)
    picture2 = models.ImageField(upload_to='article_pictures/', null=True, blank=True)
    pic_description2 = models.CharField(max_length=255, null=True, blank=True)
    text3 = models.TextField(null=True, blank=True)
    picture3 = models.ImageField(upload_to='article_pictures/', null=True, blank=True)
    pic_description3 = models.CharField(max_length=255, null=True, blank=True)
    text4 = models.TextField(null=True, blank=True)
    visibility = models.BooleanField(default=False)
    position = models.IntegerField(choices=POSITION_CHOICES, default=0)

    def __str__(self):
        return self.headline[:100]


class Comment(models.Model):
    article_id = models.ForeignKey(
        Article, 
        on_delete=models.CASCADE, 
        related_name='comments'
        )
    author = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    visibility = models.BooleanField(default=False)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.article_id.headline} ({self.id})'