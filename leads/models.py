from django.db import models
from django.conf import settings #Para pegar o AUTH_USER_MODEL
from accounts.models import Account # Para relacionar a Oportunidade

class Lead(models.Model):
    """
    Um prospect inicial. Agora com um 'dono'.
    """
    first_name = models.CharField(max_length=100, verbose_name="Nome")
    last_name = models.CharField(max_length=100, verbose_name="Sobrenome")
    company_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Empresa")
    email = models.EmailField(max_length=255, blank=True, null=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")

    STATUS_CHOICES = (
        ('novo', 'Novo'),
        ('contatado', 'Contatado'),
        ('qualificado', 'Qualificado'),
        ('perdido', 'Perdido'),
        ('convertido', 'Convertido'),
    )
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='novo')

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="leads_owned",
        verbose_name="Dono do Lead"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.status})"


class Opportunity(models.Model):
    """
    Um negócio qualificado (um Lead convertido). Tem valor e está no funil.
    """
    STAGE_CHOICES = (
        ('prospeccao', 'Prospecção'),
        ('proposta', 'Proposta'),
        ('negociacao', 'Negociação'),
        ('ganho', 'Fechado (Ganho)'),
        ('perdido', 'Fechado (Perdido)'),
    )

    # Relacionamento: A qual empresa (Account) esse negócio pertence?
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="opportunities")

    # Relacionamento: Qual vendedor (User) é o dono desse negócio?
    # Usamos settings.AUTH_USER_MODEL para referenciar nosso User customizado.
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, # Se o vendedor for deletado, o negócio ficar "sem dono"
        null=True,
        related_name="opportunities"
    )

    name = models.CharField(max_length=255, verbose_name="Nome do Negócio")
    stage = models.CharField(max_length=15, choices=STAGE_CHOICES, default='prospeccao')
    value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Valor (R$)")
    closing_date = models.DateField(blank=True, null=True, verbose_name="Data de Fechamento")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

