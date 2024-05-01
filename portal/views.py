from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category
from .serializers import (
    CategorySerializer
)
from user.mixins import UserPermissionMixin


class CategoryList(UserPermissionMixin, APIView):

    def get(self, request):
        categories = Category.objects.all()
        if not categories:
            return Response(
                {"detail": "No categories found."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if self.is_superuser(request):
            serializer = CategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)