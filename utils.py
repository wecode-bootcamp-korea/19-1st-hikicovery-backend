import jwt
from my_settings  import algorithm,SECRET_KEY
from django.http  import JsonResponse
from users.models import User

def login_required(func):
    def decorator(self, request, *args, **kwargs):
        try:
            # data = json.loads(request.body)
            # encoded_token = request.body['token']
            encoded_token = request.headers['Authorization']
            decoded_token = jwt.decode(encoded_token, SECRET_KEY, algorithms=algorithm)
            user = User.objects.filter(id=decoded_token['id'])
            if user.exists():
                request.user = user
                return func(self, request, *args, **kwargs)
        except KeyError:
            return JsonResponse({"message": "INVALID_LOGIN"}, status=401)
        except jwt.DecodeError:
            return JsonResponse({"message": "INVALID_TOKEN"}, status=401)
        return JsonResponse({"message": "UNKNOWN_USER"}, status=401)

    return decorator
