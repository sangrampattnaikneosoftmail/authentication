from os import access
from rest_framework import authentication, exceptions
from . import models, utils


class JWTAuthentication(authentication.BaseAuthentication):
    
    def authenticate(self, request):
        try:
            header = request.META['HTTP_AUTHORIZATION']
            prefix, token = header.split()
            if prefix != "Bearer":
                raise exceptions.NotAuthenticated(detail="unauthorized request")
            
            payload = utils.token.decode_access_token(token)
            sessions = models.UserLoggedInSession.objects.filter(
                access_token=token
            )
            if not sessions.exists():
                raise exceptions.NotAuthenticated(detail="user does not exist with this token", code=404)
            users = models.User.objects.filter(id=payload['id'])
            if not users.exists():
                raise exceptions.NotAuthenticated(detail="user does not exist with this token", code=404)
            
            user = users.first()
            
            payload['session_id'] = sessions.first().id
            return user, payload
        except (KeyError, ValueError):
            raise exceptions.NotAuthenticated(detail="unauthorized request")