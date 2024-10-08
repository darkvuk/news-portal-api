from rest_framework import serializers
from .models import Comment, Article

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'author', 'email', 'created_at', 'content', 
                  'visibility', 'likes', 'article_id']
        read_only_fields = ['id', 'created_at']


class ArticleListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ['id', 'headline', 'picture1']
        read_only_fields = ['id', 'headline', 'picture1']


class ArticleSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['id', 'author_id', 'category', 'created_at', 'updated_at',
                  'headline', 'text1', 'picture1', 'pic_description1',
                  'text2', 'picture2', 'pic_description2',
                  'text3', 'picture3', 'pic_description3',
                  'text4', 'visibility', 'position', 'comments']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_comments(self, obj):
        comments = Comment.objects.filter(article_id=obj.id)
        return CommentSerializer(comments, many=True).data