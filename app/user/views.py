"""
 Views for the Create User API
"""
from rest_framework import generics, permissions, authentication
from user.serializers import UserSerializer
from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """ create a new user in the system """
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """ create a new auth token for user """
    serializer_class = AuthTokenSerializer

    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """ manage the authenticated user """
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """ retrieve and return authenticated user """
        return self.request.user
