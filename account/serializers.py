from rest_framework import serializers
from .models import Image, User

class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    images=ImageSerializer(many=True, read_only=True,source='image_set')

    class Meta:
        model=User
        fields=['user_id', 'first_name', 'last_name', 'email', 'images' ]
        #fields='__all__'
