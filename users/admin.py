from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    """
    Define o painel de admin para o usuário Customizado.
    """
    # Adciona o campo 'role' aos 'fieldsets' na página de edição do usuário
    fieldsets = UserAdmin.fieldsets + (
        ('Funções Customizadas', {'fields': ('role',)}),
    )
    # Adiciona 'role' as 'add_fieldsets' na página de criação do usuário
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Funções Customizadas', {'fields': ('role',)}),
    )
    # Adiciona 'role' às colunas exibidas na lsita de usuários
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'role')

#Registra nosso modelo User com a classe de admin customizada
admin.site.register(User, CustomUserAdmin)