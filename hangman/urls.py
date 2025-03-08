from django.urls import path
from hangman.views import hangman_view

urlpatterns = [
    path('', hangman_view, name='hangman'),
]