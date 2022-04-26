# accounts/views.py
from ast import Del
import os
from django.conf import settings
from account.serializers import ImageSerializer
from rest_framework.decorators import api_view
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .models import User, Image
from .serializers import UserSerializer, ImageSerializer

class CreateNewUserView(views.APIView):
    """
Sample payload:
        {
            "user_id": "kVNr3WPrvNg8rNJu0YzRfIimpXY2",
            "email": "mohdshadaab27@gmail.com",
            "first_name": "Mohammad",
            "last_name": "Shadaab"
        }

Returned status codes: 
        - 405 Method Not allowed
        - 404 user not found
        - 400 Bad request
        - 500 Internal error
    """
    def post(self, request, format=None):
        user_id = request.data.get('user_id', None)
        if (user_id):
            if(User.objects.filter(user_id=user_id)):
                return Response(data={"message": "User already exists!!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        email = request.data.get('email', None)
        first_name = request.data.get('first_name', None)
        last_name = request.data.get('last_name', None)
        user , created = User.objects.get_or_create(
            user_id=user_id,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        if(created):
            return Response(data={"message":"user created successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(data={"message":"user was not created"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UploadImageView(views.APIView):
    #serializer_class = ImageSerializer()
    #queryset = Image.objects.all()
    """
    Sample payload:
        {
            "user_id": "kVNr3WPrvNg8rNJu0YzRfIimpXY2",
            "image": file,
            "category_list": ['top','trouser],
            "color": ['blue','red']
        }

    Returned status codes: 
        - 405 Method Not allowed
        - 404 user not found
        - 400 Bad request
        - 500 Internal error
    """
    parser_classes = (MultiPartParser, FormParser)


    def post(self, request, *args, **kwargs):
        user_id=request.data.get('user_id',None)
        if user_id:
            try:
                print(request.data.get('color'))
                user = User.objects.get(user_id=user_id)
                image=Image.objects.create(user=user, image=request.data.get('image'),category_list=request.data.get('category_list'), color=request.data.get('color'))
                return Response(data={"message":"image uploaded successfully"}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response(data={'message': 'No user exists with this user id'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(data={'message': 'Bad Request user id not found'}, status=status.HTTP_404_NOT_FOUND)
        """
        image_serializer = ImageSerializer(data=request.data)
        if image_serializer.is_valid():
            image_serializer.save()
            return Response (image_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response (image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        """


class GetImageView(views.APIView):
    """
    Sample payload:
        {
            "user_id": "kVNr3WPrvNg8rNJu0YzRfIimpXY2"
        }

    Returned status codes: 
        - 405 Method Not allowed
        - 404 user not found
        - 400 Bad request
        - 500 Internal error
    """
    def post(self,request):
        user_id=request.data.get('user_id',None)
        if user_id:
            try:
                user = User.objects.get(user_id=user_id)
            except User.DoesNotExist:
                return Response(data={'message': 'No user exists with this user id'}, status=status.HTTP_404_NOT_FOUND)
        
        images=Image.objects.filter(user=User.objects.get(user_id=user_id))
        image_ser=ImageSerializer(images, many=True, read_only=True)
        return Response(image_ser.data, status=status.HTTP_200_OK)

class GetUserView(views.APIView):
    """
    Sample payload:
        {
            "user_id": "kVNr3WPrvNg8rNJu0YzRfIimpXY2"
        }

    Returned status codes: 
        - 405 Method Not allowed
        - 404 user not found
        - 400 Bad request
        - 500 Internal error
    """
    
    def post(self, request):
        user_id = request.data.get('user_id', None)
        if user_id:
            try:
                user = User.objects.get(user_id=user_id)
            except User.DoesNotExist:
                return Response(data={'message': 'No user exists with this user id'}, status=status.HTTP_404_NOT_FOUND)

            ser = UserSerializer(user)
            return Response(ser.data, status=status.HTTP_200_OK)

        else:
            return Response(data={'message': 'Bad input, user_id not valid'}, status=status.HTTP_400_BAD_REQUEST)


class DelImageView(views.APIView):
    """
    Sample payload:
        {
            "user_id": "kVNr3WPrvNg8rNJu0YzRfIimpXY2",
            "image" : "/media/images/XXXX.jpeg"
        }

    Returned status codes: 
        - 405 Method Not allowed
        - 404 user not found
        - 400 Bad request
        - 500 Internal error
    """
    
    def post(self, request):
        user_id = request.data.get('user_id', None)
        if user_id:
            try:
                user = User.objects.get(user_id=user_id)
                im_obj=Image.objects.get(id=request.data.get('image_id'))
                #file_name=request.data.get("image").split('/')[3]
                #print(request.data.get("image"))
                #im_obj=Image.objects.filter(image=request.data.get("image"))
                #print(im_obj.values())
                im_data=ImageSerializer(im_obj).data
                print(im_data)
                file_name=im_data["image"].split('/')[3]
                Image.objects.get(id=im_data['id']).delete()
                os.remove(os.path.join(settings.MEDIA_ROOT, "images/"+file_name))

                return Response(data={'message': 'image deleted successfully.'}, status=status.HTTP_200_OK)
            except User.DoesNotExist or Image.DoesNotExist:
                return Response(data={'message': 'No user/image exists with this user id'}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response(data={'message': 'Bad input, user_id not valid'}, status=status.HTTP_400_BAD_REQUEST)


class DelUserView(views.APIView):
    """
    Sample payload:
        {
            "user_id": "kVNr3WPrvNg8rNJu0YzRfIimpXY2"
        }

    Returned status codes: 
        - 405 Method Not allowed
        - 404 user not found
        - 400 Bad request
        - 500 Internal error
    """
    
    def post(self, request):
        user_id = request.data.get('user_id', None)
        if user_id:
            try:
                user = User.objects.get(user_id=user_id)
                user_data=UserSerializer(user).data
                print(user_data)
                for i in user_data["images"]:
                    file_name=i['image'].split('/')[3]
                    print(file_name)
                    os.remove(os.path.join(settings.MEDIA_ROOT, "images/"+file_name))                
                user.delete()
                return Response(data={'message': 'user deleted successfully.'}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response(data={'message': 'No user exists with this user id'}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response(data={'message': 'Bad input, user_id not valid'}, status=status.HTTP_400_BAD_REQUEST)



