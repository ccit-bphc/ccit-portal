from django.urls import path, include
from complaints import views
from .. import pages

urlpatterns = [
    path("previous/", views.previous, name="previous-requests"),
    path("open-site/", views.open_site, name="open-site"),
    path("complaints/", views.complaint_register, name="complaint-register"),
    path("contact/", pages.views.contact, name="contact-us"),
]
