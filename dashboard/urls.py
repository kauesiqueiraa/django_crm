from django.urls import path
from .views import DashboardView

app_name = 'dashboard'
urlpatterns = [
    # A raiz ('' - vazio) do app vai para a DashboardView
    path('', DashboardView.as_view(), name='home'),
]