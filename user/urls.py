from django.urls import path
from .views import (
    RegisterView, 
    LoginView, 
    UserView, 
    LogoutView, 
    UserList,
    UserDetail
)

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),
    path('<int:pk>', UserDetail.as_view()),
    path('', UserList.as_view()),
]