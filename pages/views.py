from django.shortcuts import render


def home(request):
    return render(
        request, "registration/home.html", context={"title": "CCIT Complaint Portal"}
    )


def contact(request):
    return render(
        request, "registration/contact.html", context={"title": "CCIT Contact Us"}
    )
