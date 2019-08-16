from django.shortcuts import render
from django.contrib.auth import get_user_model
from .models import Complaint

User = get_user_model()


def previous(request):
    if not request.user.is_authenticated:
        return render(request, "registration/home.html", context={"title": "home"})
    user = request.user
    complaints = Complaint.objects.filter(user=user).order_by("-uploaded_at")
    return render(
        request, "complaints/previous_requests.html", context={"complaints": complaints}
    )


# TODO
def open_site(request):
    if request.method == "POST":
        pass
