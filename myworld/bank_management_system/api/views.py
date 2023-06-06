from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import *

# Create your views here.

class ClientViewSet(viewsets.ModelViewSet) :
    queryset = Client.objects.all()
    serializer_class = ClientSerializer