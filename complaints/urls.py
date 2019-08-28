"""Module for setting url paths"""
from django.urls import path
from complaints import views

urlpatterns = [
    path("my-tickets/", views.previous, name="previous-requests"),
    path("request-unblock/", views.request_unblock, name="unblock-request"),
    path("add-tickets/", views.register_complaint, name="complaint-register"),
    path("handle-tickets/", views.display_to_staff, name="complaint-display"),
    path("resolve-tickets/", views.handle_complaint, name="complaint-resolve"),
    path(
        "resolve-unblock-requests/",
        views.handle_unblock_request,
        name="update_request_resolve",
    ),
]
