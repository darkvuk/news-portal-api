from django.urls import path
from .views import (
    CommentList, 
    CommentDetail, 
    ArticleList, 
    ArticleDetail
)

urlpatterns = [
    path('article', ArticleList.as_view()),
    path('article/<int:pk>', ArticleDetail.as_view()),
    path('comment', CommentList.as_view()),
    path('comment/<int:pk>', CommentDetail.as_view())
]