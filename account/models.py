# accounts/models.py
from distutils.command.upload import upload
from django.db import models


class User(models.Model):
    user_id=models.CharField(max_length=28, primary_key=True)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email=models.EmailField(max_length=254, unique=True)
    # add additional fields in here

    def __str__(self):
        return f'{self.first_name}-{self.email}'


def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)

class Image(models.Model):
    user=models.ForeignKey(User, related_name='cloth_image', on_delete=models.CASCADE)
    image=models.ImageField(upload_to=upload_to, blank=True, null=True)
    category_list=models.TextField(null=True)
    color=models.TextField(max_length=30)

    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'



