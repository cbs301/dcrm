import re
from django.core.exceptions import ValidationError


class StrongPasswordValidator:
    def validate(self, password, user=None):
        errors = []
        if len(password) < 10:
            errors.append('at least 10 characters')
        if not re.search(r'[A-Z]', password):
            errors.append('an uppercase letter')
        if not re.search(r'[a-z]', password):
            errors.append('a lowercase letter')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\\/`~;\'']', password):
            errors.append('a special character')
        if errors:
            raise ValidationError(f'Password must contain {", ".join(errors)}.')

    def get_help_text(self):
        return 'Your password must be at least 10 characters and include an uppercase letter, a lowercase letter, and a special character.'
