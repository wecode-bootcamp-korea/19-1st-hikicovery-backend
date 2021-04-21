import json
import bcrypt
import jwt

from django.http            import JsonResponse
from django.core.exceptions import ValidationError
from django.views           import View
from django.db.models       import Q

from users.models           import User
from users.validations      import validate_email, validate_phone, validate_password, validate_account
from my_settings            import SECRET_KEY,algorithm

class SignUpView(View):
    def post(self,request):
        data         = json.loads(request.body)
        account      = data['account']
        password     = data['password']
        email        = data['email']
        name         = data['name']
        phone_number = data['phone_number']
        birthday     = data['birthday']

        try:
           
            if User.objects.filter(Q(account=account) |
                                   Q(email=email)
                                   ).exists():
                return JsonResponse({'message': 'ACCOUNT_EXISTS'}, status=400)
             
            if not account or not password or \
                    not name or not email or not phone_number:
                return JsonResponse({'message': 'NO_NECESSARY_VALUES'}, status=400)
             
            if not validate_account(account):
                return JsonResponse({'message': 'USE_VALID_ACCOUNT'}, status=400)
             
            if not validate_password(password):
                return JsonResponse({'message': 'USE_VALID_PASSWORD'}, status=400)
             
            if not validate_email(email):
                return JsonResponse({'message': 'USE_VALID_EMAIL'}, status=400)
             
            if not validate_phone(phone_number):
                return JsonResponse({'message': 'USE_VALID_NUMBER'}, status=400)
             
            hashed_password = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt()).decode()
             
            User.objects.create(
                account      = account,
                password     = hashed_password,
                name         = name,
                phone_number = phone_number,
                email        = email,
                birthday     = birthday,
                address      = data.get('address', None),
                mileage      = data.get('mileage', 3500),
            )
            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except ValidationError:
            return JsonResponse({'message': 'VALIDATION_ERROR'}, status=400)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

class LogInView(View):
    def post(self,request):

        try:
            data = json.loads(request.body)
             
            account  = data['account']
            password = data['password']

            if not validate_account(account):
                return JsonResponse({'message': 'WRONG_ACCOUNT'}, status=400)
             
            if not User.objects.filter(account=account).exists():
                return JsonResponse({'message': 'ACCOUNT_NOT_EXIST'}, status=401)
             
            user_account = User.objects.get(account=account)
            if not bcrypt.checkpw(password.encode('utf-8'), user_account.password.encode('utf-8')):
                return JsonResponse({'message': 'INCORRECT_PASSWORD'}, status=400)
             
            access_token = jwt.encode({'id': user_account.id}, SECRET_KEY = SECRET_KEY, algorithm = algorithm)
            return JsonResponse({'token': access_token, 'message':'SUCCESS'}, status=200)
        except ValidationError:
            return JsonResponse({'message': 'VALIDATION_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
