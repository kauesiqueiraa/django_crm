from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Modelo de usuário customizado.
    Herda de AbstractUser, então já temos username, email, password, etc.
    """

    # Nossos campos customizados
    ROLE_CHOICES = (
        ('admin', 'Administrador'),
        ('vendedor', 'Vendedor'),
        ('gerente', 'Gerente'),
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='vendedor',
    )

    def __str__(self):
        return self.username
