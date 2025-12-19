import jwt
import bcrypt
import datetime
from django.conf import settings

class AuthService:
    @staticmethod
    def hash_password(plain_password):
      
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(plain_password, hashed_password):

        return bcrypt.checkpw(
            plain_password.encode('utf-8'), 
            hashed_password.encode('utf-8')
        )

    @staticmethod
    def generate_jwt(user_id):
        
        payload = {
            'user_id': user_id,
            'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=2),
            'iat': datetime.datetime.now(datetime.UTC)
        }
        
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token
    @staticmethod
    def decode_jwt(token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            return payload['user_id']
        except:
            return None