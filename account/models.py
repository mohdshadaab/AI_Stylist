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
    
    image=models.ImageField(upload_to=upload_to, blank=True, null=True)
    category_list=models.TextField(null=True)
    color=models.TextField(null=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.image}'






