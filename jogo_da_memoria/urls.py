from django.urls import path
from jogo_da_memoria.views import memoria_view

urlpatterns = [
    path('', memoria_view, name='memoria'),
]