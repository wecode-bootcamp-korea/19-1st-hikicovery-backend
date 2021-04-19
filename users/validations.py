import re

def validate_account(value):
    account_reg = r"(^[a-zA-Z0-9]+.{6,15}$)"
    regex = re.compile(account_reg)
    if regex.match(value):
        return True
    else:
        return False

def validate_email(value):
    email_reg = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    regex = re.compile(email_reg)
    if regex.match(value):
        return True
    else:
        return False

def validate_phone(value):
    phone_reg = r"([0-9]{3}-[0-9]{4}-[0-9]{4})"
    regex = re.compile(phone_reg)

    if regex.match(value):
        return True
    else:
        return False

def validate_password(value):
    password_reg = r"(^(?=.*[a-zA-Z])((?=.*\d)|(?=.*\W)).{6,20}$)"
    # 6~ 20자 길이. 최소 1개의 숫자 혹은 특수문자 포함.
    regex = re.compile(password_reg)

    if regex.match(value):
        return True
    else:
        return False