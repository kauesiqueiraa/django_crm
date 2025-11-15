from django.contrib import admin
from .models import Account, Contact

class ContactInline(admin.TabularInline):
    """Permite ver/editar Contatos dentro da página da Conta"""
    model = Contact
    extra = 1 # Quantos formulários em branco mostrar

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'industry', 'website', 'created_at')
    search_fields = ('name', 'cnpj')
    inlines = [ContactInline] # Adiciona os contatos inline

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'account', 'email', 'phone', 'role')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('account',)

# Register your models here.
