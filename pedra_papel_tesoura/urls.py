from django.urls import path
from pedra_papel_tesoura.views import pedra_papel_tesoura_view

urlpatterns = [
    path('', pedra_papel_tesoura_view, name='pedra_papel_tesoura'),
]