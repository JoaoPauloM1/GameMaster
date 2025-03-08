from django.urls import path
from batalha_naval.views import battleship_view

urlpatterns = [
    path('', battleship_view, name='battleship'),
]