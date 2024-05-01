from rest_framework import serializers
from .models import Category
from article.serializers import ArticleListSerializer

class CategorySerializer(serializers.ModelSerializer):
    articles = ArticleListSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'title', 'articles']
        read_only_fields = ['id']