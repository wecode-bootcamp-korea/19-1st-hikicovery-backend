import jwt
from my_settings  import algorithm,SECRET_KEY
from django.http  import JsonResponse
from users.models import User

def login_required(func):
    def decorator(self, request, *args, **kwargs):
        try:
            access_token = request.headers['Authorization']
            token = jwt.decode(access_token, SECRET_KEY, algorithms=algorithm)
            user = User.objects.filter(id=token['id'])
            if user.exists():
                request.user = User.objects.get(id=token['id'])
                return func(self, request, *args, **kwargs)
            return JsonResponse({"message": "UNKNOWN_USER"}, status=401)
        except KeyError:
            return JsonResponse({"message": "INVALID_LOGIN"}, status=401)
        except jwt.DecodeError:
            return JsonResponse({"message": "INVALID_TOKEN"}, status=401)

    return decorator
