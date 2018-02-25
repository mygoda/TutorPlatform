from django.utils.timezone import is_naive, get_default_timezone, make_aware, now, make_naive, is_aware


def to_aware_datetime(value):
    time_zone = get_default_timezone()
    return make_aware(value, time_zone)


def datetime_now():
    return now()