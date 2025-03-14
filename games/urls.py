from django.urls import path
from games.views import forca_view, batalha_naval_view, jogo_da_memoria_view, pedra_papel_tesoura_view, blackjack_view, fazenda_view, clique_view

urlpatterns = [
    path('forca/', forca_view, name='forca'),
    path('batalha-naval/', batalha_naval_view, name='batalha_naval'),
    path('jogo-da-memoria/', jogo_da_memoria_view, name='jogo_da_memoria'),
    path('pedra-papel-tesoura/', pedra_papel_tesoura_view, name='pedra_papel_tesoura'),
    path('blackjack/', blackjack_view, name='blackjack'),
    path('fazenda/', fazenda_view, name='fazenda'),
    path('clique/', clique_view, name='clique'),
]