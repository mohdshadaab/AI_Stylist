from matplotlib import image
from rest_framework import serializers
from .models import Image, User

class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    images=ImageSerializer(many=True)

    class Meta:
        model=User
        field=['user_id', 'first_name', 'last_name', 'email', 'images']
