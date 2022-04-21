# accounts/urls.py
from curses.ascii import CR
from django.urls import path
from .views import CreateNewUserView, UploadImageView, GetImageView

urlpatterns = [
    path('create_user', CreateNewUserView.as_view()),
    path('upload_image', UploadImageView.as_view()),
    path('get_image', GetImageView.as_view())
] 