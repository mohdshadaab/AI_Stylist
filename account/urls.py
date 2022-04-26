# accounts/urls.py
from curses.ascii import CR
from django.urls import path
from .views import CreateNewUserView, UploadImageView, GetImageView, GetUserView, DelUserView, DelImageView

urlpatterns = [
    path('create_user', CreateNewUserView.as_view()),
    path('upload_image', UploadImageView.as_view()),
    path('get_image', GetImageView.as_view()),
    path('get_user', GetUserView.as_view()),
    path('delete_user', DelUserView.as_view()),
    path('delete_image', DelImageView.as_view())
] 