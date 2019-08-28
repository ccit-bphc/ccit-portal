"""Decorators for checking permissions."""
from django.contrib.auth.decorators import login_required, user_passes_test


def user_is_logged_in_and_active(function):
    user_is_active = user_passes_test(lambda u: u.is_active, login_url="denied")
    return login_required(user_is_active(function), login_url="account-login")


def user_is_staff(function):
    staff_user = user_passes_test(lambda u: u.is_staff, login_url="denied")
    return staff_user(function)


def user_is_nucleus(function):
    nucleus_user = user_passes_test(
        lambda u: u.groups.filter(name="nucleus"), login_url="denied"
    )
    return nucleus_user(function)


def user_is_staff_or_nucleus(function):
    dec_func = user_passes_test(
        lambda u: u.is_staff or u.groups.filter(name="nucleus").exists(),
        login_url="denied",
    )
    return dec_func(function)
