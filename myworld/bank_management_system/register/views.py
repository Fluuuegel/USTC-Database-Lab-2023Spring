from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
import random

from django.db import IntegrityError, transaction
from django.db.models import ProtectedError
from django.utils import timezone

from .serializers import *
from .forms import *
# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'

    @action(detail=False, methods=['post'])
    @transaction.atomic
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    user = serializer.save()
                    user.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            except:
                return Response({'error': 'Username already exists.'}, status=status.HTTP_409_CONFLICT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        id = request.data.get('id')
        passwd = request.data.get('passwd')

        try:
            user = User.objects.get(id=id, passwd=passwd)
        except user.DoesNotExist:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def uploadImage(self, request):
        id = request.data.get('id')
        image = request.FILES.get('image')
        user = User.objects.get(id=id)
        user.photo = image
        user.save()
        return Response({'message': 'Image uploaded successfully'}, status=status.HTTP_200_OK)
        