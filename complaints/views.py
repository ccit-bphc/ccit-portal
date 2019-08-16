from django.shortcuts import render
from django.contrib.auth import get_user_model
from .models import Complaint
from .forms import Complaint_form

User = get_user_model()


def previous(request):
    if not request.user.is_authenticated:
        return render(request, "registration/home.html", context={"title": "home"})
    user = request.user
    complaints = Complaint.objects.filter(user=user).order_by("-uploaded_at")
    return render(
        request, "complaints/previous_requests.html", context={"complaints": complaints}
    )


def complaint_register(request):
    #if not request.user.is_authenticated:
     #   return render(request, "registration/home.html", context={"title": "home"})

    form = Complaint_form(request.POST)
    if form.is_valid():
        form_obj = form.save(commit=False)
        form_obj.user = request.user
        form_obj.save()
        message.success(request, "Your Complaint has been Successfully Registered")
        return render(request, "registration/home.html", context={"title": "home"})
    else:
        form = Complaint_form()
        return render(request, "complaints/complaints_register.html", {"form": form})


# TODO
def open_site(request):
    if request.method == "POST":
        pass
