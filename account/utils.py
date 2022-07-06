from typing import List
import uuid
from django.conf import settings
import datetime
from rest_framework.exceptions import AuthenticationFailed
import jwt, re


def validate_email(email_address):
    """
        Validate Email ID
        Params:
            email_address string: user provided email address
    """
    return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email_address))


class Token:
    secret_key = settings.JWT_SECRET_KEY
    
    def encode(self,data: dict) -> List[str]:
        access_token_payload = {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRATION_IN_MINUTES),
            "jti": uuid.uuid4().hex,
            "token_type": "access"
        }
        refresh_token_payload = {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.JWT_REFRESH_TOKEN_EXPIRATION_IN_MINUTES),
            "jti": uuid.uuid4().hex,
            "token_type": "refresh"
        }
        access_token_payload.update(data)
        refresh_token_payload.update(data)
        
        access_token = jwt.encode(
            access_token_payload,
            self.secret_key,
            algorithm='HS256'
        )
        refresh_token = jwt.encode(
            refresh_token_payload,
            self.secret_key,
            algorithm='HS256'
        )
        return access_token, refresh_token
    
    def decode_access_token(self,token: str) -> dict:
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=['HS256']
            )
            if payload.get('token_type') != 'access':
                raise AuthenticationFailed()
            return payload    
        except:
            raise AuthenticationFailed()
        
    def decode_refresh_token(self,token: str) -> dict:
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=['HS256']
            )
            if payload.get('token_type') != 'refresh':
                raise AuthenticationFailed()
            return payload    
        except:
            raise AuthenticationFailed()
        
        
token = Token()