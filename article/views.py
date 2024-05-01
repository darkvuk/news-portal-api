from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Comment, Article
from .serializers import (
    CommentSerializer, 
    ArticleSerializer, 
    ArticleListSerializer
)
from user.mixins import UserPermissionMixin


class ArticleList(UserPermissionMixin, APIView):

    def post(self, request):
        if self.is_logged_in(request):
            serializer = ArticleSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        articles = Article.objects.all()
        if not articles:
            return Response(
                {"detail": "No articles found."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ArticleDetail(APIView):

    def get_object(self, pk):
        try:
            return Article.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, pk):
        article = self.get_object(pk=pk)
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentList(APIView):

    def post(self, request, pk):
        data = request.data.copy() 
        data['article_id'] = pk 
        serializer = CommentSerializer(data=data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        comments = article.comments.all()
        if not comments:
            return Response(
                {"detail": "No comments found."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CommentDetail(APIView):

    def get_object(self, article_id, comment_id):
        article = get_object_or_404(Article, pk=article_id)
        comment = article.comments.get(id=comment_id)
        if not comment:
            return Response(
                {"detail": "No comments found."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        return comment
        
    def patch(self, request, article_id, comment_id):
        comment = self.get_object(article_id=article_id, comment_id=comment_id)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, article_id, comment_id):
        comment = self.get_object(article_id=article_id, comment_id=comment_id)
        comment.delete()
        return Response(
            {'detail': 'Comment has been successfully deleted.'}, 
            status=status.HTTP_204_NO_CONTENT
        )