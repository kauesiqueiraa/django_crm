from django.contrib import admin
from .models import Lead, Opportunity

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'company_name', 'status', 'created_at')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('status',)

@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'account', 'stage', 'value', 'owner', 'closing_date')
    search_fields = ('name', 'account__name')
    list_filter = ('stage', 'owner')

    # Melhora a seleção de 'account' e 'owner' em vez de um dropdown gigante
    raw_id_fields = ('account', 'owner')
# Register your models here.
