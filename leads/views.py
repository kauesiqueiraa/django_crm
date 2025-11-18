from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db import transaction
from accounts.models import Account, Contact
from .models import Lead, Opportunity

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

class LeadUpdateView(LoginRequiredMixin, UpdateView):
    model = Lead
    template_name = 'leads/lead_form.html'
    fields = ['first_name', 'last_name', 'company_name', 'email', 'phone', 'status']
    context_object_name = 'lead'

    def get_queryset(self):
        user = self.request.user
        if user.role == 'gerente':
            return Lead.objects.all()
        else:
            return Lead.objects.filter(owner=user)
    
    def get_success_url(self):
        # Retorna para a página de detalhes do lead que acabou de ser editado
        return reverse_lazy('leads:detail', kwargs={'pk': self.object.pk})

class LeadDeleteView(LoginRequiredMixin, DeleteView):
    model = Lead
    template_name = 'leads/lead_confirm_delete.html'
    context_object_name = 'lead'
    success_url = reverse_lazy('leads:list')

    def get_queryset(self):
        user = self.request.user
        if user.role == 'gerente':
            return Lead.objects.all()
        else:
            return Lead.objects.filter(owner=user)


class LeadConvertView(LoginRequiredMixin, View):
    """ 
    View manual (não generica) para controllar o processo exato de conversão.
    """
    def get(self, request, pk):
        lead = get_object_or_404(Lead, pk=pk, owner=request.user)
        return render(request, 'leads/lead_convert.html', {'lead': lead})

    def post(self, request, pk):
        lead = get_object_or_404(Lead, pk=pk, owner=request.user)

        with transaction.atomic():
            # 1. Criar a Conta (Empresa)
            account_name = lead.company_name if lead.company_name else f"Família {lead.last_name}"
            account = Account.objects.create(
                name=account_name
            )

            # 2. Criar o Contato (Pessoa) vinculado à Conta
            contact = Contact.objects.create(
                account=account,
                first_name=lead.first_name,
                last_name=lead.last_name,
                email=lead.email,
                phone=lead.phone
            )

            # 3. Criar a Oportunidade (Negócio) vinculada à Conta e ao Vendedor
            opportunity = Opportunity.objects.create(
                name=f"Negócio com {account_name}",
                account=account,
                owner=request.user,
                stage='prospeccao'
            )

            # 4. Atualizar o Lead antigo (Não deletamos, apenas marcamos como convertido) 
            lead.status = 'convertido'
            lead.save()

        return redirect('leads:list')
