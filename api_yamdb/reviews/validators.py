from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone


def year_validator(value):
    year = timezone.now().year
    if value < settings.ZERO_YEAR or value > year:
        raise ValidationError(
            f"The year should be in the range between 0 and {year}.")
