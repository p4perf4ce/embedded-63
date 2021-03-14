
from iotlib.serializers import ShelfInfoSerializer, ShelfStateSerializer
from iotlib.models import Shelf
from rest_framework import viewsets, permissions, mixins, authentication
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

for user in User.objects.all():
    Token.objects.get_or_create(user=user)

# Create your views here.

__DEBUG_GREETING_MESSAGE = "Hello, welcome to index. {}"

def index(request: HttpRequest):
    return HttpResponse(content=__DEBUG_GREETING_MESSAGE.format(request.body))

class ShelfInfoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    End point for querying shelf information.\n
    **State-Info:**\n
        AV - Available\n
        OH - On-Hold\n
        MS - Missing\n
        IS - In Storage\n
    """
    queryset = Shelf.objects.all()
    serializer_class = ShelfInfoSerializer
    permission_classes = [permissions.AllowAny]


class ShelfStateViewSet(
    mixins.ListModelMixin,
    # mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
    # viewsets.ModelViewSet
    ):
    """
    End point for update shelf information. \n
    """
    queryset = Shelf.objects.all()
    serializer_class = ShelfStateSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication, authentication.TokenAuthentication]

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, *kwargs)