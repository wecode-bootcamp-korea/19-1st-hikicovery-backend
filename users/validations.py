import re

def validate_account(value):
    ACCOUNT_REG = r"(^[a-zA-Z0-9]+.{6,15}$)"
    regex = re.compile(ACCOUNT_REG)

    if regex.match(value):
        return True

def validate_email(value):
    EMAIL_REG = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    regex = re.compile(EMAIL_REG)

    if regex.match(value):
        return True

def validate_phone(value):
   PHONE_REG = r"([0-9]{3}-[0-9]{4}-[0-9]{4})"
   regex = re.compile(PHONE_REG)
   
   if regex.match(value):
        return True

def validate_password(value):
    PASSWORD_REG = r"(^(?=.*[a-zA-Z])((?=.*\d)|(?=.*\W)).{6,20}$)"
    regex = re.compile(PASSWORD_REG)

    if regex.match(value):
        return True
