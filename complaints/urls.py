from django.urls import path, include
from complaints import views

urlpatterns = [
    path("previous_tickets/", views.previous, name="previous-requests"),
    path("open-site/", views.open_site, name="open-site"),
    path("add_tickets/", views.complaint_register, name="complaint-register"),
    path("handle_tickets/", views.complaint_handle, name="complaint-handle"),
]
