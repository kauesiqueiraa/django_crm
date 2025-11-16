from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Lead

class LeadListView(LoginRequiredMixin, ListView):
    model = Lead
    template_name = 'leads/lead_list.html'
    context_object_name = 'leads'

    def get_queryset(self):
        # No futuro iremos filtrar isso por vendedor
        return Lead.objects.all().order_by('-created_at')

