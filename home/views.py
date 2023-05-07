from django.shortcuts import render
from login.models import Notification


# Create your views here.
def index(request):
    notifications = Notification.objects.filter(to_user=request.user.pk)
    content = {"notifications": notifications}
    print(request.META.get("HTTP_REFERER"))
    return render(request, "home/home.html", content)
