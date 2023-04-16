from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

validate = URLValidator(regex='https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}([-a-zA-Z0-9()@:%_\+.~#?&\/=]*)',message='Hello blyat')
try:
    validate('http://www.s.a')
except ValidationError as e:
    print(e)