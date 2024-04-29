from django.shortcuts import render
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


class ArticleList(APIView):

    def post(self, request):
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



class CommentList(APIView):

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        comments = Comment.objects.all()
        if not comments:
            return Response(
                {"detail": "No comments found."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CommentDetail(APIView):

    def get_object(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise Http404
        
    def patch(self, request, pk):
        comment = self.get_object(pk=pk)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        comment = self.get_object(pk)
        comment.delete()
        return Response(
            {'detail': 'Comment has been successfully deleted.'}, 
            status=status.HTTP_204_NO_CONTENT
        )