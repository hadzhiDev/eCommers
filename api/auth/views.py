from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView, get_object_or_404, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from account.models import User

from api.auth.mixins import UltraModelViewSet
from api.auth.serializers import LoginSerializer, UserSerializer, RegisterUserSerializer, ProfileSerializer, \
    ChangePasswordSerializer


class LoginGenericAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(email=email, password=password)
        if user:
            token = Token.objects.get_or_create(user=user)[0]
            user_serializer = UserSerializer(instance=user, context={'request': request})
            return Response({
                **user_serializer.data,
                'token_key': token.key
            })
        return Response({'massage': 'The user is not found or the password is invalid'},
                        status=status.HTTP_400_BAD_REQUEST)


class RegisterGenericApiView(GenericAPIView):
    serializer_class = RegisterUserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get_or_create(user=user)[0]
        user_serializer = UserSerializer(instance=user, context={'request': request})
        return Response({
            **user_serializer.data,
            'token': token.key,
        })


class ProfileViewSet(UltraModelViewSet):
    queryset = User.objects.all()
    # pagination_class = SimpleResultPagination
    serializer_class = ProfileSerializer
    lookup_field = 'id'
    permission_classes = (AllowAny,)


class ChangePasswordApiView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (AllowAny,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if self.object.check_password(serializer.data.get("old_password")):
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                    'data': []
                }

                return Response(response)
            else:
                return Response({"old_password": ['Wrong password']}, status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)