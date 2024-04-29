from django.urls import path
from .views import (
    CommentList, 
    CommentDetail, 
    ArticleList, 
    ArticleDetail
)

urlpatterns = [
    path('', ArticleList.as_view()),
    path('<int:pk>', ArticleDetail.as_view()),
    path('<int:pk>/comment', CommentList.as_view()),
    path('<int:article_id>/comment/<int:comment_id>', 
         CommentDetail.as_view())
]