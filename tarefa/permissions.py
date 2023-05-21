from django.conf import settings
import jwt
from rest_framework import permissions



from users.models import UsersModel
# from apps.user.services.auth import validate_confirmation_token, validate_token
class IsNotSuspended(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return not user.suspenso
    
def validate_token(token):
    try:
       
        payload_unsafe = jwt.decode(token,settings.SECRET_KEY,algorithms=['HS256'])
       
        user = UsersModel.objects.filter(id=payload_unsafe["user_id"]).first()
        
        if not user:
            return False

        user.refresh_from_db()
        # key = user.password + SECRET
        # payload = jwt.decode(token, key, algorithms="HS256")

        return user
    except Exception as e:
        
        return False
    
def has_user_permission(user, path):
    user_id = path.split("/")[-3]
    return str(user.id) == user_id and not user.is_blocked


class ValidToken(permissions.BasePermission):

    def has_permission(self, request, view):
        token = request.headers.get("token")
        
        user = validate_token(token)
        # print(user)
        if not user:
            return False

        request.user = user
        
        return True

class ValidAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        token = request.headers.get("token")
        payload_unsafe = jwt.decode(token,settings.SECRET_KEY,algorithms=['HS256'])
        # print(payload_unsafe)
        try:
            user = UsersModel.objects.get(id=payload_unsafe["user_id"],tipo="root")
            print(user)
            if not user:
                return False
            request.user = user
            return True
        except Exception as e:
        
            return False
        # if (not user):
        #     return False

        # request.user = user
        
        # return True
    # has_user_permission(user, request.get_full_path())