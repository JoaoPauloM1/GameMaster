from django.urls import path
from hangman.views import hangman

urlpatterns = [
    path('', hangman, name='hangman')
]