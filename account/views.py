from os import access
from drf_yasg import openapi
from . import serializers, utils
from . import models
from .authentications import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, exceptions
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
import requests


class SignupCreateAPIView(generics.GenericAPIView):
    serializer_class = serializers.UserSignupSerializer
    
    @swagger_auto_schema(
        security=[]
    )
    def post(self,request):
        self.serializer_class(data=request.data).is_valid(raise_exception=True)
        pwd = request.data.pop('password',0)
        pwd2 = request.data.pop('confirm_password',0)
        user = models.User.objects.create(
            is_active=True,
            **request.data
        )
        user.set_password(pwd)
        user.save()
        return Response(
            {
                "status": "success",
                "msg": "user resgistred successfully",
                "data": serializers.UserOutSerializer(user).data
            },
            status=201
        )

class LoginAPIView(generics.GenericAPIView):
    serializer_class = serializers.LoginSerializer
    
    @swagger_auto_schema(
        security=[]
    )
    def post(self,request):
        self.serializer_class(data=request.data).is_valid(raise_exception=True)
        user = models.User.objects.filter(
            username=request.data.get('username')
        )
        if not user.exists():
            raise exceptions.AuthenticationFailed()
        
        user = user.first()
        if not user.check_password(request.data.get('password')):
            raise exceptions.AuthenticationFailed()

        access_token, refresh_token = utils.token.encode(
            {
                "id": user.id
            }
        )
        ipinfo_response = requests.get("https://ipinfo.io/json").json()
        document = {
            "city": ipinfo_response.get("city", None),
            "country": ipinfo_response.get("country", None),
            "region": ipinfo_response.get("region", None),
            "ip": ipinfo_response.get("ip", None),
            "user_agent": request.headers.get("User-Agent", None),
            "timezone": ipinfo_response.get("timezone", None),
            "location": ipinfo_response.get("loc", None),
            'access_token': access_token,
            'refresh_token': refresh_token,
            "user_id": user.id,
        }
        models.UserLoggedInSession.objects.create(**document)
        
        return Response(
            {
                "status": "success",
                "msg": "user resgistred successfully",
                "data": {
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }
            },
            status=200
        )

class MeAPIView(generics.GenericAPIView):
    serializer_class = serializers.UserOutSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        return Response(
            {
                "status": "success",
                "msg": "user data",
                "data": self.serializer_class(request.user).data
            },
            status=200
        )

class UserLoggedinSessionAPIView(generics.GenericAPIView):
    serializer_class = serializers.UserLoggedinSessionOutSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        sessions = models.UserLoggedInSession.objects.filter(user=request.user)
        return Response(
            {
                "status": "success",
                "msg": "user session data",
                "data": self.serializer_class(sessions,many=True).data
            },
            status=200
        )

class UserLogOutSessionAPIView(generics.GenericAPIView):
    serializer_class = None
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('session_id', openapi.IN_QUERY, description="session ID", type=openapi.TYPE_STRING)]
    )
    def get(self,request):
        session_id = request.GET.get("session_id", None)
        sessions = models.UserLoggedInSession.filter(user=request.user)
        if session_id == "all":
            ...
        elif session_id is not None:
            sessions = models.UserLoggedInSession.filter(user=request.user, id=session_id)
        else:
            sessions = sessions.filter(access_token=request.META.get("HTTP_AUTHORIZATION"))
        
        sessions.update(
            access_token="",
            refresh_token="",
        )
        return Response(
            {
                "status": "success",
                "msg": "logout success",
                "data": {}
            },
            status=200
        )

class TokenRefreshAPIView(generics.GenericAPIView):
    serializer_class = None
    authentication_classes = []
    permission_classes = []

    def get(self,request,refresh_token):
        payload = utils.token.decode_access_token(refresh_token)
        sessions = models.UserLoggedInSession.filter(user_id=payload['id'],refresh_token=refresh_token)
        access_token, refresh_token = utils.token.encode(
            {
                "id": payload['id']
            }
        )
        sessions.update(
            access_token=access_token,
            refresh_token=refresh_token
        )
        return Response(
            {
                "status": "success",
                "msg": "token refresh success",
                "data": {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }
            },
            status=200
        )