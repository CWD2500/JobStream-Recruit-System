import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomPasswordValidator:
    """
    Custom validator to match JavaScript criteria.
    - At least one lowercase letter.
    - At least one uppercase letter.
    - At least one digit.
    - Minimum length of 8 characters.
    """
    def __init__(self, min_length=8):
        self.min_length = min_length
        self.regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$')

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                _("كلمة المرور يجب أن تكون بطول %(min_length)d أحرف على الأقل."),
                code='password_too_short',
                params={'min_length': self.min_length},
            )
        if not self.regex.match(password):
            raise ValidationError(
                _("كلمة المرور يجب أن تحتوي على حروف كبيرة وصغيرة، وأرقام."),
                code='password_weak',
            )

    def get_help_text(self):
        return _("كلمة المرور يجب أن تحتوي على حروف كبيرة وصغيرة، وأرقام، ويجب أن تكون بطول 8 أحرف على الأقل.")
