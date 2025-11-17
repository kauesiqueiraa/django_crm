from django.urls import path
from .views import LeadListView, LeadCreateView, LeadDetailView

app_name = 'leads'
urlpatterns = [
    path('', LeadListView.as_view(), name='list'),
    path('create/', LeadCreateView.as_view(), name='create'),
    path('<int:pk>/', LeadDetailView.as_view(), name='detail')
]