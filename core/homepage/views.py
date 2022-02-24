from django.views.generic import TemplateView, View
from core.user.models import User

class IndexView(TemplateView):
    template_name = 'index.html' 

    