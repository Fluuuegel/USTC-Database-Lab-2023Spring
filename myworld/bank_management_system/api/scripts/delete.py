from api.models import Client

def run():
    Client.objects.all().delete()