from django.urls import path
from home.views import LandingPage

urlpatterns = [
    path("", LandingPage.as_view(), name="landing"),
]
