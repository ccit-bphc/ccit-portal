"""CCIT_Portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from importlib import import_module
from django.contrib import admin
from django.urls import path, include
from allauth.account.views import LoginView, LogoutView
from allauth.socialaccount import providers
from pages import views as pages_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("contact/", pages_views.contact, name="contact-us"),
    path("complaints/", include("complaints.urls")),
    path("denied/", pages_views.denied, name="denied"),
    path("", pages_views.home, name="home"),
    path("login/", LoginView.as_view(), name="account-login"),
    path("logout/", LogoutView.as_view(), name="account-logout"),
    path("signup/", pages_views.signup, name="account_signup"),
    path("social/", include("allauth.socialaccount.urls")),
]

# Provider urlpatterns, as separate attribute (for reusability).
provider_urlpatterns = []
for provider in providers.registry.get_list():
    try:
        prov_mod = import_module(provider.get_package() + ".urls")
    except ImportError:
        continue
    prov_urlpatterns = getattr(prov_mod, "urlpatterns", None)
    if prov_urlpatterns:
        provider_urlpatterns += prov_urlpatterns
urlpatterns += provider_urlpatterns

