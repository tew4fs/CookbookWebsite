from django.views.generic import TemplateView

from login.models import Notification

class LandingPage(TemplateView):
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notifications = Notification.objects.filter(to_user=self.request.user.pk)
        context["notifications"] = notifications
        return context
