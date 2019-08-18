"""Module for setting url paths"""
from django.urls import path
from complaints import views

urlpatterns = [
    path("previous_tickets/", views.previous, name="previous-requests"),
    path("open-site/", views.open_site, name="open-site"),
    path("add_tickets/", views.register_complaint, name="complaint-register"),
    path("handle_tickets/", views.handle_complaint, name="complaint-handle"),
]
