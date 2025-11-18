from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum

from leads.models import Lead, Opportunity

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.role == 'gerente':
            leads_qs = Lead.objects.all()
            opps_qs = Opportunity.objects.all()
        else:
            leads_qs = Lead.objects.filter(owner=user)
            opps_qs = Opportunity.objects.filter(owner=user)

        context['total_leads'] = leads_qs.filter(status='novo').count()

        active_stages = ['prospeccao', 'proposta', 'negociacao']
        context['total_opportunities'] = opps_qs.filter(stage__in=active_stages).count()

        pipeline_value = opps_qs.filter(stage__in=active_stages).aggregate(Sum('value'))
        context['pipeline_value'] = pipeline_value['value__sum']

        return context
