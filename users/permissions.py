"""Decorators for checking permissions."""
from django.contrib.auth.decorators import login_required, user_passes_test


def user_is_logged_in_and_active(function):
    user_is_active = user_passes_test(lambda u: u.is_active, login_url="denied/")
    return login_required(user_is_active(function), login_url="/")


def user_is_staff(function):
    staff_user = user_passes_test(lambda u: u.is_staff, login_url="denied/")
    return login_required(staff_user(function), login_url="/")
