from rest_framework import status
from rest_framework import viewsets
from .serializers import *

# Create your views here.

class ClientViewSet(viewsets.ModelViewSet) :
    queryset = Client.objects.all()
    serializer_class = ClientSerializer