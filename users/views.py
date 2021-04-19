import json, traceback
import bcrypt
import jwt

from django.http            import JsonResponse
from django.core.exceptions import ValidationError
from django.views           import View
from django.db.models       import Q

from users.models import User
from users.validations      import validate_email, validate_phone, validate_password, validate_account

from users.models import User


class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if User.objects.filter(Q(account=data["account"]) |
                                   Q(email=data['email'])
                                   ).exists():
                return JsonResponse({'message': 'ACCOUNT_EXISTS'})

            if not data['account'] or not data['password'] or \
                    not data['name'] or not data['email'] or not data['phone_number']:
                return JsonResponse({'message': 'NO_NECESSARY_VALUES'}, status=400)

            if not validate_account(data['account']):
                return JsonResponse({'message': 'USE_VALID_ACCOUNT'}, status=400)

            if not validate_password(data['password']):
                return JsonResponse({'message': 'USE_VALID_PASSWORD'},status=400)

            if not validate_email(data['email']):
                return JsonResponse({'message': 'USE_VALID_EMAIL'},status=400)

            if not validate_phone(data['phone_number']):
                return JsonResponse({'message': 'USE_VALID_NUMBER'},status=400)

            hashed_password = bcrypt.hashpw(data['password'].encode('UTF-8'), bcrypt.gensalt()).decode()

            User.objects.create(
                account      = data['account'],
                phone_number = data['phone_number'],
                name         = data['name'],
                email        = data['email'],
                birthday     = data.get('birthday', 'not available'),
                address      = data.get('address', 'not available'),
                mileage      = data.get('mileage', 3500),
            )
            return JsonResponse({'message': 'SUCCESS', "user_account": data['account']}, status=201)

        except ValidationError:
            return JsonResponse({'message': 'VALIDATION_ERROR'}, status=400)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)


class LogInView(View):
    def post(self, request):

        try:
            data = json.loads(request.body)

            if not validate_account(data['account']):
                return JsonResponse({'message':'WRONG_ACCOUNT'}, status=400)

            if not User.objects.filter(account=data['account']).exists():
                return JsonResponse({'message': 'ACCOUNT_NOT_EXIST'}, status=401)

            user_account = User.objects.get(account=data['account'])
            if not bcrypt.checkpw(data['password'].encode('utf-8'), user_account.password.encode('utf-8')):
                return JsonResponse({'message': 'INCORRECT_PASSWORD'}, status=400)

            access_token = jwt.encode({'id': user_account.id}, 'secret', algorithm='HS256')
            return JsonResponse({'token': access_token, 'message': 'SUCCESS', 'user_account': data['account']},
                                status=200)
        except ValidationError:
            return JsonResponse({'message': 'VALIDATION_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)