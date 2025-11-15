from django.db import models

class Account(models.Model):
    """ 
    Represents a company (Client or Prospect)
    """
    name = models.CharField(max_length=255, verbose_name="Nome da Empresa")
    industry = models.CharField(max_length=100, blank=True, null=True, verbose_name="Indústria")
    website = models.URLField(blank=True, null=True)
    cnpj = models.CharField(max_length=18, blank=True, null=True, verbose_name="CNPJ")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Contact(models.Model):
    """
    Represents an Person (Contact) within a company
    """
    # Relationships: An Contact belongs to an Account.
    # If the Account is deleted, the Contact is also deleted(models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='contacts')

    first_name = models.CharField(max_length=100, verbose_name="Nome")
    last_name = models.CharField(max_length=100, verbose_name="Sobrenome")
    email = models.EmailField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")
    role = models.CharField(max_length=100, blank=True, null=True, verbose_name="Cargo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.account.name})"
