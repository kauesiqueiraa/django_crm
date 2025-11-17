from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Lead

class LeadListView(LoginRequiredMixin, ListView):
    model = Lead
    template_name = 'leads/lead_list.html'
    context_object_name = 'leads'

    def get_queryset(self):
        user = self.request.user

        if user.role == 'gerente':
            return Lead.objects.all().order_by('-created_at')
        else:
            return Lead.objects.filter(owner=user).order_by('-created_at')

class LeadCreateView(LoginRequiredMixin, CreateView):
    model = Lead
    template_name = 'leads/lead_form.html'
    # Campos que o usuário poderá preencher no formulário
    fields = ['first_name', 'last_name', 'company_name', 'email', 'phone', 'status']
    # Para onde ir após o sucesso
    success_url = reverse_lazy('leads:list')

    def form_valid(self, form):
        # Lógica Nivel Pleno: Define o 'dono' automaticamente
        form.instance.owner = self.request.user
        return super().form_valid(form)

class LeadDetailView(LoginRequiredMixin, DetailView):
    model = Lead
    template_name = 'leads/lead_detail.html'
    context_object_name = 'lead'

    def get_queryset(self):
        user = self.request.user
        if user.role == 'gerente':
            return Lead.objects.all()
        else:
            return Lead.objects.filter(owner=user)


