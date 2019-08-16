from django.urls import path, include
from complaints import views

urlpatterns = [
    path("previous/", views.previous, name="previous-requests"),
    path("open-site/", views.open_site, name="open-site"),
    path("home/", views.complaint_register, name="complaint-register"),
]